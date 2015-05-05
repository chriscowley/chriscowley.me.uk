---
layout: post
title: "Identify and mounting Cinder Volumes in using Openstack Heat"
date: 2015-05-05 18:51
comments: true
categories: ['openstack']
---
I'm back playing with Openstack again. The day job once again Openstack based, and as of last week my lab is all Openstack too. While [oVirt](http://ovirt.org) is awesome, I felt like a change.

Anyway, the meat of today's problem comes from the day job. I have some instances deployed via heat that have multiple Cinder volumes attached to them, these then need to be mounted in a certain way. The syntax for attaching a cinder volume to an instance is:

```

instance_vol_att:
    type: OS::Cinder::VolumeAttachment
    properties:
      instance_uuid:  { get_resource: instance }
      volume_id: { get_resource: instance_vol_data }
      mountpoint: /dev/vdb
```

See at the end there is `mountpoint`? Awesome, my device will always appear as /dev/vdb!

No! Unfortunately, there is no link between Cinder/Nova and _udev_ within the instance. As a result, udev will simply assign it a device name in the same way your workstation does to a USB key: it could be anything.

So what is a poor Openstack admin to do? 

Each volume has a UUID, which in the example above. Lets start with a simple HOT template to create a single instance and volume:

```
heat_template_version: 2014-10-16
description: A simple server to run Jenkins

parameters:
  imageid:
    type: string
    default: Centos-7-x64
    description: Image use to boot a server

resources:
  jenkins:
    type: OS::Nova::Server
    properties:
      image: { get_param: ImageID }
      flavor: m1.tiny
      networks:
      - network: { get_param: NetID }
  jenkins_data:
    type: OS::Cinder::Volume
    properties:
      size: 50G
  jenkins_data_att:
    type: OS::Cinder::VolumeAttachment
    properties:
      instance_uuid: { get_resource: jenkins }
      volume_id: { get_resource: jenkins_data}
```

That will create everything we need. The rest we need to pass though from Nova to the instance somehow. While Nova does not talk to udev, it does pass the `volume_id` though, albeit with a caveat. the ID is truncated to **20** characters and is available as `/dev/disk/by-id/virtio-volid20chars`. We can now access this using the userdata property and `cloud-init`.

I actually create a small bash script then run it later, so now my _Server_ resource will look like:

```
jenkins:
  type: OS::Nova::Server
    properties:
      image: { get_param: ImageID }
      flavor: m1.tiny
      networks:
        - network: { get_param: NetID }
      user_data_format: RAW
      user_data:
        str_replace:
          template: |
            #cloud-config
            write_files:
              - content: |
                  #!/bin/bash
                  vol-data_id="%vol-data_id%"
                  vol-data_dev="/dev/disk/by-id/virtio-$(echo ${vol-images_id} | cut -c -20)"
                  mkfs.ext4 ${vol-data_dev}               
                  mkdir -pv /var/lib/jenkins
                  echo "${vol-data_dev} /var/lib/jenkins ext4 defaults 1 2" >> /etc/fstab
                  mount /var/lib/jenkins
                path: /tmp/format-disks
                permissions: '0700'
            runcmd:
              - /tmp/format-disks
          params:
            "%vol-data-id%": { get_resource: jenkins_data }
```


          

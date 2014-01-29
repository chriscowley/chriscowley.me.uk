---
layout: post
title: "Docker and GRE tunnels"
date: 2014-01-29 11:23
comments: true
categories: ['linux', 'networking', 'sdn', 'openvswitch']
---
Recently I have been playing around with LXC and Open vSwitch. Allied this with my interest in all things DevOps and it was only natural that I would try my hand at building a GRE tunnel between Docker containers on seperate hosts.

<!-- more -->

The basic goal is something like this:



I am using Fedora 20, because I like it, but I reckon this will work on CentOS too, although you I think you will need to build Open vSwitch from source. Also, I should give thanks to @scottlowe who wrote up how to do this with Ubuntu. His [article](http://blog.scottlowe.org/2013/05/07/using-gre-tunnels-with-open-vswitch/) was very helpful. 

{% img center https://docs.google.com/drawings/d/1WK9tieEc-PRPmX9FRjcLYNFT7DQvrtkCk-kQapS-EHY/pub?w=1440&h=1080 %}

# Getting the Open vSwitches talking to each other.

Before you can do anything else get switches communicating with each other over a GRE tunnel. To do this you need a couple of bridges:

* A standard layer 2 bridge to connect your container interfaces to (`docker0`)
* Another within the Openvswitch (`br0`)

# Install Docker

```
yum install docker-io
```

Unfortunately you need to edit the Systemd service file. The problem is that Docker will create another bridge to attach the containers to. We have already created the bridge and wired it up as required. To avoid this you need to tell it not to create to create that bridge. Edit the file `/usr/lib/systemd/system/docker.service` and change the line:

```
ExecStart=/usr/bin/docker -d
```

To read:

```
ExecStart=/usr/bin/docker -d -b=none
```

This is not ideal, a config option would be better. We shall see what happens in the future.

First you need a couple of packages:

```
sudo yum install openvswitch docker-io
sudo systemctl enable openvswitch
```


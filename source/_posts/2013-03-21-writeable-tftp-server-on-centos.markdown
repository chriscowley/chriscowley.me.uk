---
layout: post
title: "Writeable TFTP Server On Centos"
date: 2013-01-21 10:39
comments: true
categories: linux
---
Well this caught me out for an embarassingly long time. There are [loads](http://blog.penumbra.be/tag/tftp/) [of](http://www.question-defense.com/2008/11/13/linux-setup-tftp-server-on-centos) [examples](http://wiki.centos.org/EdHeron/PXESetup) of setting up a TFTP server on the web. The vast majority of them assume that you are using them read-only for PXE booting.

I needed to make it writeable so that it could be used for storing switch/router backups. It is trivially simple once you have read the man page (pro tip: RTFM).

First install it (install the client as well to test at the end:

```
yum install tftp tftp-server xinetd
chkconfig xinetd on
```

Now edit the file `/etc/xinetd.d/tftp to read:

```
service tftp
{
    socket_type = dgram
    protocol    = udp
    wait        = yes
    user        = root
    server      = /usr/sbin/in.tftpd
    server_args = -c -s /var/lib/tftpboot
    disable     = no
    per_source  = 11
    cps         = 100 2
    flags       = IPv4
}
```

There are 2 changes to this file from the defaults. The `disable` line enables the service. Normally that is where you leave it. However, you cannot upload to the server in this case without pre-creating the files.

The second change adds a `-c` flag to the `server_args` line. This tells the service to create the files as necessary.

It still will not work though. You need to tweak the filesystem permissions and SELinux:

```
chmod 777 /var/lib/tftpboot
setsebool -P tftp_anon_write 1
```

You should now be able to upload something to the server

```
echo "stuff" > test
tftp localhost -c put test
```

Your test file should now be in `var/lib/tftpboot`.
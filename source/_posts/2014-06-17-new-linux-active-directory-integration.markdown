---
layout: post
title: "New Linux Active Directory Integration"
date: 2014-06-17 10:28
comments: true
categories: ['linux']
---
This used to be quite complex, but now is astoundingly simple. Now there is a new project call [realmd](http://freedesktop.org/software/realmd/). It is in recent version of Debian (Jessie and Sid) and Ubuntu (since 13.04). For Red Hat types, it is RHEL7 and Fedora (since 18).

<!-- more -->

If you're on Debian/Ubuntu, install with:

```
apt-get install realmd
```

For RHEL/Fedora:

```
sudo yum install realmd
```

Now you can go ahead and join the domain:

```
sudo realm join --user=<admin-user> example.com
```

That is it, you can check this by running `sudo realm list`, which will give you something like:

```
example.com
  type: kerberos
  realm-name: EXAMPLE.COM
  domain-name: example.com
  configured: kerberos-member
  server-software: active-directory
  client-software: sssd
  required-package: oddjob
  required-package: oddjob-mkhomedir
  required-package: sssd
  required-package: adcli
  required-package: samba-common
  login-formats: %U@example.com
  login-policy: allow-realm-logins
```

The last step is `sudo`. If you want to have everyone in *Domain Admins* have permission to run everything as root, then add the following to `sudoers`:

```
%domain\ admins@example.com ALL=(ALL)       ALL
```

By default `realmd` used SSSD to perform the authentication. This in turn configures Kerberos and LDAP.

My initial testing has been performed with an Active Directory that has "Identity Managment for UNIX" installed. However, I forgot to actually enable my user for UNIX. Even so, it worked perfectly. It sees my Windows groups and defines a home directory of `/home/example.com/<username>`. I am pretty certain that you do not need to extend AD, it should work out of the box from what I can see.

As a bonus, it seems to respect nested groups, something that has always been a bug bear in these things.

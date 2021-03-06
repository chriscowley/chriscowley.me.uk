---
layout: post
title: "Integrating RHEL with Active Directory"
date: 2013-12-16 09:52
comments: true
categories: linux
---
I had a request on Reddit to share a document I wrote about connect Red Hat Enterprise Linux with Active Directory. The original document I wrote is confidential, but I said I would write it up.

This works for both Server 2008(R2) and 2012. If I recall correctly it will also work with 2003, but may need to minor terminology changes on the Windows side. From the Linux side, it should be fine with RHEL 6 and similar (CentOS and Scientific Linux). It should also apply to Fedora, but your mileage may vary.

<!-- more -->

So without further ado, let's dive in. To do this you need to know what is actually happening under the surface when you authenticate to AD from a client. The basic idea looks something like this:

{% img center https://docs.google.com/drawings/d/1tjaacfXrTJtOZCREonoXzdHfgZQHssQ2zkDzFpLGeX0/pub?w=960&h=720 %}

Integration with AD requires the installation of a few services in Red Hat, along with some minor modifications on the Windows Domain Controllers. On the Linux side, everything revolves around the System Security Services Daemon (SSSD). All communication between the PAM and the various possible back-ends is brokered through this daemon. This is only one solution, there are several. The others involve Winbind (which I have found problematic), or LDAP/Kerberos directly (no offline authentication, more difficult to set up). Note that this does not give you any file sharing, but  can easily be extended to do so using Samba.

PAM communicates with SSSD, which in turn talks to Active Directory via LDAP and Kerberos. Identification is performed via LDAP, with the user is authenticated using Kerberos. These different components have some prerequisites on Windows.

- DNS must be working fully - both forward and reverse lookups should be functional. If the Kerberos server (Windows Domain Controller) cannot identify the client via DNS, Kerberos will fail.
- Accurate time is essential – if the two systems have too larger difference in time (about 5 minutes), Kerberos will fail.
- The Active Directory needs to be extended to include the relevant information for *NIX systems (home directory, shell, UUID/GUID primarily).
   - They are actually there, but empty and uneditable. The necessary GUI fields are part of “Identity Management for UNIX”
- It must be possible for the Linux client to perform an LDAP search. This could be either via an anonymous bind or authenticated.
   - Anonymous is obviously not recommended.
   - Simple binds (username/password) do work but are not recommended. Although I am not one to practise what I preach (see below).
   - The best option is SASL/GSSAPI, using a keytab generated by Samba. This does not require Admin privileges on Windows, only permissions to join computers to the domain.

For both DNS and NTP I'm assuming that you are using the services provided by Active Directory. It is possible to break those out to other boxes, but it beyond my Windows Admin ability/desire to do so.
   
# Preparing Active Directory

In Server Manager, add the Role Service "Identity Management for UNIX". This is under the Role "Active Directory Domain Services" (took me a while to find that). When it asks, use your AD domain name as the NIS name. For example, with a AD domain of _chriscowley.lab_, use _chriscowley_.

Once that is installed, create a pair of groups. For the sake of argument, lets call them _LinuxAdmin_ and _LinuxUser_. The intended roles of these 2 groups is left as an exercise for the reader. When you create these groups, you will see a new tab in the properties window for both groups and users: "UNIX Attributes".

Now go ahead and create a user (or edit an existing one). Go into the UNIX tab and set the configure the user for UNIX access: {% img right https://i.imgur.com/Ox9kuAy.png %}

- Select the NIS domain you created earlier
- Set an approprate UUID (default should be fine)
- Set the login shell as `/bin/bash`, `/bin/sh` should be fine most of the time, but I have seen a few odd things happen (details escape me)
- Set the home directory. I seperate them out from local users to something like `/home/<DOMAIN>/<username>`

Open up one of your groups (let's start with LinuxAdmin) and add the user to that group. Note you have to do it 2 places (don't blame me, I am just the messenger). Both in the standard Groups tab, but also in the UNIX attributes tab.

That should be everything on the Windows side. 

# Configure RHEL as a client
Most of the heavy lifting is done by the _System Security Service Daemon_ (SSSD).

```
yum install sssd sssd-client krb5-workstation samba openldap-clients policycoreutils-python
```

This should also pull in all the dependencies.

## Configure Kerberos

I've already said, this but I will repeat myself as getting it wrong will cause many lost hours.

- DNS must be working for both forward and reverse lookups
- Time must be in sync accross all the clients

Make sure that /etc/resolv.conf contains your domain controllers.

**Gotcha**: In RHEL/Fedora the DNS setting are defined in /etc/sysconfig/network-settings/ifcfg-eth0 (or whichever NIC comes first) by Anaconda. This will over-write /etc/resolv.conf on reboot. For no good reason other than stubbornness I tend to remove these entries and define resolv.conf myself (or via configuration management). Alternatively put DNS1 and DNS2 entries in the network configuration files.

In `/etc/krb5.conf` change you servers to point at your Domain Controllers.

```
[logging]
 default = FILE:/var/log/krb5libs.log

[libdefaults]
 default_realm = AD.EXAMPLE.COM
 dns_lookup_realm = true
 dns_lookup_kdc = true
 ticket_lifetime = 24h
 renew_lifetime = 7d
 rdns = false
 forwardable = yes

[realms]
 AD.EXAMPLE.COM = {
  # Define the server only if DNS lookups are not working
#  kdc = server.ad.example.com
#  admin_server = server.ad.example.com
 }

[domain_realm]
 .ad.example.com = AD.EXAMPLE.COM
 ad.example.com = AD.EXAMPLE.COM
```

You should now be able to run:

```
kinit aduser@AD.EXAMPLE.COM
```

That should obtain a kerberos ticket (check with `klist`) and you can move on. If it does not work fix it now - Kerberos is horrible to debug later.

## Enable LDAP Searches

The best way to bind to AD is using SASL/GSSAPI as no passwords are needed.

```
kinit Administrator@AD.EXAMPLE.COM
net ads join createupn=host/client.ad.example.com@AD.EXAMPLE.COM –k
net ads keytab create	
net ads keytab add host/client.ad.example.com@AD.EXAMPLE.COM
```

You should now be able to get information about yourself from AD using ldapsearch:
```
ldapsearch -H ldap://server.ad.example.com/ -Y GSSAPI -N -b "dc=ad,dc=example,dc=com" "(&(objectClass=user)(sAMAccountName=aduser))"
```

## Configure SSSD
Everything in SSSD revolves around a single config file (/etc/sssd/ssd.conf).

```
[sssd]
 config_file_version = 2
 domains = ad.example.com
 services = nss, pam
 debug_level = 0

[nss]

[pam]

[domain/ad.example.com]
 id_provider = ldap
 auth_provider = krb5 
 chpass_provider = krb5
 access_provider = ldap

 # To use Kerberos, un comment the next line
 #ldap_sasl_mech = GSSAPI

 # The following 3 lines bind to AD. Comment them out to use Kerberos
 ldap_default_bind_dn = CN=svc_unix,OU=useraccounts,DC=ad,DC=example,DC=com
 ldap_default_authtok_type = password
 ldap_default_authtok = Welcome_2014

 ldap_schema = rfc2307bis

 ldap_user_search_base = ,dc=ad,dc=example,dc=com
 ldap_user_object_class = user
 
 ldap_user_home_directory = unixHomeDirectory
 ldap_user_principal = userPrincipalName

 ldap_group_search_base = ou=groups,dc=ad,dc=example,dc=com
 ldap_group_object_class = group
 
 ldap_access_order = expire
 ldap_account_expire_policy = ad
 ldap_force_upper_case_realm = true

 krb5_realm = AD.EXAMPLE.COM
```

There is something wrong here. Note the lines:
```
 # To use Kerberos, un comment the next line
 #ldap_sasl_mech = GSSAPI
 
 # The following 3 lines bind to AD. Comment them out to use Kerberos
 ldap_default_bind_dn = CN=svc_unix,OU=useraccounts,DC=ad,DC=example,DC=com
 ldap_default_authtok_type = password
 ldap_default_authtok = Welcome_2014
```

Instead of doing the SASL/GSSAPI bind I would prefer to do I have chickened out and done a simple bind. Why? Because I am weak... :-(

Try with kerberos first, if it works then awesome, if not then create a service account in AD that can do nothing other than perform a search and use that to perform the bind. Make sure its path matches that of the *ldap_default_bind_dn* path, also make sure the password is more complex than "Welcome_2014".

For now this does nothing, we need to tell PAM to use it. The easiest way to enable this on RHEL is to use the authconfig command:

```
authconfig --enablesssd --enablesssdauth --enablemkhomedir –update
```

This will update `/etc/nsswitch.conf` and various files in `/etc/pam.d` to tell the system to authenticate against SSSD. SSSD will in turn talk to Active Directory, using LDAP for Identification and Kerberos for authentication.
Finally you can enable your LinuxAdmin’s to use sudo. Run the command visudo and add the line:

```
%LinuxAdmin ALL=(ALL)       ALL
# note the % sign, the defines it as a group not a user
```

Now your admin’s can run commands as root by prefacing them with sudo. For an encore, I would suggest disabling root login via SSH. Log in as your AD user (leave your root session open, just in case) and run:

```
sudo sed -i 's/PermitRootLogin no/PermitRootLogin yes/' /etc/ssh/sshd_config
sudo service sshd reload
```

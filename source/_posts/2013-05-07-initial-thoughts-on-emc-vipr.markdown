---
layout: post
title: "Initial thoughts on EMC ViPR"
date: 2013-05-07 13:32
comments: true
categories: storage
---
{% img right https://upload.wikimedia.org/wikipedia/en/8/8b/Colonial_viper_original-series.JPG  350 Colonel Viper - geddit haha%} The big announcement at this years EMC World is ViPR. Plenty of people with far bigger reputations than me in the industry have already made their comments:
<!-- more -->

-   [Chad Sakac](http://virtualgeek.typepad.com/virtual_geek/2013/05/storage-virtualization-platform-re-imagined.html) has really good and deep, but long.
-   [Chuck Hollis](http://chucksblog.emc.com/chucks_blog/2013/05/introducing-emc-vipr-a-breathtaking-approach-to-software-defined-storage.html) is nowhere near as technical but (as is normal for Chuck) sells it beautifully
-   [Scott Lowe](http://blog.scottlowe.org/2013/05/06/very-early-thoughts-about-emc-vipr/) has an excellent overview

Chad Sakac has also made a few technical introductory videos too that are linked on his article. I strongly recommend reading his article.

I am quite excited so far about ViPR, although that may be because it is new and shiney. Please note that my research is ongoing, so some of what I say may be inaccurate/just-plain-nonsense.

ViPR is EMC's response to two major storage problems:

1.   Storage is missing some sort of abstraction layer, particularly for management (the Control Plane).
1.   There is more to storage than NFS and iSCSI. As well as NAS/SAN we now have multiple forms of object stores, plus important non-POSIX file systems such as HDFS.

Another problem I would add is that of *Openness*. For now there is not really any protocols for managing multiple arrays from different manufacturers, even at a basic level. They have been attempts in the past (SMI-S), but they have never taken off. ViPR attacks that problem as well, kind 

Both southbound (data) and northbound (management) services are managed via plugins that hit the RESTful API.

<a href="http://imgur.com/OdTFVO5"><img src="http://i.imgur.com/OdTFVO5.png" title="Hosted by imgur.com"/></a>

The API on both sides is fully documented and this is what make this so exciting.

So called "Unified" systems try and answer point 2 to a certain extent. However, the tend to concentrate on giving both block and file access. What they do not do is give access the same data by more than two mechanisms. You can get block by either FC or iSCSI, or you can get to file by either CIFS or NFS. If you want to access your NFS share using a REST API, you are stuck. Likewise, the array has no knowledge of what is in your block, so you cannot access it via NFS.



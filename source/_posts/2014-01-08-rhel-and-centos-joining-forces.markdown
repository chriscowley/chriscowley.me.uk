---
layout: post
title: "RHEL and CentOS joining forces"
date: 2014-01-08 14:34
comments: true
categories: linux
---
{% img right http://i.imgur.com/3colCNj.png 200 200 %}Yesterday saw probably the biggest FLOSS news in recent times. Certainly the biggest news of 2014 so far :-) By some freak of overloaded RSS readers, I missed the announcement, but I did see this:

<blockquote class="twitter-tweet" lang="en"><p>Day 1 at the new job. Important stuff first.. Where do I get my Red Hat ?</p>&mdash; Karanbir Singh (@CentOS) <a href="https://twitter.com/CentOS/statuses/420876286785892353">January 8, 2014</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

It did not take long to dig up [this](http://community.redhat.com/centos-faq/?utm_content=buffer6403d&utm_source=buffer&utm_medium=twitter&utm_campaign=Buffer) and [this](http://lists.centos.org/pipermail/centos-announce/2014-January/020100.html), where Red Hat and CentOS respectively announce that they have joined forces. Somethings from the announcement struck me:

>  Some of us now work for Red Hat, but not RHEL

That is important! This says to me that Red Hat see the value of CentOS as an entity in itself. By not linking the CentOS developers to RHEL in anyway, they are not going to be side-tracking them. Instead, they are simple freeing them up to work more effectively on CentOS.

> we are now able to work with the Red Hat legal teams

QA was always a problem for CentOS, simply because it took place effectively in secret. Now they can just walk down the corridor to talk to the lawers who would have previously (potentially) sued them, all the potential problems go away.

# The RHEL Ecosystem

{% pullquote %}
In the beginning there is [Fedora](http://fedoraproject.org)), where the RHEL developers get to play. Here is where they can try new things and make mistakes. {"In Fedora things can break without people really worrying"} (especially in Rawhide). The exception to this is my wife as we run it on the family PC and she gets quite frustrated with its foibles. However, she knew she was marrying a geek from the outset, so I will not accept any blame for this.
{% endpullquote %}}

Periodically, the the Fedora developers will pull everything together and create a release that has the potential to be transformed into RHEL. Here they pull together all the things that have be learnt over the last few releases. I consider this an Alpha release of RHEL. At this point, behind the scences, the RHEL developers will take those packages and start work on the next release of RHEL.

{% pullquote %}
On release of RHEL, Red Hat make the source code available, as required by the terms of the GPL (and other relevant licenses).The thing is, {"Red Hat as a company are built on Open Source"} principles, they firmly believe in them and, best of all, they practise what the preach. They would still be within the letter of the law if the just dumped a bunch of apparently random scripts on a web server. Instead, they publish the SRPM packages used to build RHEL.
{% endpullquote %}

CentOS then take these sources and get to work. By definition they are always beind RHEL. As many know this got pretty bad at one point:

{% img http://www.standalone-sysadmin.com/~matt/centos-delays.jpg center %}

(Thanks to Matt Simmons, aka [Standalone Sysadmin](http://www.standalone-sysadmin.com), from whom I blatantly stole that graph, I'll ask permission later)

Since then, things have got better, with new point releases coming hot on the heels of RHEL. Certainly preparations for EL7 seemed to be going on nicely even before this announcement.

So how does this now affect the two projects then

{% img right http://i.imgur.com/qbKvXko.jpg 350 350 %}I am sure that there are few people in the community who will rue this day. Maybe they see 

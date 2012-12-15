---
layout: post
title: "Redmine on Centos with Nginx"
date: 2012-12-14 22:08
comments: true
categories: linux
---
This could have been simple, but it wasn't. There are plenty of articles out there that describe how to get Redmine working on Centos, but they all had problems.

Many were written for Apache, which I do not use. I love Apache, it has served me well, but I fancy using Nginx. No particular reason, I just do. It is my server I do what I want :)
<!-- more -->

Those that are for Nginx generally use the Passenger. This is great, but I have an existing installation which I do not want to change. With Apache, the Passenger installer just builds a module which you add to your existing install, which is great. With Nginx, it builds a whole new install of Nginx, which I did not want. So I needed to find alternative to Passenger, which are legion.

Nginix makes a brilliant load-balancer and proxy, so I went down that route. Initially I though I would just use Webrick, which is really simple. I could just proxy port 3000, job done. I tried it and it worked. Webrick is only really for testing though. It was fine for my simple needs, but I might as well do it properly.

I toyed between Thin and Mongrel, and decided to give Thin a whirl. There is an article on it on [Redmine's Wiki](http://www.redmine.org/projects/redmine/wiki/HowTo_configure_Nginx_to_run_Redmine), but I had some problems.

Initially I wanted to use just packages, but that turned out to be a no go. Using the rubygem-thin package from EPEL kept crashing. For some reason it could not load gems that I quite clearly had installed. I am not enough of a Ruby expert to fix that, but there was an alternative. For my site, I use Octopress; as such I use RVM on my workstation. I figured I would use that on my server as well.

Without further ado

'''
curl -L https://get.rvm.io | bash -s stable --rails
source /usr/local/rvm/scripts/rvm
'''

That gets your Ruby environment setup



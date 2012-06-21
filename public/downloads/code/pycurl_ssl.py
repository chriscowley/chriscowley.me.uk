#!/usr/bin/env python
downloadedFile = "/tmp/stuff"
outfile = file(downloadedFile, 'wb')
url = https://someurl.example.com
c = pycurl.Curl()
c.setopt(c.URL, url)
c.setopt(pycurl.USERPWD, "%s:%s" % (username, password))
c.setopt(c.WRITEFUNCTION, outfile.write)
c.setopt(c.SSL_VERIFYPEER, 0) # That is you key line for this purpose!
c.perform()
c.close

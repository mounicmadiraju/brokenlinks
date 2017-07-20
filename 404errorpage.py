from __future__ import print_function
import urllib2

baseURL = "https://www.jobstreet.com.my"

for n in xrange(100):
    fullURL = baseURL + str(n)
    #print fullURL
    try:
        req = urllib2.Request(fullURL)
        resp = urllib2.urlopen(req)
        if resp.getcode() == 404:
            # printing 404 error links
            print ("404 Found!")
        else:
            
            print ("URL: {0} Response: {1}".format(fullURL, resp.getcode()))
    except:
        print ("Could not connect to URL: {0} ".format(fullURL))

import urllib, urllib2, time

the_url = 'http://www.someserver.fr'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

values = {'name' : 'Michael Foord',
          'location' : 'Northampton',
          'language' : 'Python' }
headers = { 'User-Agent' : user_agent }

data = urllib.urlencode(values)
t0 = time.time()
req = urllib2.Request(the_url, data, headers)
handle = urllib2.urlopen(req)
t1 = time.time()
the_page = handle.read()
d = t1 - t0
print "Temps de chargement: %d secondes" % d
print handle.info()


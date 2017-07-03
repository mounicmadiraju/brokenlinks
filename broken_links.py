try:
    from urllib2 import urlopen, Request, HTTPError, URLError
except ImportError:
    from urllib.request import urlopen, Request, HTTPError, URLError

import signal
import threading
from bs4 import BeautifulSoup
import sys
import time

shutdown_event = None
GAME_OVER = 'game over'

def build_request(url, data=None, headers={}):
    headers['User-Agent'] = 'jobstreet'
    return Request(url, data=data, headers=headers)

def ctrl_c(signum, frame):
    global shutdown_event
    shutdown_event.set()
    raise SystemExit('\nCancelling...')

class Crawler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        file = None
        try:
            try:
                file = open('broken_link_file.txt', 'a')
            except:
                print 'Failed to open file.'

            if file != None:
                pages = self.readSiteMap()
              
	        for page in pages:
                    links = self.readHref(page)
                    if links == GAME_OVER:
                        break;

                    ret = self.crawlLinks(links, file)
                    if ret == GAME_OVER:
                        break;
        except IOError:
            print "IOError"
        finally:
            if file:
                file.close()

    def queryLinks(self, result):
        links = []
        content = ''.join(result)
        soup = BeautifulSoup(content)
        elements = soup.select('a')

        for element in elements:
            if shutdown_event.isSet():
                return GAME_OVER

            try:
                link = element.get('href')
                if link.startswith('http'):
                    links.append(link)
            except:
                print 'href error!!!'
                continue

        return links

    def readHref(self, url):
        result = []
        try:
            request = build_request(url)
            f = urlopen(request, timeout=3)
            while 1 and not shutdown_event.isSet():
                tmp = f.read(10240)
                if len(tmp) == 0:
                    break
                else:
                    result.append(tmp)

            f.close()
        except HTTPError, URLError:
            print URLError.code

        if shutdown_event.isSet():
            return GAME_OVER

        return self.queryLinks(result)

    def readSiteMap(self):
        pages = []
        try:
            # f = urlopen("https://www.jobstreet.com.my/career-resources/page-sitemap.xml")
            request = build_request("https://www.jobstreet.com.my/career-resources/page-sitemap.xml")
            f = urlopen(request, timeout=3)
            xml = f.read()

            soup = BeautifulSoup(xml)
            urlTags = soup.find_all("url")

            print "The number of url tags in sitemap: ", str(len(urlTags))

            for sitemap in urlTags:
                link = sitemap.findNext("loc").text
                pages.append(link)

            f.close()
        except HTTPError, URLError:
            print URLError.code

        return pages

    def crawlLinks(self, links, file=None):
        for link in links:
            if shutdown_event.isSet():
                return GAME_OVER

            status_code = 0

            try:
                request = build_request(link)
                f = urlopen(request)
                status_code = f.code
                f.close()
            except HTTPError, URLError:
                status_code = URLError.code

            if status_code == 404:
                if file != None:
                    file.write(link + '\n')

            print str(status_code), ':', link

        return GAME_OVER

def crawlPages():
    global shutdown_event
    shutdown_event = threading.Event()

    signal.signal(signal.SIGINT, ctrl_c)

    crawler = Crawler()
    crawler.start()
    while crawler.isAlive():
        crawler.join(timeout=0.1)

    print GAME_OVER

def main():
    try:
        crawlPages()
    except KeyboardInterrupt:
        print_('\nKeyboardInterrupt')

if __name__ == '__main__':
    main()

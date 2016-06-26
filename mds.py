import os
import urllib2
from bs4 import BeautifulSoup
import pdb

####CHANGE ME#####
listingurl = "http://mds-club.ru/cgi-bin/index.cgi?r=84&lang=rus&filter=0&article=0&sortby=21&posits=0&search="
##################
u = urllib2.urlopen(listingurl)
listhtml = u.read()
u.close()
listsoup = BeautifulSoup(''.join(listhtml))
listtable = listsoup.find('div',id="catalogtable").find('table')
listrows = listtable.findAll("tr", { "class" : "w" })
for tr in listrows:
    cols = tr.findAll('td')
    id = cols[0].find(text=True)
    recordurl = cols[0].find('a')['href']
    
    
    #get a page for the record
    u = urllib2.urlopen(recordurl)
    rechtml = u.read()
    u.close()
    recsoup = BeautifulSoup(''.join(rechtml))
    recrows = recsoup.findAll("tr", { "class" : "w" })
    
    #find working link by checking if headers look ok
    meta_len = 0
    col = 0
    while meta_len == 0:
        cols = recrows[col].findAll('td')
        mp3url = cols[3].find('a')['href']
        url = mp3url

        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        meta = u.info()
        meta_len = len(meta.getheaders("Content-Length"))
        col = col + 1
        
    #download mp3
    if os.path.isfile(id + " - " + file_name) == False:
        f = open(id + " - " + file_name, 'wb')
        
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (id + " - " + file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()

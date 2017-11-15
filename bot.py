import html2text
import urllib2

import sys
reload(sys)
sys.setdefaultencoding("UTF8")


def MapGatherDocsAndUrls():
    return ["https://en.wikipedia.org/wiki/Conflict_in_the_Niger_Delta"]

def MapOpenDoc(doc):
    rawhtmltext = urllib2.urlopen(doc).read().decode('utf8')
    ''.join(e for e in rawhtmltext if e.isalnum())
    h = html2text.HTML2Text()
    return h.handle(rawhtmltext)

def MapSentanceMap():
    i=0

def MapUploadToDatabase():
    i=0

def MapVisualize():
    i=0

def MapNetwork():
    doclist = MapGatherDocsAndUrls()

    for doc in doclist:
        doctext = MapOpenDoc(doc)
        doctext = doctext.split(".")
        for sentence in doctext:
            print sentence

MapNetwork()




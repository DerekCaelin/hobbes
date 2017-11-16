import html2text
import urllib2
import spacy
from nltk import tokenize

import sys
reload(sys)
sys.setdefaultencoding("UTF8")


def MapGatherDocsAndUrls():
    return ["https://www.washingtonpost.com/news/monkey-cage/wp/2017/11/15/to-understand-the-coup-in-zimbabwe-you-need-to-know-more-about-grace-mugabe/"]

def MapOpenDoc(doc):
    rawhtmltext = urllib2.urlopen(doc).read().decode('utf8')
    ''.join(e for e in rawhtmltext if e.isalnum())
    h = html2text.HTML2Text()
    return h.handle(rawhtmltext)

def MapSentenceMap(sentence):
    nlp = spacy.load('en')
    sentence = nlp(sentence)

    gotsubjnoun = False
    gotverb = False
    gotdirectobject = False

    subjnoun1 = ""
    verb = ""
    directobject1 = ""
    directobject2 = ""

    print ("processing: "+str(sentence))

    for word in sentence:

        if word.dep_ == "nsubj" and word.pos_ == "PROPN":
            gotsubjnoun = True
            if subjnoun1 == "":
                subjnoun1 = word.text
        if word.dep_ == "ROOT":
            gotverb = True
            if verb == "":
                verb = word.text
        if word.dep_ == "dobj" and (word.pos_ == "PROPN"):
            gotdirectobject = True
            if directobject1 == "":
                directobject1 = word.text

    if gotsubjnoun == True and gotverb == True and gotdirectobject == True:
        print("found")
        sentencepackage = {"subjnoun1" : subjnoun1,
                           "verb" : verb,
                           "directobject1" : directobject1}
        print (sentencepackage)


def MapUploadToDatabase():
    i=0

def MapVisualize():
    i=0

def MapNetwork():
    doclist = MapGatherDocsAndUrls()

    for doc in doclist:
        doctext = MapOpenDoc(doc)
        doctext = tokenize.sent_tokenize(doctext)
        for sentence in doctext:
            MapSentenceMap(sentence)

MapNetwork()




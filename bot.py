import html2text
import urllib2
import spacy
from nltk import tokenize

import sys
reload(sys)
sys.setdefaultencoding("UTF8")

import requests
import random


def MapGatherDocsAndUrls():
    return ["https://www.washingtonpost.com/news/monkey-cage/wpc/2017/11/15/to-understand-the-coup-in-zimbabwe-you-need-to-know-more-about-grace-mugabe/"]

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

#11/25/17 - imported this function from peacetechbot, rework to declare protests in recent timeframe
def VisualizeACLED(queryword, replytweet):
    print("Checking ACLED")
    try:
        # get ACLED data
        url = "https://api.acleddata.com/acled/read.csv"
        response = requests.get(url)
        data = pd.read_csv(url)
        countrycol = data.loc[:, "country"]
        dates = data.loc[:, "event_date"]

        # select country
        countries = list(set(countrycol))
        if queryword == "random":
            country = random.choice(countries)
        else:
            country = queryword.title()

        # get data from country
        countrydatafull = data[data['country'] == country]
        total_events = len(countrydatafull)

        # contingencies
        if replytweet == False and total_events == 0:
            VisualizeACLED(queryword, replytweet)
        if replytweet == True and total_events == 0:
            print ("no acled data for " + queryword)
        else:
            # get dates
            cdates = sorted(list(set(countrydatafull.loc[:, "event_date"])))
            dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in cdates]
            first_date = dates_list[0]
            last_date = dates_list[len(dates_list) - 1]
            final_dates = []

            # if acledupdated recently
            timesinceupdate = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), '%Y-%m-%d').date() - last_date
            print(timesinceupdate.days)

            if timesinceupdate.days <= 3 and replytweet == False:

                delta = last_date - first_date
                for i in range(delta.days + 1):
                    final_dates.append(first_date + timedelta(days=i))

                eventcount = []

                # get events per date
                for date in cdates:
                    thing = list(countrydatafull.loc[:, "event_date"]).count(date)
                    eventcount.append(thing)

                # get event types
                ceventtypes = sorted(list(set(countrydatafull.loc[:, "event_type"])))
                print(ceventtypes)

                datelists = []
                graphcount = 0
                colors = ["#223451", "#4b6896", "#394559", "#10397c", "#04193d", "#839cc6", "#393c42", "#000000"]

                # pre format chart
                fig, ax = plt.subplots()
                plt.title("Recent ACLED Events: " + country)

                # getdata
                for ceventtype in ceventtypes:

                    # get date of eventtype
                    selcountrydatafull = countrydatafull[countrydatafull['event_type'] == ceventtype]
                    datetocheckstr = list(selcountrydatafull.loc[:, "event_date"])
                    datetocheckdt = [datetime.strptime(date, '%Y-%m-%d').date() for date in datetocheckstr]

                    # get events per date
                    ceventcounts = []
                    for date in final_dates:
                        thing = datetocheckdt.count(date)
                        ceventcounts.append(thing)

                    # make a list of dates
                    datelists.append(ceventcounts)

                # Visualize
                sumdatelist = []
                graphs = []
                for date in datelists[0]:
                    sumdatelist.append(0)
                for datelist in datelists:
                    graph = plt.bar(final_dates, datelist, color=colors[graphcount], bottom=sumdatelist)
                    graphs.append(graph)
                    sumdatelist = np.add(datelist, sumdatelist)
                    graphcount += 1

                # post viz formatting
                ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
                ax.set_ylim(ymin=0)
                ax.set_xlabel('Date')
                ax.set_ylabel('Events')
                plt.gcf().subplots_adjust(bottom=0.15)
                plt.xticks(rotation=15)
                plt.legend((graphs), (ceventtypes), fancybox=True, framealpha=0.5)
                # ax.legend(loc='best', fancybox=True, framealpha=0.5)
                plt.savefig("chart.png")

                # create status and share
                if (first_date != last_date):
                    status = "Between " + str(first_date) + " and " + str(last_date) + ", there were " + str(
                        total_events) + " protests or violent events in " + country + ". #ACLED #conflict #peacetech"
                if (first_date == last_date):
                    if total_events == 1:
                        status = "On " + str(
                            first_date) + ", there was a protest or violent event in " + country + ". #ACLED #conflict #peacetech"
                    if total_events > 1:
                        status = "On " + str(first_date) + ", there were " + str(
                            total_events) + " protests or violent events in " + country + ". #ACLED #conflict #peacetech"
                print(status)
                if replytweet == True:
                    tweetid = GetMyMostRecentTweet()
                    print(status)
                    api.update_with_media("chart.png", status=status, in_reply_to_status_id=tweetid)
                    os.remove("chart.png")
                else:
                    print(status)
                    api.update_with_media("chart.png", status=status)
                    os.remove("chart.png")
    except:


print("error doing acled")

MapNetwork()




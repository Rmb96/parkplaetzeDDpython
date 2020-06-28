import requests
import lxml.html as html
from pprint import pprint
from bs4 import BeautifulSoup

class Parkplatz:
    def __init__(self, url = 'https://www.dresden.de/apps_ext/ParkplatzApp/index'):
        self.url = url
    def getdata(self):
        resp = requests.get(self.url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        return resp.content

    def gettablev1(self):
        resp = requests.get(self.url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        #print(resp.content) print the full site
        doc = html.fromstring(resp.content) #parse html
        tr_elements = doc.xpath('//tr') # find all tables
        #pprint(tr_elements[1].text_content())
        #pprint(tr_elements[2].text_content())
        #pprint(dir(tr_elements[2]))
        #pprint(tr_elements[2].classes)
        resultdata = []
        for i in range(1, len(tr_elements)):
            tmp = tr_elements[i].text_content()
            tmp = tmp.replace(" \n", "")
            tmp = tmp.replace("  ", "")
            tmp = tmp.split("\n")
            del tmp[0]
            del tmp[(len(tmp)-1)]
            if len(tmp) > 4:
                #print(str(len(tmp))+":"+str(i))
                #pprint(tmp)
                resultdata.append([tmp[0],tmp[2],tmp[4]])
        return(resultdata)
            # example  p1 = Parkplatz()  pprint(p1.getdata())
    def gettablev2(self):
        return  self.get_tables(self.getdata())

    def makelist(self,table):
        result = []
        allrows = table.findAll('tr')
        for row in allrows:
            result.append([])
            allcols = row.findAll('td')
            for col in allcols:
                thestrings = [unicode(s) for s in col.findAll(text=True)]
                thetext = ''.join(thestrings)
                result[-1].append(thetext)
        return result

    def get_tables(self, htmldoc):
        soup = BeautifulSoup(htmldoc)
        return soup.findAll('table')

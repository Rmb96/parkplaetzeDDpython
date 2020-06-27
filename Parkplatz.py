import requests
import lxml.html as html
import pandas as pd
from pprint import pprint

class Parkplatz:
    def __init__(self, url = 'https://www.dresden.de/apps_ext/ParkplatzApp/index'):
        self.url = url
    def getdata(self):
        resp = requests.get(self.url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        #print(resp.content) print the full site
        doc = html.fromstring(resp.content) #parse html
        tr_elements = doc.xpath('//tr') # find all tables
        #pprint(tr_elements[0].text_content())
        #pprint(tr_elements[2].text_content())
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

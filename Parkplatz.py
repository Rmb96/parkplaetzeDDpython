import requests
import lxml.html
from pprint import pprint
#from bs4 import BeautifulSoup
import pandas as pd

class Parkplatz:
    def __init__(self, url = 'https://www.dresden.de/apps_ext/ParkplatzApp/index'):
        self.url = url
    def getdata(self):
        resp = requests.get(self.url)
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        #print(resp.content) print the full site
        return resp

    def gettablev1(self):
        doc = lxml.html.fromstring(self.getdata().content) #parse html
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
            
    def gettablev2(self):
        return  self.makelist(self.getdata())

    def makelist(self,html):
        df_list = pd.read_html(html.text) # this parses all the tables in webpages to a list
        for i in range(1,len(df_list)):
            df_list[i].columns = ['id','Ort', 'Stellplätze', 'frei']
            df_list[i].drop(columns=['id'])
            #pprint(df_list[i]["Stellplätze"])
            #pprint(df_list[i])
        df = df_list[1]
        mydfs=[df]
        for i in range(2,len(df_list)):
            mydfs.append(df_list[i])
        df = pd.concat(mydfs)
        df.pop('id') # remove id line
        df['Stellplätze'] = df['Stellplätze'].str.replace('Stellplätze', '')
        df['frei'] = df['frei'].str.replace('frei', '')
        df['Stellplätze'] = pd.to_numeric(df['Stellplätze'])
        df['frei'] = pd.to_numeric(df['frei'])
        #df = pd.concat(df_list[1])
        return df;

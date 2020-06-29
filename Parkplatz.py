import requests
from pprint import pprint
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

    def gettable(self):
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

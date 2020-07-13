import joblib
from datetime import timedelta
import pandas as pd
import numpy as np
import requests
from datetime import datetime

def lockdown():
    try:
        today=datetime.today().strftime('%d-%m-%Y')
        s_date=datetime.strptime('03-07-2020','%d-%m-%Y')
        e_date=datetime.strptime(today,'%d-%m-%Y')
        dates=pd.date_range(s_date,e_date,freq='d')
        case_dates=[]
        for d in dates:
            d1 = d - timedelta(days=2)
            d2=d1.strftime('%d-%m-%Y')
            case_dates.append(d2)
        x= requests.get('https://api.covid19india.org/data.json')
        data_stats = x.json()
        data = data_stats["cases_time_series"]
        confirmed=[]
        active=[]
        death=[]
        recovered=[]
        date=[]
        print(case_dates)
        for i in data:
            confirmed.append(i["dailyconfirmed"])
            death.append(i["dailydeceased"])
            recovered.append(i["dailyrecovered"])
            date.append(i["date"])
            activee=int(i["dailyconfirmed"])-(int(i["dailydeceased"])+int(i["dailyrecovered"]))
            active.append(activee)
        cases=pd.DataFrame()
        cases['date']=date
        cases['confirmed']=confirmed
        cases['active']=active
        cases['death']=death
        cases['recovered']=recovered

        cdates=[]
        for d in cases['date']:
            d1=d.strip()+' 2020'
            d2=datetime.strptime(d1,'%d %B %Y').strftime('%d-%m-%Y')
            cdates.append(d2)
        cases['date']=cdates
        cases1=cases[cases['date'].isin(case_dates)]
        
        gbr=joblib.load('grad.sav')
        y=gbr.predict(cases1.iloc[:,[1,2,3,4]])
        output=pd.DataFrame()
        output['case_date']=cases1['date']
        output['confirmed']=cases1['confirmed']
        output['active']=cases1['active']
        output['death']=cases1['death']
        output['recovered']=cases1['recovered']

        fd=[]
        for i in range(len(dates)):
            d=dates[i]
            d1=d.strftime('%d-%m-%Y')
            fd.append(d1)
            
        output['sentiment_date']=fd
        output['sentiment_score']=y
        output=output.reset_index(drop=True)
        output.to_csv('lockdown.csv',index=False)
        
    except Exception as e:
        print(e)


if __name__ == '__main__':
    lockdown()

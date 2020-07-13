import pandas as pd
import requests,json
from pandas import DataFrame
x= requests.get('https://api.covid19india.org/data.json')
data_stats = x.json()
data = data_stats["cases_time_series"]
confirmed=[]
active=[]
death=[]
recovered=[]
date=[]
for i in data:
    confirmed.append(i["dailyconfirmed"])
    death.append(i["dailydeceased"])
    recovered.append(i["dailyrecovered"])
    date.append(i["date"])
    activee=int(i["dailyconfirmed"])-(int(i["dailydeceased"])+int(i["dailyrecovered"]))
    active.append(activee)
confirmed=DataFrame(confirmed,columns=['Confirmed'])
active=DataFrame(active,columns=['Active'])
death=DataFrame(death,columns=['Death'])
recovered=DataFrame(recovered,columns=['Recovered'])
date=DataFrame(date,columns=['Date'])
pd.concat([date,confirmed,active,death,recovered],sort=False,axis=1).to_csv(r"cases.csv")


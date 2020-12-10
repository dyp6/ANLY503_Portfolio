#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 20:33:59 2020

@author: postd
"""
import pandas as pd
import requests
import matplotlib.pyplot as plt

URL = 'https://acleddata.com/download/22846/'
output_path = '/Users/postd/Documents/ANLY503_Project/acled_events.xlsx'
r = requests.get(URL)

output = open(output_path,'wb')
output.write(r.content)
output.close()

acled = pd.read_excel(output_path,sheet_name="Sheet1")
drop = ["ISO","EVENT_ID_CNTY","EVENT_ID_NO_CNTY","YEAR",
        "TIME_PRECISION","REGION","COUNTRY","GEO_PRECISION",
        "SOURCE_SCALE","ADMIN3"]

acled = acled.drop(columns=drop)
EventFreqs = acled.groupby(["EVENT_TYPE","SUB_EVENT_TYPE"]).size()\
    .reset_index()
InterFreqs = acled.groupby(["INTER1","INTER2"]).size().reset_index()
Actor1Freqs = acled.groupby(["ACTOR1","ASSOC_ACTOR_1"]).size().reset_index()
Actor2Freqs = acled.groupby(["ACTOR2","ASSOC_ACTOR_2"]).size().reset_index()

ActorPairFreqs = acled.groupby(["ACTOR1","ACTOR2"]).size().reset_index()

def stackedEventBar(EventDF,ev_type):
    EventDF =EventDF.sort_values(by=0).reset_index(drop=True)

    eventCol = EventDF.loc[EventDF.EVENT_TYPE==ev_type,
                          "SUB_EVENT_TYPE"].unique()
    colors = ["#440154FF","#3B528BFF","#21908CFF","#5DC863FF","#FDE725FF"]
    fig, ax = plt.subplots(1)
    for i in range(len(eventCol)):
        if i == 0:
            ax.bar(1,EventDF.loc[EventDF.SUB_EVENT_TYPE==eventCol[i],0],
               color = colors[i],label=eventCol[i],
                    width = 0.2)
        else:
            ax.bar(1,EventDF.loc[EventDF.SUB_EVENT_TYPE==eventCol[i],0],
                width = 0.2,
                color = colors[i],label=eventCol[i],
                bottom =EventDF\
                    .loc[EventDF.SUB_EVENT_TYPE==eventCol[i-1],0])
    ax.legend(fontsize=9)
    fig.suptitle("Events: "+ev_type,fontsize=16,fontfamily="serif")
    fig.patch.set_facecolor("#FFFBF0")
    ax.set_facecolor("#FBF0FF")
    ax.set_ylabel("Frequency",fontfamily="serif",fontsize=11)
    ax.set_xlabel(ev_type,fontfamily="serif",fontsize=11)
    ax.set_xticklabels("")
    ax.set_xticks([])
    return fig

Pfig = stackedEventBar(EventFreqs,"Protests")
Vfig=stackedEventBar(EventFreqs,"Violence against civilians")
Sfig = stackedEventBar(EventFreqs,"Strategic developments")
Rfig = stackedEventBar(EventFreqs,"Riots")
Bfig = stackedEventBar(EventFreqs,"Battles")
Pfig.savefig("/Users/postd/Documents/ANLY503_Project/ProtestsBar.png")
Vfig.savefig("/Users/postd/Documents/ANLY503_Project/VacBar.png")
Sfig.savefig("/Users/postd/Documents/ANLY503_Project/StDevBar.png")
Rfig.savefig("/Users/postd/Documents/ANLY503_Project/RiotsBar.png")
Bfig.savefig("/Users/postd/Documents/ANLY503_Project/BattlesBar.png")

# Inter Codes:
# 1: State Forces, 2: Rebel Groups, 3: Political Militias, 
# 4: Identity Militias, 5: Rioters, 6: Protestors,
# 7: Civilians, 8: External/Other Forces

EvntTyps = acled.groupby(["EVENT_DATE","EVENT_TYPE"]).size().reset_index()
start = min(acled.EVENT_DATE)
end = max(acled.EVENT_DATE)

dailyDates = [[start + pd.Timedelta(days=i)]*5 \
              for i in range((end - start).days)]
dailyDates = [x for y in dailyDates for x in y]
events = ["Protests","Battles","Riots",
          "Violence against civilians","Strategic developments"]
events = [x for y in [events] * int(len(dailyDates)/5) for x in y]
numEvents = []
for i in range(len(events)):
    if [x for x in EvntTyps.loc[(EvntTyps.EVENT_DATE==dailyDates[i])\
                    &(EvntTyps.EVENT_TYPE==events[i]),0].values]:
        [numEvents.append(x) for x in EvntTyps.\
                     loc[(EvntTyps.EVENT_DATE==dailyDates[i])\
                         &(EvntTyps.EVENT_TYPE==events[i]),0].values]
    else:
        numEvents.append(0)
        
protEvents = numEvents[0::5]
BatEvnts = numEvents[1::5]
riotEvnts = numEvents[2::5]
vacEvnts = numEvents[3::5]
sdEvnts = numEvents[4::5]
daily = [pd.to_datetime(x).date() for x in pd.Series(dailyDates).unique()]
typesMag = pd.DataFrame(dict(date = daily,Protests=protEvents,
                             Battles=BatEvnts,Riots=riotEvnts,
                             VAC=vacEvnts,SD=sdEvnts))

typesMag['Date'] = pd.to_datetime(typesMag['date']) - pd.to_timedelta(7, unit='d')
df = typesMag.groupby([pd.Grouper(key='Date', freq='W-MON')])\
       .sum()\
       .reset_index()\
       .sort_values('Date')

fig2, ax2 = plt.subplots(3,figsize=(10,12))
fig2.patch.set_facecolor("#FFFBF0")
ax2[0].plot(df.Date,df.Protests,label="Protests",color="#440154FF",linewidth=3)
ax2[0].axvspan(pd.to_datetime("2020-05-25"),pd.to_datetime("2020-06-08"),
               color="red",alpha=0.15)
ax2[0].set_ylim(0,4000)
ax2[0].set_ylabel("Frequency",fontsize=12,fontfamily="serif")
ax2[0].annotate("George Floyd's\nDeath (5/25)",(pd.to_datetime("2020-05-25"),3200),
                textcoords="offset points",xytext=(0,10),ha='center',
                fontweight="bold",fontfamily="serif")
ax2[0].legend()
ax2[0].set_facecolor("#FBF0FF")
ax2[1].plot(df.Date,df.Riots,label="Riots",
            color="#440154FF",linewidth=3)
ax2[1].plot(df.Date,df.SD,label="Strategic developments",
            color="#5DC863FF",linewidth=3)
ax2[1].axvspan(pd.to_datetime("2020-05-25"),pd.to_datetime("2020-06-08"),
               color="red",alpha=0.15)
ax2[1].set_ylabel("Frequency",fontsize=12,fontfamily="serif")
ax2[1].legend()
ax2[1].set_facecolor("#FBF0FF")
ax2[2].plot(df.Date,df.VAC,label="Violence against civilians",
            color="#440154FF",linewidth=3)
ax2[2].plot(df.Date,df.Battles,label="Battles",
            color="#5DC863FF",linewidth=3)
ax2[2].axvspan(pd.to_datetime("2020-05-25"),pd.to_datetime("2020-06-08"),
               color="red",alpha=0.15)
ax2[2].set_ylabel("Frequency",fontsize=12,fontfamily="serif")
ax2[2].legend()
ax2[2].set_facecolor("#FBF0FF")
fig2.suptitle("Frequency of Events by Category (Weekly)",
              fontsize=20,fontfamily="serif",y = 0.92)

fig2.savefig("/Users/postd/Documents/ANLY503_Project/EventsLines.png")
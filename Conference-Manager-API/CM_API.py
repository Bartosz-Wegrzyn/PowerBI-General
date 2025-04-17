""" 
    How to run:
    
    Execute "python CM_API.py" with optional atguments:
    
        Parameters: 

            -y {int} Event Start Date Year. From 2018 to current year. Pass for all. 
            -u {str} Business Unit 'Account1_ID' or 'Account2_ID'. Pass for both. 
            -f {str} Save format:  'csv' or 'excel'. Pass for .csv

        Examples:
            python CM_API.py   -  Refresh all dataset (Priopably won't work due to HTTP 400 or 401 or 408) 
            python CM_API.py -u 'Account1_ID' -  Refresh Account1_Country data (Priopably won't work due to HTTP 400 or 401 or 408)
            python CM_API.py -y 2024 # Get 2024 data
            
   Content:
        # 0. Preperation
            ## 0.1 Packages imports
            ## 0.2 CM Settings
            ## 0.3 Passwords Imports
            ## 0.4 Definitions
                ### 0.4.1 Get Account1_ID token
                ### 0.4.2 Get Events List. Aka d_Events
                ### 0.4.3 Get Participants List. Aka f_Participants
                ### 0.4.4 Get Participant_Categories List. Aka f_Participant_Categories
        
        Main:
        # 1. Get Data
            ## 1.1 Get Account1_ID 
                ### 1.1.2 Participants 
                ### 1.1.3 Participants Categories
            ## 1.2 Get Account2_ID 
                ### 1.1.1 Events
                ### 1.1.2 Participants 
                ### 1.1.3 Participants Categories 
        
        # 2. Concat 
        
        # 3. Save 
        
    Output:
        Naming convention:
            "d_Events"                  & (".csv", ".xlsx")
            "f_Participants"            & (".csv", ".xlsx")
            "d_Participants_Categories" & (".csv", ".xlsx")
            
"""
# 0. Preperation
## 0.1 Packages imports
import json
import requests
import pandas as pd
import html
import warnings
from tqdm import tqdm
warnings.simplefilter(action='ignore', category=FutureWarning)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-y","--Year")
parser.add_argument("-u","--Unit")   # -u {str} Business Unit 'Account1_ID' or 'Account2_ID'. Pass for both.
parser.add_argument("-f","--Format") # -f {str} Save format. csv/exc. Pass for .csv
args = parser.parse_args()


## 0.2 CM Settings
max_rows = (2**31)-1
CompanyID_Account1_ID = "CompanyID_Account1_ID"
CompanyID_Account2_ID = "CompanyID_Account2_ID"

## 0.3 Passwords Imports
Secret_Account1_ID =  {
"username": "Account1_ID",
"password": "Account1_Password"
}
Secret_Account2_ID = {
"username": "Account2_ID",
"password": "Account2_Password"
}

## 0.4 Definitions
### 0.4.1 Get Account1_ID token
def Get_API_Token(CompanyID, Secret):
    URL = f"https://{CompanyID}.cmapi.io/v1/auth/"
    headers = { "accept": "application/json", "Content-Type": "application/json"}
    resp = requests.post(URL, headers = headers ,data=json.dumps(Secret))
    token = resp.json()['token']
    return token


### 0.4.2 Get Events List. Aka d_Events
def GET_Events(CompanyID, Token):
    URL = f'https://{CompanyID}.cmapi.io/v1/events?limit={max_rows}'
    header = {
        "authorization": f"{Token}", 
        "accept": "application/json",
        "Content-Type": "application/json"}

    resp1 = requests.get(URL, headers=header, timeout=1200)
    resp2 = pd.DataFrame.from_dict(resp1.json())
    Events = (pd.DataFrame(resp2['events'].values.tolist()))

    out =  pd.DataFrame(Events)
    websiteMetadata = pd.DataFrame(Events)
    websiteMetadata_Inside = pd.DataFrame(websiteMetadata['websiteMetadata'].values.tolist())
    out= out.join(websiteMetadata_Inside.add_prefix("websiteMetadata."))
    eventLocation = pd.DataFrame(websiteMetadata)
    eventLocation_Inside = pd.DataFrame(eventLocation['eventLocation'].values.tolist())
    out= out.join(eventLocation_Inside.add_prefix("eventLocation."))
    eventOrganizer = pd.DataFrame(eventLocation)
    eventOrganizer_Inside = pd.DataFrame(eventOrganizer['eventOrganizer'].values.tolist())
    out= out.join(eventOrganizer_Inside.add_prefix("eventOrganizer."))
    del out['eventLocation']
    del out['websiteMetadata']
    del out['eventOrganizer']
    out["eventOrganizer.city"] = out["eventOrganizer.city"].apply(lambda x: html.unescape(str(x)))
    out["eventLocation.address"] = out["eventLocation.address"].apply(lambda x: html.unescape(str(x)))
    out["eventLocation.city"] = out["eventLocation.city"].apply(lambda x: html.unescape(str(x)))
    out["eventOrganizer.address"] = out["eventOrganizer.address"].apply(lambda x: html.unescape(str(x)))
    out["eventName"] = out["eventName"].apply(lambda x: html.unescape(str(x)))
    out["websiteMetadata.title"] = out["websiteMetadata.title"].apply(lambda x: html.unescape(str(x)))
    out["eventName"] = out["eventName"].apply(lambda x: html.unescape(str(x)))

    return out


### 0.4.3 Get Participants List. Aka f_Participants
def GET_Participants(CompanyID, Token, EventsList):
    header = {
    "authorization": f"{Token}", 
    "accept": "application/json",
    "Content-Type": "application/json"}
    
    Participants = pd.DataFrame()

    for eventID, i in zip(EventsList, tqdm(range(len(EventsList)-1))):
        url = f'https://{CompanyID}.cmapi.io/v1/participants/event/{eventID}?extended=false'
        participants_resp1 = requests.get(url, headers=header, timeout=None)
        if(str(participants_resp1) != "<Response [200]>"):
            print(participants_resp1, eventID)
            continue
            
        participants_resp2 = pd.DataFrame.from_dict(participants_resp1.json())
        
        if participants_resp2.empty:
            continue
        else:
            Participants = Participants.append(pd.DataFrame(participants_resp2['participants'].values.tolist()))

    return Participants

### 0.4.4 Get Participant_Categories List. Aka f_Participant_Categories
def GET_Participant_Categories(CompanyID,Token):
    URL = f'https://{CompanyID}.cmapi.io/v1/participantcategories?'
    header = {
    "authorization": f"{Token}", 
    "accept": "application/json",
    "Content-Type": "application/json"}
    resp1 = requests.get(URL, headers=header, timeout=None)
    resp2 = pd.DataFrame.from_dict(resp1.json())
    out = (pd.DataFrame(resp2['categories'].values.tolist()))
    return out

if __name__ == "__main__":

    # 1. Get Data
    ## 1.1 Get Account1_ID 
    if args.Unit == None or args.Unit == "Account1_ID":
        print("Downloading Account1_ID data")

        Token_Account1_ID = Get_API_Token(CompanyID_Account1_ID, Secret_Account1_ID)
        print(" Account1_ID API token collected.")

        print(" Collecting Events..")
        d_Events_Account1_ID = GET_Events(CompanyID_Account1_ID, Token_Account1_ID)
        d_Events_Account1_ID["Source"] = "Account1_Country"

        if args.Year != None:
            EventIDs_Account1_ID = d_Events_Account1_ID[d_Events_Account1_ID['eventStartTS'].str.startswith(args.Year)==True]['eventID'] 
        else:
            EventIDs_Account1_ID = d_Events_Account1_ID['eventID'] 
        print(" Collecting Participants from", len(EventIDs_Account1_ID), "events..")
        f_Participants_Account1_ID = GET_Participants(CompanyID_Account1_ID, Token_Account1_ID, EventIDs_Account1_ID)
        f_Participants_Account1_ID["Source"] = "Account1_Country"    
        print(" ", len(f_Participants_Account1_ID), "participants collected")

        print(" Collecting Participants Categories..")
        d_Participants_Categories_Account1_ID =  GET_Participant_Categories(CompanyID_Account1_ID,Token_Account1_ID)
        d_Participants_Categories_Account1_ID["Source"] = "Account1_Country"
        print(" Participants Categories collected")

    ## 1.2 Get Account2_ID 
    if args.Unit == None or args.Unit == "Account2_ID":
        print("Downloading Account2_ID data")

        Token_Account2_ID = Get_API_Token(CompanyID_Account2_ID, Secret_Account2_ID)
        print(" Account2_ID API token collected.")

        print(" Collecting Events..")
        d_Events_Account2_ID = GET_Events(CompanyID_Account2_ID, Token_Account2_ID)
        d_Events_Account2_ID["Source"] = "Account2_Country"

        if args.Year != None:
            EventIDs_Account2_ID = d_Events_Account2_ID[d_Events_Account2_ID['eventStartTS'].str.startswith(args.Year)==True]['eventID'] 
        else:
            EventIDs_Account2_ID = d_Events_Account2_ID['eventID'] 
        print(" Collecting Participants from", len(EventIDs_Account2_ID), "events..")

        f_Participants_Account2_ID = GET_Participants(CompanyID_Account2_ID, Token_Account2_ID, EventIDs_Account2_ID)
        f_Participants_Account2_ID["Source"] = "Account2_Country"    
        print(" ", len(f_Participants_Account2_ID), "participants collected")

        print(" Collecting Participants Categories..")
        d_Participants_Categories_Account2_ID =  GET_Participant_Categories(CompanyID_Account2_ID,Token_Account2_ID)
        d_Participants_Categories_Account2_ID["Source"] = "Account2_Country"
        print(" Participants Categories collected")

    # 2. Concat 
    if args.Unit == None:
        print("Concat Events..")
        d_Events = pd.concat([d_Events_Account2_ID, d_Events_Account1_ID]).reset_index(drop=True)
        
        print("Concat Participants..")
        f_Participants = pd.concat([f_Participants_Account2_ID, f_Participants_Account1_ID]).reset_index(drop=True)
        
        print("Concat Participants Categories")
        d_Participants_Categories = pd.concat([d_Participants_Categories_Account2_ID, d_Participants_Categories_Account1_ID]).reset_index(drop=True)

    elif args.Unit == "Account1_ID":
        d_Events = d_Events_Account1_ID
        f_Participants = f_Participants_Account1_ID
        d_Participants_Categories = d_Participants_Categories_Account1_ID

    elif args.Unit == "Account2_ID":
        d_Events = d_Events_Account2_ID
        f_Participants = f_Participants_Account2_ID
        d_Participants_Categories = d_Participants_Categories_Account2_ID

    # 3. Save 
    folder = "All" if args.Year==None else args.Year
    if args.Format == None or args.Format == 'excel':
        d_Events.to_excel(f"{folder}/d_Events.xlsx")
        print("d_Events saved to Excel, Len:", len(d_Events))

        f_Participants.to_excel(f"{folder}/f_Participants.xlsx")
        print("f_Participants saved to Excel, Len:", len(f_Participants))

        d_Participants_Categories.to_excel(f"{folder}/d_Participants_Categories.xlsx")
        print("d_Participants_Categories saved to Excel, Len:", len(d_Participants_Categories))

    elif args.Format == 'csv':
        d_Events.to_csv(f"{folder}/d_Events.csv")
        print("d_Events saved to CSV, Len:", len(d_Events))

        f_Participants.to_csv(f"{folder}/f_Participants.csv")
        print("f_Participants saved to CSV, Len:", len(f_Participants))

        d_Participants_Categories.to_csv(f"{folder}/d_Participants_Categories.csv")
        print("d_Participants_Categories saved to CSV, Len:", len(d_Participants_Categories))

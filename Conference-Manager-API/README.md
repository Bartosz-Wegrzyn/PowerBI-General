# Why

This code was written because the CM API is extremely slow — downloading anything in the standard way is nearly impossible, and numerous errors occur. Even though the files are technically very small, the download process, based on the data I tested, takes around 40 minutes.

# Introduction 

This code is based on Conference Manager - API 1.0.6

It can by used for 1 or 2 accounts \
Account1 = "Account1_ID" \
Account2 = "Account2_ID" 

API api documentation \
https://Account1_ID.cmapi.io/v1/docs/ \
https://Account2_ID.cmapi.io/v1/docs/



# How to run 
    
Execute `python CM_API.py` with optional arguments: 

#### Arguments:

`-y {int}` Event Start Date Year. From 2018 to current year. Pass for all. \
`-u {str}` Business Unit 'DK' or 'PL'. Pass for both. \
`-f {str}` Save format:  'csv' or 'excel'. Pass for .csv

#### Examples:

`python CM_API.py`   -  Refresh all dataset (Priopably won't work due to HTTP 400 or 401 or 408)  \
`python CM_API.py -u 'DK'` -  Refresh danish data (Priopably won't work due to HTTP 400 or 401 or 408) \
`python CM_API.py -y 2024` - Get 2024 data
            
            

            
# To do: 

### Autorefresh online
`python CM_API.py -y {Current Year}` 

### Security 
API passwords are stored directly in the code - bad idea I guess 🥸
import pandas as pd
import json
import requests
import time
import os
import random
import csv
from pathlib import Path

YAHOO_FINANCE_API_HEADERS = {
    'x-rapidapi-key': "71a5d7c9a5msh0ce9fc09f6a1668p137554jsnde2c9287d2b4",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

FIN_DATA_kEYS = ['targetLowPrice', 'targetMedianPrice', 'currentPrice', 'targetMeanPrice', 'targetHighPrice']


def loadsampledata():
    #data = pd.read_csv('..\..\Portfolio\Positions - Default.csv')
    
    project_path = Path(os.getcwd())

    #data_path = Path('Portfolio\Positions - Default.csv')
    data_path = Path(r'Portfolio\Positions - Retirement and TFSA - Default.csv')
    final_path = os.path.join(project_path.parent.parent, data_path)

    data = pd.read_csv(final_path)

    return data

class AnalysisResult:
    
    #Class variables
    instrument_found = False
    instrument_type = 'unknown'
    instrument_symbol = ''
    instrument_data = {}
    
    #Class constructor
    def __init__(self, symbol):
        self.instrument_symbol = symbol
        self.instrument_found = False
        self.instrument_data = {}
        self.instrument_type = 'unknown'

def rate_limited_request(request_type, request_url, headers, params):
    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        # Make a request to Clover REST API
        #response = requests.get(request_url, headers = {"Authorization": "Bearer " + api_token})
        response = requests.request(request_type, request_url, headers=headers, params=params)
        
        # If not rate limited, break out of while loop and continue with the rest of the code
        if response.status_code != 429:
            break
        
        # If rate limited, wait and try again
        time.sleep((2 ** attempts) + random.random())
        attempts = attempts + 1

    return response


def get_analysis(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"

    querystring = {"symbol": symbol}
    result = AnalysisResult(symbol)

    #response = requests.get(url, headers=headers, params=querystring)
    #response = requests.request("GET", url, headers=YAHOO_FINANCE_API_HEADERS, params=querystring)
    response = rate_limited_request("GET", url, YAHOO_FINANCE_API_HEADERS, querystring)

    
#    print (response.headers)
    if response.status_code != 200:
        print("Error in response")
        return False
    
    elif response.headers['content-length'] == "0":
        return result
    
    else:
        analysis = response.json()
        
        #if analysis.hasOwnProperty('financialData'):
        if 'financialData' in analysis:
            result.instrument_type = 'STOCK'
        
            #fin_data_keys = ['targetLowPrice', 'targetMedianPrice', 'currentPrice', 'targetMeanPrice', 'targetHighPrice']
            
            for key in FIN_DATA_kEYS:
                if 'fmt' in analysis['financialData'][key]:
                    #print("Adding " + key + " = " + json.dumps(analysis['financialData'][key]['fmt'], indent = 4, sort_keys=False))
                    result.instrument_data[key] = analysis['financialData'][key]['fmt']
                    result.instrument_found = True

                else:
                    print(key + "value does not exist for " + symbol)
            
            return result
    
        #elif analysis.hasOwnProperty('fundPerformance'):
        elif 'fundPerformance' in analysis:
            result.instrument_type = 'ETF'

            fund_performance_keys = ['annualTotalReturns']

            for key in fund_performance_keys:
                if 'annualTotalReturns' in analysis['fundPerformance']:
                    #print("Adding " + json.dumps(analysis['fundPerformance']['annualTotalReturns'], indent = 4, sort_keys=False))
                    result.instrument_data['annualTotalReturns'] = analysis['fundPerformance']['annualTotalReturns']
                    result.instrument_found = True
                else:
                    print(key + "value does not exist for " + symbol)
            
            return result

            
        else:
            print("New category")
            return result

#get_analysis("TSLA"), 
#get_analysis("XEQT")
#get_analysis("THNK.V")


data = loadsampledata()
symbols = data.Symbol.dropna().unique()
#symbols = ['TSLA', 'XEQT', 'XEQT.TO', 'THNK.V']

print(len(symbols), symbols)

symbol_stocks = []
symbol_etfs = []
symbol_unknowns = []


for symbol in symbols:
    print("Analyzing " + symbol )
    analysis = get_analysis(symbol)    
    if analysis == False:
        symbol_unknowns.append(symbol)
    elif analysis.instrument_found:
            if analysis.instrument_type == "STOCK":
                symbol_stocks.append(analysis)
            if analysis.instrument_type == "ETF":
                symbol_etfs.append(analysis)
    else:
        symbol_unknowns.append(analysis)

print("-------- Results -------")

with open('analysis-stock.csv', 'wb') as stockcsvfile:
    filewriter = csv.writer(stockcsvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Symbol', 'Type'] + FIN_DATA_kEYS)

for i in symbol_stocks:
    print(i.instrument_symbol, i.instrument_type, i.instrument_data)
    datalist = []
    for key in FIN_DATA_kEYS:
        datalist.append(i.instrument_data[key])
    filewriter.writerow([i.instrument_symbol, i.instrument_type] + datalist)

for j in symbol_etfs:
    print(j.instrument_symbol, j.instrument_type)

print("For the following - Data not found")
for k in symbol_unknowns:
    print(k.instrument_symbol)




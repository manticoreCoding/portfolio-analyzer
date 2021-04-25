import pandas as pd
import json
import requests
import os
from pathlib import Path

data_loc = r'Portfolio\Positions - Default.csv'

headers = {
    'x-rapidapi-key': "71a5d7c9a5msh0ce9fc09f6a1668p137554jsnde2c9287d2b4",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

def loadsampledata():
    #data = pd.read_csv('..\..\Portfolio\Positions - Default.csv')
    
    project_path = Path(os.getcwd())
    data_path = Path(data_loc)
    #data_path = Path('Portfolio\Positions - Default.csv')
    final_path = os.path.join(project_path.parent.parent, data_path)

    data = pd.read_csv(final_path)

    return data

class AnalysisResult:
    
    instrument_found = False
    instrument_type = 'unknown'
    instrument_symbol = ''
    instrument_data = {}

    def __init__(self, symbol):
        self.instrument_symbol = symbol



def get_analysis(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"

    querystring = {"symbol": symbol}
    result = AnalysisResult(symbol)


    response = requests.request("GET", url, headers=headers, params=querystring)
    #response = requests.get(url, headers=headers, params=querystring)
    
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
            #print(json.dumps(analysis, indent = 4, sort_keys=False))
            keys = ['targetLowPrice', 'targetMedianPrice', 'currentPrice', 'targetMeanPrice', 'targetHighPrice']
            
            for key in keys:
                if 'fmt' in analysis['financialData'][key]:
                    print(key + " = " + json.dumps(analysis['financialData'][key]['fmt'], indent = 4, sort_keys=False))
                else:
                    print(key + "value does not exist for " + symbol)
                    return False
            #return True
            return analysis['financialData']
    
        #elif analysis.hasOwnProperty('fundPerformance'):
        elif 'fundPerformance' in analysis:
            print(symbol + "is a fund/ETF")
            if 'annualTotalReturns' in analysis['fundPerformance']:
                print(json.dumps(analysis['fundPerformance']['annualTotalReturns'], indent = 4, sort_keys=False))
                return analysis['fundPerformance']['annualTotalReturns']
            else:
                print(len(analysis['fundPerformance']))
                return False

            
        else:
            print("New category")
            return True

#get_analysis("TSLA"), 
#get_analysis("XEQT")
#get_analysis("THNK.V")



data = loadsampledata()
#symbols = data.Symbol.dropna().unique()
symbols = ['TSLA', 'XEQT', 'THNK.V']

print(len(symbols), symbols)



for symbol in symbols:
    print("Analyzing " + symbol )
    result = get_analysis(symbol)
    print(result)
    print("-----------")

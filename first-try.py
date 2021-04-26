import pandas as pd
import json
import requests
import os
from pathlib import Path

data_folder = Path("/Portfolio/")
data_file = "Positions - Default.csv"

headers = {
    'x-rapidapi-key': "71a5d7c9a5msh0ce9fc09f6a1668p137554jsnde2c9287d2b4",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

def loadsampledata():
    #data = pd.read_csv('..\..\Portfolio\Positions - Default.csv')
    
    project_path = Path(os.getcwd())
    file_to_open = data_folder / data_file
    #data_path = Path('Portfolio\Positions - Default.csv')
    final_path = os.path.join(project_path.parent.parent, file_to_open)

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
            result.instrument_type = 'stock'
        
            keys = ['targetLowPrice', 'targetMedianPrice', 'currentPrice', 'targetMeanPrice', 'targetHighPrice']
            
            for key in keys:
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

            keys = ['annualTotalReturns']

            for key in keys:
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
#symbols = data.Symbol.dropna().unique()
symbols = ['TSLA', 'XEQT', 'XEQT.TO']

print(len(symbols), symbols)



for symbol in symbols:
    print("Analyzing " + symbol )
    analysis = get_analysis(symbol)
    unknowns = []
    if analysis.instrument_found:
        print(analysis.instrument_symbol, analysis.instrument_type, analysis.instrument_data)
    else:
        unknowns.append(analysis)
    print("-----------")

for i in unknowns:
    print("For the following - Data not found")
    print(i.instrument_symbol)
    

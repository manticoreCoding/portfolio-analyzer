import pandas as pd
import json
import requests

def loadsampledata():
    data = pd.read_csv('..\..\Portfolio\Positions - Default.csv')

    return data

data = loadsampledata()

symbols = data.Symbol.dropna().unique()
#symbols2 = data.dropna().Symbol.unique()

#pd.unique(data["Symbol"])

#data["Symbol"].unique()
#data.Symbol.unique()

print(len(symbols), symbols)
#print(len(symbols2), symbols2)

headers = {
    'x-rapidapi-key': "71a5d7c9a5msh0ce9fc09f6a1668p137554jsnde2c9287d2b4",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

def check_url(url):
  url = urlparse(url)
  conn = http.client.HTTPConnection(url.netloc)
  conn.request("HEAD", url.path)
  r = conn.getresponse()
  if r.status == 200:
    return True
  else:
    return False

def get_analysis(symbol):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"

    querystring = {"symbol": symbol}


    response = requests.request("GET", url, headers=headers, params=querystring)
    #response = requests.get(url, headers=headers, params=querystring)
    
#    print (response.headers)
    if response.status_code != 200:
        print("Error in response")
        return false
    
    elif response.headers['content-length'] == "0":       
        print(symbol + " symbol not found")
        
        return True
    
    else:
        #analysis = json.loads(response.text)
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

for symbol in symbols:
    print("Analyzing " + symbol )
    get_analysis(symbol)
    print("-----------")
from flask import Flask
from nepse import Nepse

app = Flask(__name__)

nepse = Nepse()

date='2025-05-19'
nepse.setTLSVerification(False)

@app.route('/')
def hello():
    return 'Hello, World! apple'

@app.route('/m')
def priceVolumeHistory():
    print("start nepse")
    data = nepse.getMarketStatus()
    print(data)
    return data

@app.route('/a')
def getSummarysss():
    print("start nepse")
    data = nepse.getSummary()
    print(data)
    return data

if __name__ == '__main__':
    app.run(debug=True,port=8000)
# 

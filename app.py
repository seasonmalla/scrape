from flask import Flask
from nepse import Nepse

app = Flask(__name__)

nepse = Nepse()

date='2025-05-19'

@app.route('/')
def hello():
    return 'Hello, World! apple'

@app.route('/nepse')
def prieVolumeHistory():
    return nepse.getPriceVolumeHistory(date)


if __name__ == '__main__':
    app.run(debug=True,port=8000)
# 

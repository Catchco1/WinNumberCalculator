# an object of WSGI application 
import time
from flask import Flask
from flask import request
from dataProcessing.analyze import makeGraphs, tallyVotes

app = Flask(__name__)   # Flask constructor 
  
# A decorator used to tell the application 
# which URL is associated function 
@app.route('/')       
def defaultRoute(): 
    return 'HELLO'

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/graph', methods=['POST'])
def get_election_graph():
    data = request.json
    years = data.get('years')
    state = data.get('state')
    office = data.get('office')
    districtNum = int(data.get('district'))
    results = []
    for year in years:
        results.append(tallyVotes(state, districtNum, office, year))
    return makeGraphs(results)
  
if __name__=='__main__': 
   app.run() 

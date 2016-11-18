from flask import Flask,request,jsonify
from NLP import *
from GooglePlaceDetailAPI import *
from urllib import urlopen
import json
import requests
import urllib2
from gevent.wsgi import WSGIServer
app = Flask(__name__)
# api = Api(app)
from flask_cors import CORS,cross_origin

import pdb
import time

CORS(app)
@app.route('/')
def get():
    starttime = time.time()
    todo_id=request.args['searchstring']
    #print "todo_id ",todo_id
    [query,bhk,bhk_desc,apt_type,budget,budget_item,budget_desc,amenities,location,possession,possession_desc,date]=start(todo_id)
    total_budget=0
    print "++++++++++++++++++++++++++++++++++++"
    total_budget=0
    if budget_desc:
        for item in budget_desc:
            if item in ["cheap","low"]:
                total_budget=1000000
            if item in ["delux","posh","costly"]:
                total_budget=10000000
    
    if budget :
        try: 
            total_budget=float(max(budget))
        except: 
            total_budget=0

        if budget_item:
            for item in budget_item:
                if item in ['cr','crore','crores' ]:
                    total_budget=total_budget*10000000
                    break

                if item in ['lac','l','lakh','lacs','lakhs']:
                    total_budget=total_budget*100000
                    break

        
    poss=0
    if possession:
        if date:
            if date[0] in ['year','yr','yrs','years']:
                possession=int(possession[0])*12
            else:
                possession=int(possession[0])

            if possession_desc[0] in ["more"]:
                if possession <6:
                    poss=1
                if  possession >=6 and possession <12:
                    poss=2
                if  possession >=12 and possession <24:
                    poss=3
                if  possession >=24 and possession <36:
                    poss=4
                if  possession >=36:
                    poss=5

            else:
                if possession <6:
                    poss=1
                if  possession >=6 and possession <12:
                    poss=2
                if  possession >=12 and possession<24:
                    poss=3
                if  possession >=24 and possession<36:
                    poss=4
                if  possession >=36:
                    poss=5

    
    string="https://hdfcred.com/mobile_v3/project_listing_new_revised/?"
    str1=string
    lat=[]
    log=[]
    cityid=[]
    places_found=[]
    if location:
        for item in location:
            try:
                locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+item+"&wt=json&indent=true"
                req = urllib2.Request(locationstring)
                url = urllib2.urlopen(req).read()
                result_location = json.loads(url)
                lat.append(result_location['response']['docs'][0]['latitude'])
                log.append(result_location['response']['docs'][0]['longitude'])
                cityid.append(result_location['response']['docs'][0]['cityid'])
                places_found.append(item)
            except:
                [geoLatitude,geoLongitude,address]=start123(item)
                if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                    lat.append(geoLatitude)
                    log.append(geoLongitude)
                    places_found.append(item)

        if lat:
            if not string==str1:
                string=string+"&"
            string=string+"lat="

            for item in lat:
                string=string+str(item)+","
            string=string[:-1]+"&long="
            
            for item in log:
                string=string+str(item)+","
            string=string[:-1]+"&areas="

            for item in places_found:
                string=string+str(item.title())+"$$"
            string=string[:-2]

        if cityid:
            if not string==str1:
                string=string+"&"
            string=string+"cityid="+max(cityid)

    if apt_type:
        if not string==str1:
            string=string+"&"
        string=string+"propertytype="+apt_type[0]
    else:
        if not string==str1:
            string=string+"&"
        string=string+"propertytype="+"APARTMENT"
    

    if bhk:
        if not string==str1:
            string=string+"&"
        string=string+"bhk="+str(min(bhk))

    elif bhk_desc:
        for item in bhk_desc:
            if item in ["small","tiny"]:
                if not string==str1:
                    string=string+"&"
                string=string+"bhk=2"
                break
            if item in ["big","huge","large"]:
                if not string==str1:
                    string=string+"&"
                string=string+"bhk=4"
                break

    if total_budget:
        if not string==str1:
            string=string+"&"
        string=string+"budget="+str(total_budget)

        
    if amenities:   
        if not string==str1:
            string=string+"&"
        string=string+"amenityid="
        for item in amenities:
            string=string+str(item)+","
        string=string[:-1]
    if not string==str1:
            string=string+"&"
    string=string+"possession="+str(poss)+"&position=Location,Budget,Size,Possession,Amenities&limit=0,30"

    print string
    endtime = time.time()
    print "total Time " , endtime - starttime
    try :
        url = urlopen(string).read()
        print "Hello "
        result = json.loads(url)
        
        print "Hello 2"
        return jsonify({
		"result": result,
		"url": string,
		})

    except:
        result =  {
		"data": [], 
		"msg": "zero projects", 
		"status": 0, 
		"total": 0
		}
        return jsonify({
		"result": result,
		"url": string,
		})
    #return url 
    #return {"text":todo_id,"string":string,"apt_type":apt_type,"BHK":bhk,"Budget":total_budget,"Amenities":amenities,"Location":location,"Possession":possession}
    #return {"text":todo_id,"apt_type":apt_type,"BHK":bhk,"Budget":total_budget,"Amenities":amenities,"Location":location,"latitude":geoLatitude,"longitude":geoLongitude}


if __name__ == '__main__':
#    app.run(host='0.0.0.0',port=6020)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()


from flask import Flask,request,jsonify
from NLP5 import *
from GooglePlaceDetailAPI import *
from urllib import urlopen
import json
import requests
import urllib2
from gevent.wsgi import WSGIServer
app = Flask(__name__)
# api = Api(app)
import pdb
import time
import datetime
from flask_cors import CORS,cross_origin

fileName = "newApiTest"  + str(datetime.date.today().month ) + str(datetime.date.today().year)

CORS(app)
@app.route('/')
def get():
    starttime = time.time()
    amenity_exclusion=["park","garden","gas","pipeline","gate","sports","manor","park","old","golf","mandir","gurudwara","garden","park","mall","pooja","jog","pent","jacuuzi","jacuzi","vaastu","dargah","puja"]
    todo_id=request.args['searchstring']
    [query,bhk,bhk_desc,apt_type,budget,budget_item,budget_adj,amenities,location,adv_location,radius,possession,possession_desc,date,project_id,project_name]=start(todo_id)
    nlptime=time.time()

    poss=0
    if possession:
        if date:
            if date[0] in ['year','yr','yrs','years']:
                possession=int(possession[0])*12
            else:
                possession=int(possession[0])

            if possession_desc[0] in ["more","after"]:
                if possession <6:
                    poss=3
                if  possession >=6 and possession <12:
                    poss=4
                if  possession >=12 and possession <24:
                    poss=5
                if  possession >=24 and possession <36:
                    poss=6
                if  possession >=36:
                    poss=6

            else:
                if possession <6:
                    poss=2
                if  possession >=6 and possession <12:
                    poss=3
                if  possession >=12 and possession<24:
                    poss=4
                if  possession >=24 and possession<36:
                    poss=5
                if  possession >=36:
                    poss=6



    string = "http://52.66.44.154/apimaster/mobile_v3?"
    str1=string
    
    lat={"in":[],"notin":[],"dist":[],"nearby":[],"around":[],"direction":[]}
    log={"in":[],"notin":[],"dist":[],"nearby":[],"around":[],"direction":[]}
    place={"in":[],"notin":[],"dist":[],"nearby":[],"around":[],"direction":[]}
    cityid=[]
    adverbs=[]
    dirs=[]
    if location:
        for i,adv in enumerate(adv_location):
            if adv in ['in','at']:
                adverbs.append(adv)
                if not location[i] in amenity_exclusion and not location[i] in project_name:
                    try:
                        locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                        req = urllib2.Request(locationstring)
                        url = urllib2.urlopen(req).read()
                        result_location = json.loads(url)
                        place['in'].append(location[i])
                        lat['in'].append(result_location['response']['docs'][0]['latitude'])
                        log['in'].append(result_location['response']['docs'][0]['longitude'])
                        cityid.append(result_location['response']['docs'][0]['cityid'])

                    except:
                        [geoLatitude,geoLongitude,address]=start123(location[i])
                        place['in'].append(location[i])
                        lat['in'].append(geoLatitude)
                        log['in'].append(geoLongitude)

            if adv in ['not']:
                adverbs.append(adv)
                if not location[i] in amenity_exclusion and not location[i] in project_name:
                    try:
                        locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                        req = urllib2.Request(locationstring)
                        url = urllib2.urlopen(req).read()
                        result_location = json.loads(url)
                        place['notin'].append(location[i])
                        lat['notin'].append(result_location['response']['docs'][0]['latitude'])
                        log['notin'].append(result_location['response']['docs'][0]['longitude'])
                        cityid.append(result_location['response']['docs'][0]['cityid'])

                    except:
                        [geoLatitude,geoLongitude,address]=start123(location[i])
                        place['notin'].append(location[i])
                        lat['notin'].append(geoLatitude)
                        log['notin'].append(geoLongitude)

            if adv in ['dist']:
                adverbs.append(adv)
                if not location[i] in amenity_exclusion and not location[i] in project_name:
                    try:
                        locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                        req = urllib2.Request(locationstring)
                        url = urllib2.urlopen(req).read()
                        result_location = json.loads(url)
                        lat['dist'].append(result_location['response']['docs'][0]['latitude'])
                        log['dist'].append(result_location['response']['docs'][0]['longitude'])
                        place['dist'].append(location[i])
                        cityid.append(result_location['response']['docs'][0]['cityid'])

                    except:
                        [geoLatitude,geoLongitude,address]=start123(location[i])
                        place['dist'].append(location[i])
                        lat['dist'].append(geoLatitude)
                        log['dist'].append(geoLongitude)

            if adv in ['nearby','near']:
                adverbs.append(adv)
                if not location[i] in amenity_exclusion and not location[i] in project_name:
                    try:
                        locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                        req = urllib2.Request(locationstring)
                        url = urllib2.urlopen(req).read()
                        result_location = json.loads(url)
                        lat['nearby'].append(result_location['response']['docs'][0]['latitude'])
                        log['nearby'].append(result_location['response']['docs'][0]['longitude'])
                        place['nearby'].append(location[i])
                        cityid.append(result_location['response']['docs'][0]['cityid'])

                    except:
                        [geoLatitude,geoLongitude,address]=start123(location[i])
                        place['nearby'].append(location[i])
                        lat['nearby'].append(geoLatitude)
                        log['nearby'].append(geoLongitude)

            if adv in ['around']:
                adverbs.append(adv)
                if not location[i] in amenity_exclusion and not location[i] in project_name:
                    try:
                        locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                        req = urllib2.Request(locationstring)
                        url = urllib2.urlopen(req).read()
                        result_location = json.loads(url)
                        lat['around'].append(result_location['response']['docs'][0]['latitude'])
                        log['around'].append(result_location['response']['docs'][0]['longitude'])
                        place['around'].append(location[i])
                        cityid.append(result_location['response']['docs'][0]['cityid'])

                    except:
                        [geoLatitude,geoLongitude,address]=start123(location[i])
                        place['around'].append(location[i])
                        lat['around'].append(geoLatitude)
                        log['around'].append(geoLongitude)

            if adv in ['direction']:
                adverbs.append(adv)
                if not location[i] in amenity_exclusion and not location[i] in project_name:
                    try:
                        locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                        req = urllib2.Request(locationstring)
                        url = urllib2.urlopen(req).read()
                        result_location = json.loads(url)
                        lat['direction'].append(result_location['response']['docs'][0]['latitude'])
                        log['direction'].append(result_location['response']['docs'][0]['longitude'])
                        place['direction'].append(location[i])
                        cityid.append(result_location['response']['docs'][0]['cityid'])
                        adverbs.append(adv)

                    except:
                        [geoLatitude,geoLongitude,address]=start123(location[i])
                        place['direction'].append(location[i])
                        lat['direction'].append(geoLatitude)
                        log['direction'].append(geoLongitude)
                        dirs.append(adv)
        

        if adverbs:
            if not string==str1:
                    string=string+"&"
            string+="LocKeyword="
            adverbs=list(set(adverbs))
            for item in adverbs:
                string+=item+","
            string=string[:-1]

        if lat["in"]:
                if not string==str1:
                    string=string+"&"
                string+="inLocation="
                for item in place["in"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&inLat="    

                for item in lat["in"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&inLong=" 

                for item in log["in"]:
                    string=string+str(item)+","
                string=string[:-1]

        if lat["notin"]:
                if not string==str1:
                    string=string+"&"
                string+="notInLocation="
                for item in place["notin"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&notInLat="    

                for item in lat["notin"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&notInLong=" 

                for item in log["notin"]:
                    string=string+str(item)+","
                string=string[:-1]

        if lat["dist"]:
                if not string==str1:
                    string=string+"&"
                string+="distLocation="
                for item in place["dist"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&distLat="    

                for item in lat["dist"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&distLong=" 

                for item in log["dist"]:
                    string=string+str(item)+","
                string=string[:-1]
                
                if radius:
                    string=string+"&locationDist="+str(radius[0])
                else:
                    string=string+"&locationDist="+"4"

        if lat["nearby"]:
                if not string==str1:
                    string=string+"&"
                string+="nearByLocation="
                for item in place["nearby"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&nearByLat="    

                for item in lat["nearby"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&nearByLong=" 

                for item in log["nearby"]:
                    string=string+str(item)+","
                string=string[:-1]

        if lat["around"]:
                if not string==str1:
                    string=string+"&"
                string+="aroundLocation="
                for item in place["around"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&aroundLat="    

                for item in lat["around"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&aroundLong=" 

                for item in log["around"]:
                    string=string+str(item)+","
                string=string[:-1]

        if lat["direction"]:
                if not string==str1:
                    string=string+"&"
                string+="directionLocation="
                for item in place["direction"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&directionLat="    

                for item in lat["direction"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&directionLong=" 

                for item in log["direction"]:
                    string=string+str(item)+","
                string=string[:-1]
                string+="&locationDirection="

                for item in dirs:
                    string=string+str(item)+","
                string=string[:-1]
        

        if cityid:
            if not string==str1:
                string=string+"&"
            string=string+"cityid="+list(set(cityid))[0]


    
    if apt_type:
        if not string==str1:
            string=string+"&"
        string=string+"propType="+apt_type[0]
    else:
        if not string==str1:
            string=string+"&"
        string=string+"propType="+"APARTMENT"    
    if bhk_desc:
        for item in bhk_desc:
            if item in ["small","tiny"]:
                bhk.append(1)
            if item in ["big","huge","large"]:
                bhk.append(3)
    if bhk:
        if not string==str1:
            string=string+"&"
        string=string+"maxBHK="+str(max(bhk))
    
    budget_modified=[]
    minimumprice=0
    maximumprice=0
    if budget:
        for i,item in enumerate(budget):
                try:
                    if budget_item:    
                        try:
                            if budget_item[i]:
                                if budget_item[i] in ['cr','crore','crores' ]:
                                    budget_modified.append(float(float(item)*10000000))
                                if budget_item[i] in ['lac','l','lakh','lacs','lakhs']:
                                    budget_modified.append(float(float(item)*100000))
                                if budget_item[i] in ['number']:
                                    budget_modified.append(float(item))
                        except:
                            if budget_item[0] in ['cr','crore','crores' ]:
                                budget_modified.append(float(float(item)*10000000))
                            if budget_item[0] in ['lac','l','lakh','lacs','lakhs']:
                                budget_modified.append(float(float(item)*100000))
                except:
                    budget_modified.append(float(item))


        print budget_modified
        length=len(budget_modified)
        if length==1:
            if budget_adj:
                for item in budget_adj:
                    if item in ["around","near","within","nearby"]:
                        minimumprice=min(budget_modified)*0.7
                        maximumprice=max(budget_modified)*1.3
                        break
                    if item in ["in","of","at","more","above"]:
                        minimumprice=min(budget_modified) 
                    if item in ["less","below","under"]:
                        maximumprice=max(budget_modified)
            else:
                minimumprice=min(budget_modified)*0.7
                maximumprice=max(budget_modified)*1.3


        else:
            budget_modified.sort()
            minimumprice=min(budget_modified)
            maximumprice=max(budget_modified)


    if minimumprice:
        if not string==str1:
            string=string+"&"
        string=string+"minBudget="+str(minimumprice)

    if maximumprice:
        if not string==str1:
            string=string+"&"
        string=string+"maxBudget="+str(maximumprice)

    if project_id:
        if not string==str1:
            string=string+"&"
        string+="projectid="
        for item in project_id: 
            string+=str(item)+","
        string=string[:-1]    
    
    if amenities:    
        if not string==str1:
            string=string+"&"
        string=string+"amenities="
        for item in amenities:
            string=string+str(item)+","
        string=string[:-1]

    if poss:
        if not string==str1:
                string=string+"&"
        string=string+"possession="+str(poss)
    print string

    stringformationtime=time.time()
    
    logString= "\n"
    try:
        for a in [starttime,query,bhk,bhk_desc,apt_type,budget,budget_item,budget_adj,amenities,location,adv_location,radius,possession,possession_desc,date,project_id,project_name]:
            logString =  logString + str(a) + ";"

        with open(fileName,"a") as myFile:
            myFile.write(logString)
    except:
        pass

    try :
        url = urlopen(string).read()
        result = json.loads(url)
    except:
        result =  {
        "data": [], 
        "msg": "zero projects", 
        "status": 0, 
        "total": 0
        }

    jtime = time.time()
    print "NLP time " , nlptime-starttime
    print  "stringForm  " , stringformationtime - nlptime
    print "jtime  " ,  jtime - stringformationtime
    print "total Time " , jtime - starttime
    return jsonify({
        "result": result,
        "url": string,
        })



if __name__ == '__main__':
#    app.run(host='0.0.0.0',port=6020)
    http_server = WSGIServer(('0.0.0.0', 5006), app)
    http_server.serve_forever()


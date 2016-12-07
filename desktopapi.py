
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
    [query,bhk,bhk_desc,apt_type,budget,budget_item,budget_adj,amenities,location,adv_location,radius,possession,possession_desc,date,project_id,project_name,area,area_type,dim]=start(todo_id)
    nlptime=time.time()

    poss=0
    if possession:
        if date:
            if date[0] in ['year','yr','yrs','years']:
                possession=int(possession[0])*12
            else:
                possession=int(possession[0])

            try:
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

            except:
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



    string = "http://52.66.44.154/apimaster/mobile_v3/nlp_listing_v1?"
    str1=string
    
    lat={"in":[],"notin":[],"dist":[],"nearby":[],"around":[],"direction":[]}
    log={"in":[],"notin":[],"dist":[],"nearby":[],"around":[],"direction":[]}
    place={"in":[],"notin":[],"dist":[],"nearby":[],"around":[],"direction":[]}
    cityid=[]
    adverbs=[]
    dirs=[]
    if location:
        if adv_location:
            for i,adv in enumerate(adv_location):
                if adv in ['in','at']:
                    if not location[i] in amenity_exclusion and not location[i] in project_name:
                        try:
                            locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                            req = urllib2.Request(locationstring)
                            url = urllib2.urlopen(req).read()
                            result_location = json.loads(url)
                            lat['in'].append(result_location['response']['docs'][0]['latitude'])
                            log['in'].append(result_location['response']['docs'][0]['longitude'])
                            cityid.append(result_location['response']['docs'][0]['cityid'])
                            place['in'].append(location[i])
                            adverbs.append("in")

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                place['in'].append(location[i])
                                lat['in'].append(geoLatitude)
                                log['in'].append(geoLongitude)
                                adverbs.append("in")

                elif adv in ['not']:
                    if not location[i] in amenity_exclusion and not location[i] in project_name:
                        try:
                            locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                            req = urllib2.Request(locationstring)
                            url = urllib2.urlopen(req).read()
                            result_location = json.loads(url)
                            lat['notin'].append(result_location['response']['docs'][0]['latitude'])
                            log['notin'].append(result_location['response']['docs'][0]['longitude'])
                            cityid.append(result_location['response']['docs'][0]['cityid'])
                            place['notin'].append(location[i])
                            adverbs.append("notIn")

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                place['notin'].append(location[i])
                                lat['notin'].append(geoLatitude)
                                log['notin'].append(geoLongitude)
                                adverbs.append("notIn")

                elif adv in ['dist','distance','from']:
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
                            adverbs.append("dist")

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                place['dist'].append(location[i])
                                lat['dist'].append(geoLatitude)
                                log['dist'].append(geoLongitude)
                                adverbs.append("dist")

                elif adv in ['nearby','near']:
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
                            adverbs.append("nearBy")

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                place['nearby'].append(location[i])
                                lat['nearby'].append(geoLatitude)
                                log['nearby'].append(geoLongitude)
                                adverbs.append("nearBy")

                elif adv in ['around']:
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
                            adverbs.append("around")

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                place['around'].append(location[i])
                                lat['around'].append(geoLatitude)
                                log['around'].append(geoLongitude)
                                adverbs.append("around")

                elif adv in ['north','east','west','south']:
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
                            adverbs.append("direction")
                            dirs.append(adv)


                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                place['direction'].append(location[i])
                                lat['direction'].append(geoLatitude)
                                log['direction'].append(geoLongitude)
                                adverbs.append("direction")
                                dirs.append(adv)

                else:
                    if not location[i] in amenity_exclusion and not location[i] in project_name:
                        try:
                            locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                            req = urllib2.Request(locationstring)
                            url = urllib2.urlopen(req).read()
                            result_location = json.loads(url)
                            lat['in'].append(result_location['response']['docs'][0]['latitude'])
                            log['in'].append(result_location['response']['docs'][0]['longitude'])
                            cityid.append(result_location['response']['docs'][0]['cityid'])
                            place['in'].append(location[i])
                            adverbs.append("in")

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                place['in'].append(location[i])
                                lat['in'].append(geoLatitude)
                                log['in'].append(geoLongitude)
                                adverbs.append("in")
        else:
            for i,item in enumerate(location):
                if not location[i] in amenity_exclusion and not location[i] in project_name:
                    try:
                        locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                        req = urllib2.Request(locationstring)
                        url = urllib2.urlopen(req).read()
                        result_location = json.loads(url)
                        lat['in'].append(result_location['response']['docs'][0]['latitude'])
                        log['in'].append(result_location['response']['docs'][0]['longitude'])
                        cityid.append(result_location['response']['docs'][0]['cityid'])
                        place['in'].append(location[i])
                        adverbs.append("in")

                    except:
                        [geoLatitude,geoLongitude,address]=start123(location[i])
                        if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                            place['in'].append(location[i])
                            lat['in'].append(geoLatitude)
                            log['in'].append(geoLongitude)
                            adverbs.append("in")

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
                    if item in ["around","near","within","nearby","from"]:
                        minimumprice=min(budget_modified)*0.7
                        maximumprice=max(budget_modified)*1.3
                        break
                    elif item in ["in","of","at","more","above"]:
                        minimumprice=min(budget_modified) 
                    elif item in ["less","below","under"]:
                        maximumprice=max(budget_modified)
                    else:
                        minimumprice=min(budget_modified)

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

    minarea=0
    maxarea=0
    if area:
        length=len(area)
        if length==1:
            if area_type:
                for item in area_type:
                    if item in ["around","near","within","nearby","from"]:
                        minarea=float(min(area))*0.7
                        maxarea=float(max(area))*1.3
                        break
                    elif item in ["in","of","at","more","above"]:
                        minarea=min(area) 
                    elif item in ["less","below","under"]:
                        maxarea=max(area)
                    else:
                        minarea=min(area)

            else:
                minarea=min(area)*0.7
                maxarea=max(area)*1.3


        else:
            area.sort()
            minarea=min(area)
            maxarea=max(area)

    if minarea:
        if not string==str1:
            string=string+"&"
        string=string+"minArea="+str(minarea)

    if maxarea:
        if not string==str1:
            string=string+"&"
        string=string+"maxArea="+str(maxarea)

    if dim:
        if not string==str1:
            string=string+"&"
        if dim[0] in ['sqft','sft','ft']:
            string+="areaUnit=sq. ft"

        elif dim[0] in ['meter','mtrsqr','metersquare']:
            string+="areaUnit=sq. m"

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


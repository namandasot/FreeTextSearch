
from flask import Flask,request,jsonify,session
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

fileName = "newApi"  + str(datetime.date.today().month ) + str(datetime.date.today().year)
app.config['SECRET_KEY']='adasd'
CORS(app)
@app.route('/')
def get():
    string=request.args['searchstring']
   
    user_id='1234'
    limit="0,20"
    if limit == "0,20":
        url=str(URL_formation(string))
        session[user_id]= url
    else:
            if user_id in session.keys():
                url = session[user_id]+"&limit="+limit
            else:
                url=str(URL_formation(string))
                session[user_id]= url
                url+="&limit=0,20"
    url_copy=url
    try :
        url = urlopen(url).read()
        result = json.loads(url)

    except:
        result =  {
        "data": [], 
        "msg": "zero projects", 
        "status": 0, 
        "total": 0
        }
    
    return jsonify({
        "result": result,
        "url": url_copy,
        }) 



def URL_formation(todo_id):
    #starttime = time.time()
    amenity_exclusion=["Bhk","Flat","Villa","Bunglow","Apartment","Park","Garden","Gas","Pipeline","Gate","Sports","Manor","Park","Old","Golf","Mandir","Gurudwara","Garden","Park","Mall","Pooja","Jog","Pent","Jacuuzi","Jacuzi","Vaastu","Dargah","Puja","Bhk Villa","Bhk Flat","Bhk Apartment"]
    todo_id=request.args['searchstring']
    [query,bhk,bhk_desc,apt_type,budget,budget_item,budget_adj,amenities,location,adv_location,radius,possession,possession_desc,date,project_id,project_name,area,area_type,dim]=start(todo_id)
    #nlptime=time.time()

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
                    if possession <=6:
                        poss=2
                    if  possession >6 and possession <=12:
                        poss=3
                    if  possession >12 and possession <=24:
                        poss=4
                    if  possession >24 and possession<=36:
                        poss=5
                    if  possession >36:
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



    string = "https://hdfcred.com/apimaster/mobile_v3/nlp_listing_v1?"
    str1=string
    
    lat={"in":"inLat=","notin":"notInLat=","dist":"distLat=","nearby":"nearByLat=","around":"aroundLat=","direction":"directionLat="}
    log={"in":"inLong=","notin":"notInLong=","dist":"distLong=","nearby":"nearByLong=","around":"aroundLong=","direction":"directionLong="}
    place={"in":"inLocation=","notin":"notInLocation=","dist":"distLocation=","nearby":"nearByLocation=","around":"aroundLocation=","direction":"directionLocation="}
    
    cityid=[]
    adverbs=[]
    dirs=[]

    if location:
        flag=0
        if adv_location:
            for i,adv in enumerate(adv_location):
                if adv in ['in','at']:
                    if not location[i] in amenity_exclusion and not location[i] in project_name:
                        try:
                            locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                            req = urllib2.Request(locationstring)
                            url = urllib2.urlopen(req).read()
                            result_location = json.loads(url)
                            lat['in']+=result_location['response']['docs'][0]['latitude']+","
                            log['in']+=result_location['response']['docs'][0]['longitude']+","
                            cityid.append(result_location['response']['docs'][0]['cityid'])
                            place['in']+=location[i]+","
                            adverbs.append("in")
                            flag=1

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                lat['in']+=str(geoLatitude)+","
                                log['in']+=str(geoLongitude)+","
                                place['in']+=location[i]+","
                                adverbs.append("in")
                                flag=1

                elif adv in ['not']:
                    if not location[i] in amenity_exclusion and not location[i] in project_name:
                        try:
                            locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                            req = urllib2.Request(locationstring)
                            url = urllib2.urlopen(req).read()
                            result_location = json.loads(url)
                            lat['notin']+=result_location['response']['docs'][0]['latitude']+","
                            log['notin']+=result_location['response']['docs'][0]['longitude']+","
                            cityid.append(result_location['response']['docs'][0]['cityid'])
                            place['notin']+=location[i]+","
                            adverbs.append("notIn")
                            flag=1

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                lat['notin']+=str(geoLatitude)+","
                                log['notin']+=str(geoLongitude)+","
                                place['notin']+=location[i]+","
                                adverbs.append("notIn")
                                flag=1

                elif adv in ['dist','distance','from']:
                    if not location[i] in amenity_exclusion and not location[i] in project_name:
                        try:
                            locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                            req = urllib2.Request(locationstring)
                            url = urllib2.urlopen(req).read()
                            result_location = json.loads(url)
                            lat['dist']+=result_location['response']['docs'][0]['latitude']+","
                            log['dist']+=result_location['response']['docs'][0]['longitude']+","
                            place['dist']+=location[i]+","
                            cityid.append(result_location['response']['docs'][0]['cityid'])
                            adverbs.append("dist")
                            flag=1

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                lat['dist']+=str(geoLatitude)+","
                                log['dist']+=str(geoLongitude)+","
                                place['dist']+=location[i]+","
                                adverbs.append("dist")
                                flag=1

                elif adv in ['nearby','near']:
                    if not location[i] in amenity_exclusion and not location[i] in project_name:
                        try:
                            locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                            req = urllib2.Request(locationstring)
                            url = urllib2.urlopen(req).read()
                            result_location = json.loads(url)
                            lat['nearby']+=result_location['response']['docs'][0]['latitude']+","
                            log['nearby']+=result_location['response']['docs'][0]['longitude']+","
                            place['nearby']+=location[i]+","
                            cityid.append(result_location['response']['docs'][0]['cityid'])
                            adverbs.append("nearBy")
                            flag=1

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                lat['nearby']+=str(geoLatitude)+","
                                log['nearby']+=str(geoLongitude)+","
                                place['nearby']+=location[i]+","
                                adverbs.append("nearBy")
                                flag=1

                elif adv in ['around']:
                    if not location[i] in amenity_exclusion and not location[i] in project_name:
                        try:
                            locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                            req = urllib2.Request(locationstring)
                            url = urllib2.urlopen(req).read()
                            result_location = json.loads(url)
                            lat['around']+=result_location['response']['docs'][0]['latitude']+","
                            log['around']+=result_location['response']['docs'][0]['longitude']+","
                            place['around']+=location[i]+","
                            cityid.append(result_location['response']['docs'][0]['cityid'])
                            adverbs.append("around")
                            flag=1

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                lat['around']+=str(geoLatitude)+","
                                log['around']+=str(geoLongitude)+","
                                place['around']+=location[i]+","
                                adverbs.append("around")
                                flag=1

                elif adv in ['north','east','west','south']:
                    if not location[i] in amenity_exclusion and not location[i] in project_name:
                        try:
                            locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                            req = urllib2.Request(locationstring)
                            url = urllib2.urlopen(req).read()
                            result_location = json.loads(url)
                            lat['direction']+=result_location['response']['docs'][0]['latitude']+","
                            log['direction']+=result_location['response']['docs'][0]['longitude']+","
                            place['direction']+=location[i]+","
                            cityid.append(result_location['response']['docs'][0]['cityid'])
                            adverbs.append("direction")
                            dirs.append(adv)
                            flag=1


                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                lat['direction']+=str(geoLatitude)+","
                                log['direction']+=str(geoLongitude)+","
                                place['direction']+=location[i]+","
                                adverbs.append("direction")
                                dirs.append(adv)
                                flag=1

            if flag==0:
                    if not location[i] in amenity_exclusion and not location[i] in project_name:
                        try:
                            locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                            req = urllib2.Request(locationstring)
                            url = urllib2.urlopen(req).read()
                            result_location = json.loads(url)
                            lat['in']+=result_location['response']['docs'][0]['latitude']+","
                            log['in']+=result_location['response']['docs'][0]['longitude']+","
                            cityid.append(result_location['response']['docs'][0]['cityid'])
                            place['in']+=location[i]+","
                            adverbs.append("in")

                        except:
                            [geoLatitude,geoLongitude,address]=start123(location[i])
                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                lat['in']+=str(geoLatitude)+","
                                log['in']+=str(geoLongitude)+","
                                place['in']+=location[i]+","
                                adverbs.append("in")
        else:
            for i,item in enumerate(location):
                if not location[i] in amenity_exclusion and not location[i] in project_name:
                    try:
                        locationstring="http://52.66.44.154:8983/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+location[i]+"&wt=json&indent=true"
                        req = urllib2.Request(locationstring)
                        url = urllib2.urlopen(req).read()
                        result_location = json.loads(url)
                        lat['in']+=result_location['response']['docs'][0]['latitude']+","
                        log['in']+=result_location['response']['docs'][0]['longitude']+","
                        cityid.append(result_location['response']['docs'][0]['cityid'])
                        place['in']+=location[i]+","
                        adverbs.append("in")

                    except:
                        [geoLatitude,geoLongitude,address]=start123(location[i])
                        if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                            lat['in']+=str(geoLatitude)+","
                            log['in']+=str(geoLongitude)+","
                            place['in']+=location[i]+","
                            adverbs.append("in")

        if adverbs:
            if not string==str1:
                    string=string+"&"
            string+="LocKeyword="
            adverbs=list(set(adverbs))
            for item in adverbs:
                string+=item+","
            string=string[:-1]

        if not lat["in"]== "inLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["in"][:-1]+"&"+lat["in"][:-1]+"&"+log["in"][:-1]
                

        if not lat["notin"]=="notInLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["notin"][:-1]+"&"+lat["notin"][:-1]+"&"+log["notin"][:-1]
                

        if not lat["dist"]=="distLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["dist"][:-1]+"&"+lat["dist"][:-1]+"&"+log["dist"][:-1]
                    
                if radius:
                    string=string+"&locationDist="+str(radius[0])
                else:
                    string=string+"&locationDist="+"4"

        if not lat["nearby"]=="nearByLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["nearby"][:-1]+"&"+lat["nearby"][:-1]+"&"+log["nearby"][:-1]
                

        if not lat["around"]=="aroundLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["around"][:-1]+"&"+lat["around"][:-1]+"&"+log["around"][:-1]

        if not lat["direction"]=="directionLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["around"][:-1]+"&"+lat["around"][:-1]+"&"+log["around"][:-1]

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
        string=string+"maxBHK="+str(min(bhk))
    
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
        flag=0
        if length==1:
            if budget_adj:
                for item in budget_adj:
                    if item in ["in","of","at","around","near","nearby","from"]:
                        minimumprice=min(budget_modified)*0.7
                        maximumprice=max(budget_modified)*1.3
                        flag=1
                        break
                    elif item in ["within","less","below","under","max","maximum"]:
                        maximumprice=max(budget_modified)
                        flag=1
                        break
                    elif item in ["more","above","min","minimum"]:
                        minimumprice=min(budget_modified)
                        flag=1
                        break 
                    
                if flag==0:
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
        flag=0
        if length==1:
            if area_type:
                for item in area_type:
                    if item in ["around","near","within","nearby","from"]:
                        minarea=float(min(area))*0.7
                        maxarea=float(max(area))*1.3
                        flag=1
                        break
                    elif item in ["in","of","at","more","above"]:
                        minarea=min(area) 
                        flag=1
                        break
                    elif item in ["less","below","under"]:
                        maxarea=max(area)
                        flag=1
                        break
                if flag==0:
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
            string+="areaUnit=4"

        elif dim[0] in ['meter','mtrsqr','metersquare']:
            string+="areaUnit=1"

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
    
    return string



if __name__ == '__main__':
#    app.run(host='0.0.0.0',port=6020)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()


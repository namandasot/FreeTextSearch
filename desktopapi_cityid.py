
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


app.config['SECRET_KEY']='adasd'
CORS(app)
@app.route('/')
def get():
    string=request.args['searchstring']
    cityid=request.args['cityid']
    user_id='1234'
    limit="0,20"
    if limit == "0,20":
        url,feedback=URL_formation(string,cityid)
        url = str(url)
        session[user_id]= url
    else:
            if user_id in session.keys():
                url = session[user_id]+"&limit="+limit
            else:
                url,feedback=URL_formation(string,cityid)
                url = str(url)
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
    try:
        totalVal = result["total"]
    except:
        totalVal = 0
    feedback = "Showing "+str(totalVal)+" properties "+feedback
    return jsonify({
        "result": result,
        "url": url_copy,
        "feedback" : feedback
        })



def URL_formation(todo_id,cityid):
    solr_ip="10.2.101.209:8983"
    starttime = str(datetime.datetime.today())
    fileName = "nlpNew"  + str(datetime.date.today().month )+ "_" + str(datetime.date.today().year)

    amenity_exclusion=["bhk flat","bhk flats","bhk","flat","flats","villa","bunglow","apartment","park","garden","gas","pipeline","gate","sports","manor","park","old","golf","mandir","gym","gurudwara","garden","park","mall","pooja","jog","pent","jacuuzi","jacuzi","vaastu","dargah","puja","bhk villa","bhk apartments","bhk apartment","east","west","north","south","central"]
    todo_id=request.args['searchstring']
    [query,bhk,bhk_desc,apt_type,budget,budget_item,budget_adj,amenities,location,adv_location,radius,possession,possession_desc,date,project_id,project_name,area,area_type,dim]=start(todo_id,cityid)
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
    
    #cityid=[]
    adverbs=[]
    dirs=[]

    def lat_long_tagging(word,keyword,city,flag):
        print "lat long taggiong word " , word
        if not word.lower() in amenity_exclusion and not word in project_name:
                        word_actual=word
                        word=word+" ,"+city
                        # try:
                        #     locationstring="http://"+solr_ip+"/solr/hdfcmarketing_shard1_replica1/select?q=name%3A"+word+"&wt=json&indent=true"
                        #     req = urllib2.Request(locationstring)
                        #     url = urllib2.urlopen(req).read()
                        #     result_location = json.loads(url)
                        #     lat[keyword]+=result_location['response']['docs'][0]['latitude']+","
                        #     log[keyword]+=result_location['response']['docs'][0]['longitude']+","
                        #     #cityid.append(result_location['response']['docs'][0]['cityid'])
                        #     place[keyword]+=word_actual+","
                        #     adverbs.append(keyword)
                        #     flag=1

                        # except:
                        try:
                            if word_actual=="kalyan":
                                [geoLatitude,geoLongitude,address] = [19.2403,73.1305,"Kalyan"]

                            else:
                                [geoLatitude,geoLongitude,address]=start123(word)

                            if float(geoLatitude)<37 and float(geoLatitude)>6 and float(geoLongitude)>68 and float(geoLongitude)<97: 
                                lat[keyword]+=str(geoLatitude)+","
                                log[keyword]+=str(geoLongitude)+","
                                place[keyword]+=word_actual+","
                                adverbs.append(keyword)
                                flag=1
                        except:
                            pass

        return flag 

    location_string=""
    if location:
        flag=0
        city_data=pd.read_csv('CityWithId.csv',header=0)
        city=city_data['Project_City_Name'][city_data['Project_City'] == int(cityid)].values[0]
        if adv_location:
            for i,adv in enumerate(adv_location):
                location[i]=location[i].lower().replace("bhk","")
                if adv in ['in','at']:
                    flag=lat_long_tagging(location[i],'in',city,flag)

                elif adv in ['not']:
                    flag=lat_long_tagging(location[i],'notin',city,flag)

                elif adv in ['dist','distance','from']:
                    flag=lat_long_tagging(location[i],'dist',city,flag)

                elif adv in ['nearby','near']:
                    flag=lat_long_tagging(location[i],'nearby',city,flag)

                elif adv in ['around']:
                    flag=lat_long_tagging(location[i],'around',city,flag)

                elif adv in ['north','east','west','south']:
                    flag=lat_long_tagging(location[i],'direction',city,flag)
                    if flag==1:
                        dirs.append(adv)

            if flag==0:
                    flag=lat_long_tagging(location[i],'in',city,flag)
        else:
            for i,item in enumerate(location):
                flag=lat_long_tagging(location[i],'in',city,flag)

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
                location_string+="in "+place["in"][11:-1]
                

        if not lat["notin"]=="notInLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["notin"][:-1]+"&"+lat["notin"][:-1]+"&"+log["notin"][:-1]
                if location_string:
                    location_string+=" and "
                location_string+="not in "+place["notin"][14:-1]
                

        if not lat["dist"]=="distLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["dist"][:-1]+"&"+lat["dist"][:-1]+"&"+log["dist"][:-1]
                if location_string:
                    location_string+=" and "
                location_string+="near "+place["dist"][13:-1]
                    
                if radius:
                    string=string+"&locationDist="+str(radius[0])
                else:
                    string=string+"&locationDist="+"4"

        if not lat["nearby"]=="nearByLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["nearby"][:-1]+"&"+lat["nearby"][:-1]+"&"+log["nearby"][:-1]
                if location_string:
                    location_string+=" and "
                location_string+="nearby "+place["nearby"][15:-1]
                

        if not lat["around"]=="aroundLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["around"][:-1]+"&"+lat["around"][:-1]+"&"+log["around"][:-1]
                if location_string:
                    location_string+=" and "
                location_string+="around "+place["around"][15:-1]

        if not lat["direction"]=="directionLat=":
                if not string==str1:
                    string=string+"&"
                string+=place["direction"][:-1]+"&"+lat["direction"][:-1]+"&"+log["direction"][:-1]
                if location_string:
                    location_string+=" and "
                location_string+=str(dirs[0])+place["direction"][18:-1]

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
    # else:
    #     if not string==str1:
    #         string=string+"&"
    #     string=string+"propType="+"APARTMENT"    
    
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
                    if item in ["of","at","around","near","nearby","from"]:
                        minimumprice=min(budget_modified)*0.7
                        maximumprice=max(budget_modified)*1.3
                        flag=1
                        break
                    elif item in ["within","less","below","under","max","maximum","in"]:
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
    logString = "\n"
    ###################### Feedback Formation ################################
    feedback_string=""
    if project_name:
        feedback_string+="for "+str(project_name)+" "

    if bhk:
        feedback_string+="of size "
        bhk=list(set(bhk))
        for b in bhk:
            feedback_string+=b+","
        feedback_string=feedback_string[:-1]+" bhk "

    if budget:
        if minimumprice:
            feedback_string+="within "
            if minimumprice/10000000 >= 1:
                feedback_string+=str(minimumprice/10000000)+"Cr "
            else:
                feedback_string+=str(minimumprice/100000)+"Lac "

            if maximumprice:
                feedback_string+="to "
                if maximumprice/10000000 >= 1:
                    feedback_string+=str(maximumprice/10000000)+"Cr "
                else:
                    feedback_string+=str(maximumprice/100000)+"Lac "

        if maximumprice and not minimumprice:
            feedback_string+="within "
            if maximumprice/10000000 >= 1:
                    feedback_string+=str(maximumprice/10000000)+"Cr "
            else:
                    feedback_string+=str(maximumprice/100000)+"Lac "

    if location_string:
        feedback_string+=location_string
    print feedback_string,string



    try:
        logString = logString + starttime + " ; " + str(todo_id) + " ; " + string + " ; "

        with open(fileName,"a") as myFile:
            myFile.write(logString)
            myFile.close()
    except:
        pass

    return string,feedback_string



if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=6020)
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()


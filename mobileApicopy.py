from flask import Flask,request,jsonify
from NLP import *
from GooglePlaceDetailAPI import *
import requests
import urllib2
from gevent.wsgi import WSGIServer
app = Flask(__name__)
# api = Api(app)
import pdb
import time
from flask_cors import CORS,cross_origin
import datetime

fileName = "mobileAPI"  + str(datetime.date.today().month ) + str(datetime.date.today().year)



CORS(app)
@app.route('/')
def get():
    starttime = time.time()
    preference=[]
    preference_dict={}
    todo_id=request.args['searchstring']
    amenity_exclusion=["park","garden","gas","pipeline","gate","sports","manor","park","old","golf","mandir","gurudwara","garden","park","mall","pooja","jog","pent","jacuuzi","jacuzi","vaastu","dargah","puja"]
    try:
        token_id = request.headers.get('token_id')
        if(token_id == None):
            token_id= '12345'
    except:
        token_id = '12345'
    print "token_id",token_id
    print "todo_id ",todo_id
    [query,bhk,bhk_desc,apt_type,budget,budget_item,budget_desc,amenities,location,possession,possession_desc,date,project_id]=start(todo_id)

    total_budget=0
    if budget_desc:
        for item in budget_desc:
            if item in ["cheap","low"]:
                total_budget=1000000
            if item in ["delux","posh","costly"]:
                total_budget=10000000
    
    if budget :
        try: 
            total_budget=float(budget[0])
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
        preference_dict['budget']=total_budget
        
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


            preference_dict['possession']=poss


    string = "http://api.hdfcred.net/mobile_v3/project_listing_v3/?"
    str1=string
    lat=[]
    log=[]
    cityid=[]
    places_found=[]
    if location:
        for item in location:
            if not item in amenity_exclusion:
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
            preference_dict['latitude']=''
            preference_dict['longitude']=''
            preference_dict['suggestionareaname']=''

            if not string==str1:
                string=string+"&"
            string=string+"latitude="

            for item in lat:
                string=string+str(item)+","
                preference_dict['latitude']=preference_dict['latitude']+str(item)+","
            preference_dict['latitude']=preference_dict['latitude'][:-1]
            
            string=string[:-1]+"&longitude="
            for item in log:
                string=string+str(item)+","
                preference_dict['longitude']=preference_dict['longitude']+str(item)+","
            string=string[:-1]+"&suggestionareaname="
            
            preference_dict['longitude']=preference_dict['longitude'][:-1]
            for item in places_found:
                string=string+str(item.title())+"$$"
                preference_dict['suggestionareaname']=preference_dict['suggestionareaname']+str(item.title())+"$$"
            string=string[:-2]
            preference_dict['suggestionareaname']=preference_dict['suggestionareaname'][:-2]

        if cityid:
            if not string==str1:
                string=string+"&"
            string=string+"cityid="+max(cityid)
            preference_dict['cityid']=max(cityid)

    if apt_type:
        if not string==str1:
            string=string+"&"
        string=string+"propertytype="+apt_type[0]
        preference_dict['propertytype']=apt_type[0]
    else:
        if not string==str1:
            string=string+"&"
        string=string+"propertytype="+"APARTMENT"
        preference_dict['propertytype']="APARTMENT"
    
    if project_id:
        if not string==str1:
            string=string+"&"
        string+="projectid="
        for item in project_id: 
            string+=item+","
        string=string[:-1]
    
    if bhk:
        if not string==str1:
            string=string+"&"
        string=string+"bhk="+str(min(bhk))
        preference_dict['bhk']=str(min(bhk))
    elif bhk_desc:
        for item in bhk_desc:
            if item in ["small","tiny"]:
                if not string==str1:
                    string=string+"&"
                string=string+"bhk=2"
                preference_dict['bhk']="2"
                break
            if item in ["big","huge","large"]:
                if not string==str1:
                    string=string+"&"
                string=string+"bhk=4"
                preference_dict['bhk']="4"
                break

    if total_budget:
        if not string==str1:
            string=string+"&"
        string=string+"budget="+str(total_budget)
        preference_dict['budget']=total_budget
        
    if amenities:
        preference_dict['amenities']=''    
        if not string==str1:
            string=string+"&"
        string=string+"amenityid="
        for item in amenities:
            string=string+str(item)+","
            preference_dict['amenities']=preference_dict['amenities']+str(item)+","
        string=string[:-1]
        preference_dict['amenities']=preference_dict['amenities'][:-1]
    if not string==str1:
            string=string+"&"
    string=string+"possession="+str(poss)+"&position=Location,Budget,Size,Possession,Amenities&limit=0,30"
    preference_dict["position"]="Location,Budget,Size,Possession,Amenities"
    preference_dict["limit"]= "0,30"
    print string
    preference.append(preference_dict)
    print preference
    stringformationtime = time.time()
    logString= "\n"
    try:
        for a in [starttime,query,bhk,bhk_desc,apt_type,budget,budget_item,budget_desc,amenities,location,possession,possession_desc,date,lat,log]:
            logString =  logString + str(a) + ";"

        with open(fileName,"a") as myFile:
            myFile.write(logString)
    except:
        pass
    results = requests.get(string, params = {},headers={"token_id":token_id})
    try :
        result =  results.json()

    except:
         result = {
"data": [],
"msg": "zero projects", 
"status": 0, 
"total": 0,
}    
    jtime = time.time()
#    print "NLP time " , nlptime-starttime
#    print  "stringForm  " , stringformationtime - nlptime
#    print "jtime  " ,  jtime - stringformationtime
    print "total Time " , jtime - starttime
    result['preference'] = preference
    result['url'] = string
    return jsonify(result)



if __name__ == '__main__':
#    app.run(host='0.0.0.0',port=6020)
    http_server = WSGIServer(('0.0.0.0', 6030), app)
    http_server.serve_forever()


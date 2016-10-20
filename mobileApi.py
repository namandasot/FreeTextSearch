from flask import Flask,request,jsonify
from NLP import *
from GooglePlaceDetailAPI import *
import requests
app = Flask(__name__)
# api = Api(app)
import pdb
import time
# class TodoSimple(Resource):
@app.route('/')
def get():
    starttime = time.time()
    preference=[]
    preference_dict={}
    todo_id=request.args['searchstring']
    try:
        token_id = request.headers.get('token_id')
        if(token_id == None):
            token_id= '12345'
    except:
        token_id = '12345'
    print "token_id",token_id
    print "todo_id ",todo_id
    [query,bhk,bhk_desc,apt_type,budget,budget_item,budget_desc,amenities,location,possession,possession_desc,date]=start(todo_id)
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
        preference_dict['budget']=total_budget
        
    poss=0
    if possession:
        if date:
            if date[0] in ['year','yr','yrs','years']:
                if possession_desc[0] in ["more"]:
                    if int(max(possession)) <=1:
                        poss=4
                    if  int(max(possession)) >1 and int(max(possession)) <=2:
                        poss=5
                    if  int(max(possession)) >2:
                        poss=6

                else:
                    if int(max(possession)) <=1:
                        poss=3
                    if  int(max(possession)) >1 and int(max(possession)) <=2:
                        poss=4
                    if  int(max(possession)) >2 and int(max(possession)) <=3:
                        poss=5
                    if  int(max(possession)) >3 :
                        poss=6
            if date[0] in ['month','months','mnth','mnths']:
                if possession_desc[0] in ["more"]:
                    poss=2
                else:
                    if int(max(possession)) <6:
                        poss=0
                    if int(max(possession)) >=6:
                        poss=2
            preference_dict['possession']=poss

    nlptime = time.time()

    string = "http://api.hdfcred.net/mobile_v3/project_listing_v3/?"
    str1=string
    lat=[]
    log=[]
    if location:
        if not string==str1:
            string=string+"&"
        for item in location:
            [geoLatitude,geoLongitude,address]=start123(item)
            lat.append(geoLatitude)
            log.append(geoLongitude)
        if not string==str1:
            string=string+"&"
        string=string+"lat="
        preference_dict['latitude']=''
        preference_dict['longitude']=''
        preference_dict['suggestionareaname']=''
        for item in lat:
            string=string+str(item)+","
            preference_dict['latitude']=preference_dict['latitude']+str(item)+","
        preference_dict['latitude']=preference_dict['latitude'][:-1]
        string=string[:-1]+"&long="
        for item in log:
            string=string+str(item)+","
            preference_dict['longitude']=preference_dict['longitude']+str(item)+","
        string=string[:-1]+"&areas="
        preference_dict['longitude']=preference_dict['longitude'][:-1]
        for item in location:
            string=string+str(item)+"$$"
            preference_dict['suggestionareaname']=preference_dict['suggestionareaname']+str(item)+"$$"
        string=string[:-2]
        preference_dict['suggestionareaname']=preference_dict['suggestionareaname'][:-2]

    if apt_type:
        if not string==str1:
            string=string+"&"
        string=string+"propertytype="+apt_type[0]
        preference_dict['propertytype']=apt_type[0]
    
    if bhk_desc:
        for item in bhk_desc:
            if item in ["small","tiny"]:
                bhk.append(2)
            if item in ["big","huge","large"]:
                bhk.append(4)
    if bhk:
        if not string==str1:
            string=string+"&"
        string=string+"bhk="+str(min(bhk))
        preference_dict['bhk']=str(min(bhk))

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
    results = requests.get(string, params = {},headers={"token_id":token_id})
    try :
        result =  results.json()
    #return jsonify({'mssg':"success","status":1,'total':len(result),'data':result,'preference':preference,'url':string})

    except:
         result = {
"data": [],
"msg": "zero projects", 
"status": 0, 
"total": 0,
"Faalt" :0
}    
    jtime = time.time()
    print "NLP time " , nlptime-starttime
    print  "stringForm  " , stringformationtime - nlptime
    print "jtime  " ,  jtime - stringformationtime
    print "total Time " , jtime - starttime
    return jsonify(result)
    # return {"text":todo_id,"string":string,"apt_type":apt_type,"BHK":bhk,"Budget":total_budget,"Amenities":amenities,"Location":location,"Possession":possession}


# api.add_resource(TodoSimple, '/searchstring=<todo_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=6020)



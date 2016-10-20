from flask import Flask,request,jsonify
from NLP import *
from GooglePlaceDetailAPI import *
import requests
app = Flask(__name__)
# api = Api(app)


# class TodoSimple(Resource):
@app.route('/')
def get():
    #Location,Possession
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
    print "++++++++++++++++++++++++++++++++++++"
    print location
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
    
    string = "http://api.hdfcred.net/mobile_v3/project_listing_v3/?"
    str1=string
    lat=[]
    log=[]
    print location
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
        for item in lat:
            string=string+str(item)+","
        string=string[:-1]+"&long="
        for item in log:
            string=string+str(item)+","
        string=string[:-1]+"&areas="
        for item in location:
            string=string+item+"$$"
        string=string[:-2]

    if apt_type:
        if not string==str1:
            string=string+"&"
        string=string+"propertytype="+apt_type[0]
    
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
    string=string+"possession="+str(poss)+"&position=Budget,Amenities,Location,Size,Possession&limit=0,20"
    string+="&order=P_Min_Price&order_type=DESC"
    print string
    
    results = requests.get(string, params = {},headers={"token_id":token_id})
    return jsonify(results.json())
    return jsonify({
"data": [], 
"msg": "zero projects", 
"status": 0, 
"total": 0,
"Faalt" :0
})
    # return {"text":todo_id,"string":string,"apt_type":apt_type,"BHK":bhk,"Budget":total_budget,"Amenities":amenities,"Location":location,"Possession":possession}


# api.add_resource(TodoSimple, '/searchstring=<todo_id>')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=6020)



# import sys
import pandas as pd
# import nltk
# from nltk.parse import stanford
# from nltk.parse import RecursiveDescentParser as rd
# from nltk.parse import malt
from nltk.internals import find_jar, config_java, java, _java_options, find_jars_within_path
import os
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse import stanford
import string
from nltk.tag import pos_tag
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
# import argparse
from googleapiclient import discovery
import httplib2
import json
from oauth2client.client import GoogleCredentials
import time
# import MySQLdb

os.environ.get('CLASSPATH')

start = time.time()
os.environ['STANFORD_PARSER'] = '/home/ubuntu/nltk_data/models/stanford-parser-full-2015-04-20/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = '/home/ubuntu/nltk_data/models/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar'
#parser = stanford.StanfordParser("/home/kiran/nltk_data/stanford-parser-python-r22186/3rdParty/stanford-parser/englishPCFG.July-2010.ser", java_options='-mx1000m')
parser=stanford.StanfordParser()
#stanford_dir = parser._classpath[0].rpartition('/')[0]
#parser._classpath = tuple(find_jars_within_path(stanford_dir))
DISCOVERY_URL = ('https://{api}.googleapis.com/'
                 '$discovery/rest?version={apiVersion}')


def Cleaning(words):
    words.append([word.lower() for word in phrases])



def BHK(word,tagged_words):
    BHK=['bedroom','rk','kitchen','bathroom','bhk','room','rooms','hall','bedrooms','house',"flat"]
    leafs=[]
    adj=[]
    item1=[]      

    for item in BHK:
         if item in word:
             length=len(tagged_words)-1
             pos=word.index(item)
             item1.append(item)
             # if tagged_words[pos][0] == '<':
             #                 adj.append('less')
             # if tagged_words[pos][0] == '>':
             #                 adj.append('more')
             # if tagged_words[pos][1] == 'CD':
             #                 leafs.append(tagged_words[pos][0])
                             
                         
             # if (tagged_words[pos][1]=="JJ") or (tagged_words[pos][1]=="JJR") or (tagged_words[pos][1]=="JJS"):
             #             adj.append(tagged_words[pos][0])
             
             if not pos-1<0:
                 if tagged_words[pos-1][0] == '<':
                             adj.append('less')
                 elif tagged_words[pos-1][0] == '>':
                             adj.append('more')
                 elif tagged_words[pos-1][1] == 'CD':
                             leafs.append(tagged_words[pos-1][0])
                         
                 elif (tagged_words[pos-1][1]=="JJ") or (tagged_words[pos-1][1]=="JJR") or (tagged_words[pos-1][1]=="JJS"):
                         adj.append(tagged_words[pos-1][0])
             
             # if not pos+1>length:
             #     if tagged_words[pos+1][1] == 'CD':
             #                 leafs.append(tagged_words[pos+1][0])
                         
             #     if (tagged_words[pos+1][1]=="JJ") or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
             #             adj.append(tagged_words[pos+1][0])
                         
             if not pos-2<0:
                 if tagged_words[pos-2][0] == '<':
                             adj.append('less')
                 elif tagged_words[pos-2][0] == '>':
                             adj.append('more')
                 elif tagged_words[pos-2][1] == 'CD':
                             leafs.append(tagged_words[pos-2][0])
                         
                 elif (tagged_words[pos-2][1]=="JJ") or (tagged_words[pos-2][1]=="JJR") or (tagged_words[pos-2][1]=="JJS"):
                         adj.append(tagged_words[pos-2][0])
                         
             if not pos-3<0:
                 if tagged_words[pos-3][0] == '<':
                             adj.append('less')
                 elif tagged_words[pos-3][0] == '>':
                             adj.append('more')
                 elif tagged_words[pos-3][1] == 'CD':
                             leafs.append(tagged_words[pos-3][0])
                         
                 elif (tagged_words[pos-3][1]=="JJ") or (tagged_words[pos-3][1]=="JJR") or (tagged_words[pos-3][1]=="JJS"):
                         adj.append(tagged_words[pos-3][0])
    if not leafs:
        leafs+=''
    if not adj:
        adj+=''
    if not item1:
        item1+=''
    #print leafs,adj
    return ([leafs,adj,item1])


def Budget(word,tagged_words):
    budget=['lac','l','lakh','cr','crore','lacs','lakhs','crores','million' ]
    BHK=['bedroom','rk','kitchen','bathroom','bhk','room','rooms','hall','bedrooms','house',"flat"]
    leafs=[]
    adj=[] 
    word1=[]
    item1=[]


    word1=tagged_words
    for w in word1:            
        if w[1]=="CD":               
            try:
                if int(w[0])>100000:
                     
                     pos=word1.index(w)
                     leafs.append(w[0])
                     length=len(tagged_words)-1

                                 
                     if not pos-1<0:
                         if tagged_words[pos-1][0] == '<':
                                         adj.append('less')
                         elif tagged_words[pos-1][0] == '>':
                                         adj.append('more')                                           
                         elif (tagged_words[pos-1][1]=="RB") or (tagged_words[pos-1][1]=="RBR") or (tagged_words[pos-1][1]=="RBS") or (tagged_words[pos-1][1]=="IN"):
                                 adj.append(tagged_words[pos-1][0])
                         elif (tagged_words[pos-1][1]=="JJ") or (tagged_words[pos-1][1]=="JJR") or (tagged_words[pos-1][1]=="JJS"):
                                adj.append(tagged_words[pos-1][0])

                     
                     if not pos+1>length:
                         if tagged_words[pos+1][0] == '<':
                                         adj.append('less')
                         elif tagged_words[pos+1][0] == '>':
                                         adj.append('more')
                         elif (tagged_words[pos+1][1]=="RB") or (tagged_words[pos+1][1]=="RBR") or (tagged_words[pos+1][1]=="RBS") or (tagged_words[pos+1][1]=="IN"):
                                 adj.append(tagged_words[pos+1][0])
                         elif (tagged_words[pos+1][1]=="JJ") or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
                                adj.append(tagged_words[pos+1][0])

                                 
                     if not pos-2<0:                                             
                         if tagged_words[pos-2][0] == '<':
                                         adj.append('less')
                         elif tagged_words[pos-2][0] == '>':
                                         adj.append('more')
                         elif (tagged_words[pos-2][1]=="RB") or (tagged_words[pos-2][1]=="RBR") or (tagged_words[pos-2][1]=="RBS") or (tagged_words[pos-2][1]=="IN"):
                                 adj.append(tagged_words[pos-2][0])
                         elif (tagged_words[pos-2][1]=="JJ") or (tagged_words[pos-2][1]=="JJR") or (tagged_words[pos-2][1]=="JJS"):
                                adj.append(tagged_words[pos-2][0])
                                 
                     if not pos+2>length:                                           
                         if tagged_words[pos+2][0] == '<':
                                         adj.append('less')
                         elif tagged_words[pos+2][0] == '>':
                                         adj.append('more')
                         elif (tagged_words[pos+2][1]=="RB") or (tagged_words[pos+2][1]=="RBR") or (tagged_words[pos+2][1]=="RBS") or (tagged_words[pos+2][1]=="IN"):
                                 adj.append(tagged_words[pos+2][0])
                         elif (tagged_words[pos+2][1]=="JJ") or (tagged_words[pos+2][1]=="JJR") or (tagged_words[pos+2][1]=="JJS"):
                                adj.append(tagged_words[pos+2][0])

                     if not pos-3<0:                                           
                         if tagged_words[pos-3][0] == '<':
                                         adj.append('less')
                         elif tagged_words[pos-3][0] == '>':
                                         adj.append('more')
                         elif (tagged_words[pos-3][1]=="RB") or (tagged_words[pos-3][1]=="RBR") or (tagged_words[pos-3][1]=="RBS") or (tagged_words[pos-3][1]=="IN"):
                                 adj.append(tagged_words[pos-3][0])
                         elif (tagged_words[pos-3][1]=="JJ") or (tagged_words[pos-3][1]=="JJR") or (tagged_words[pos-3][1]=="JJS"):
                                adj.append(tagged_words[pos-3][0])
          
                     #break
                    
            except:
                print"error"
                        

                  
                        
    
    
    for pos,item in enumerate(word) :
         if item in budget:
             length=len(tagged_words)-1
             item1.append(item)
                         
             if not pos-1<0:
                 if tagged_words[pos-1][0] in BHK:
                    continue
                 elif tagged_words[pos-1][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos-1][0] == '>':
                                         adj.append('more')
                 elif tagged_words[pos-1][1] == 'CD':
                             leafs.append(tagged_words[pos-1][0])

                         
                 elif (tagged_words[pos-1][1]=="JJ") or (tagged_words[pos-1][1]=="JJR") or (tagged_words[pos-1][1]=="JJS"):
                         adj.append(tagged_words[pos-1][0])
                         
                 elif (tagged_words[pos-1][1]=="RB") or (tagged_words[pos-1][1]=="RBR") or (tagged_words[pos-1][1]=="RBS") or (tagged_words[pos-1][1]=="IN"):
                         adj.append(tagged_words[pos-1][0])
             
             if not pos+1>length:
                 if tagged_words[pos+1][0] in BHK:
                    continue
                 elif tagged_words[pos+1][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos+1][0] == '>':
                                         adj.append('more')
                 elif tagged_words[pos+1][1] == 'CD':
                             leafs.append(tagged_words[pos+1][0])
                         
                 elif (tagged_words[pos+1][1]=="JJ") or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
                         adj.append(tagged_words[pos+1][0])
                         
                 elif (tagged_words[pos+1][1]=="RB") or (tagged_words[pos+1][1]=="RBR") or (tagged_words[pos+1][1]=="RBS") or (tagged_words[pos+1][1]=="IN"):
                         adj.append(tagged_words[pos+1][0])
                         
             if not pos-2<0:
                 if tagged_words[pos-2][0] in BHK:
                    continue
                 elif tagged_words[pos-2][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos-2][0] == '>':
                                         adj.append('more')
                 elif tagged_words[pos-2][1] == 'CD':
                             leafs.append(tagged_words[pos-2][0])
                         
                 elif (tagged_words[pos-2][1]=="JJ") or (tagged_words[pos-2][1]=="JJR") or (tagged_words[pos-2][1]=="JJS"):
                         adj.append(tagged_words[pos-2][0])
                         
                 elif (tagged_words[pos-2][1]=="RB") or (tagged_words[pos-2][1]=="RBR") or (tagged_words[pos-2][1]=="RBS") or (tagged_words[pos-2][1]=="IN"):
                         adj.append(tagged_words[pos-2][0])

             if not pos-3<0:
                 if tagged_words[pos-3][0] in BHK:
                    continue
                 elif tagged_words[pos-3][1] == 'CD':
                             leafs.append(tagged_words[pos-3][0])
                         
                 elif tagged_words[pos-3][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos-3][0] == '>':
                                         adj.append('more')
                 elif (tagged_words[pos-3][1]=="JJ") or (tagged_words[pos-3][1]=="JJR") or (tagged_words[pos-3][1]=="JJS"):
                         adj.append(tagged_words[pos-3][0])
                         
                 elif (tagged_words[pos-3][1]=="RB") or (tagged_words[pos-3][1]=="RBR") or (tagged_words[pos-3][1]=="RBS") or (tagged_words[pos-3][1]=="IN"):
                         adj.append(tagged_words[pos-3][0])

             if not pos+2>length:
                 if tagged_words[pos+2][0] in BHK:
                    continue
                 elif tagged_words[pos+2][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos+2][0] == '>':
                                         adj.append('more')
                 elif tagged_words[pos+2][1] == 'CD':
                             leafs.append(tagged_words[pos+2][0])

                         
                 elif (tagged_words[pos+2][1]=="JJ") or (tagged_words[pos+2][1]=="JJR") or (tagged_words[pos+2][1]=="JJS"):
                         adj.append(tagged_words[pos+2][0])
                         
                 elif (tagged_words[pos+2][1]=="RB") or (tagged_words[pos+2][1]=="RBR") or (tagged_words[pos+2][1]=="RBS") or (tagged_words[pos+2][1]=="IN"):
                         adj.append(tagged_words[pos+2][0])

    
    if not leafs:
        leafs+=''
    if not adj:
        adj+=''
    if not item1:
        item1+=''                     
    return ([leafs,adj,item1])
    
def Location(words,tagged_words): ##
  adv=[]
  item1=[]
  http = httplib2.Http()
  credentials = GoogleCredentials.get_application_default().create_scoped(
                ['https://www.googleapis.com/auth/cloud-platform'])
  credentials.authorize(http)


  service = discovery.build('language', 'v1beta1',
                            http=http, discoveryServiceUrl=DISCOVERY_URL)

  service_request = service.documents().analyzeEntities(
    body={
      'document': {
         'type': 'PLAIN_TEXT',
         'content': words,
      }
    })

  response = service_request.execute()

  try:
    words=words.lower().split()
    length=len(tagged_words)-1
    for i in range (0,len(response['entities'])):
      if response['entities'][i]['type']=='LOCATION':
                 item1.append(response['entities'][i]['name'])
                 pos=words.index(response['entities'][i]['name'].split()[0].lower())
            
                 if not pos-1<0:                            
                     if (tagged_words[pos-1][1]=="RB") or (tagged_words[pos-1][1]=="RBR") or (tagged_words[pos-1][1]=="RBS") or (tagged_words[pos-1][1]=="IN")  or (tagged_words[pos-1][1]=="JJR") or (tagged_words[pos-1][1]=="JJS"):
                             adv.append(tagged_words[pos-1][0])
                 
                 if not pos+1>length:                                  
                     if (tagged_words[pos+1][1]=="RB") or (tagged_words[pos+1][1]=="RBR") or (tagged_words[pos+1][1]=="RBS") or (tagged_words[pos+1][1]=="IN")  or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
                             adv.append(tagged_words[pos+1][0])
                             
                 if not pos-2<0:         
                     if (tagged_words[pos-2][1]=="RB") or (tagged_words[pos-2][1]=="RBR") or (tagged_words[pos-2][1]=="RBS") or (tagged_words[pos-2][1]=="IN")  or (tagged_words[pos-2][1]=="JJR") or (tagged_words[pos-2][1]=="JJS"):
                             adv.append(tagged_words[pos-2][0])

                 if not pos-3<0:        
                     if (tagged_words[pos-3][1]=="RB") or (tagged_words[pos-3][1]=="RBR") or (tagged_words[pos-3][1]=="RBS") or (tagged_words[pos-3][1]=="IN")  or (tagged_words[pos-3][1]=="JJR") or (tagged_words[pos-3][1]=="JJS"):
                             adv.append(tagged_words[pos-3][0])
                             
                 if not pos+2>length:                  
                     if (tagged_words[pos+2][1]=="RB") or (tagged_words[pos+2][1]=="RBR") or (tagged_words[pos+2][1]=="RBS") or (tagged_words[pos+2][1]=="IN") or (tagged_words[pos+2][1]=="JJR") or (tagged_words[pos+2][1]=="JJS"):
                             adv.append(tagged_words[pos+2][0])
  except:
    print "Error"

  if not adv:
        adv+=''
  if not item1:
        item1+=''                     
  return ([item1,adv])



def Possession(word,tagged_words):
    pos_type=['year','yr','yrs','years','month','months','mnth','mnths','available','ready','possession']
    budget=['lac','l','lakh','cr','crore','lacs','lakhs','crores','million' ]
    BHK=['bedroom','rk','kitchen','bathroom','bhk','room','rooms','hall','bedrooms','house',"flat"]
    item1=[]
    leafs=[]
    adj=[]

    
    for item in pos_type:
        if item in word:
             length=len(tagged_words)-1
             pos=word.index(item)
             item1.append(item)
             # print tagged_words
             if not pos-1<0:
                 if tagged_words[pos-1][0] in BHK or tagged_words[pos-1][0] in budget:
                    continue
                 elif tagged_words[pos-1][0] in ["a","an"] and not leafs:
                    leafs.append("1")

                 elif tagged_words[pos-1][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos-1][0] == '>':
                                         adj.append('more')

                 
                 elif tagged_words[pos-1][1] == 'CD':
                             leafs.append(tagged_words[pos-1][0])
                         
                 elif (tagged_words[pos-1][1]=="RB") or (tagged_words[pos-1][1]=="RBR") or (tagged_words[pos-1][1]=="RBS") or (tagged_words[pos-1][1]=="IN") or (tagged_words[pos-1][1]=="JJR"):
                         adj.append(tagged_words[pos-1][0])
             
             # if not pos+1>length:
             #     if tagged_words[pos+1][1] == 'CD':
             #                 leafs.append(tagged_words[pos+1][0])
                         
             #     if (tagged_words[pos+1][1]=="JJ") or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
             #             adj.append(tagged_words[pos+1][0])
                         
             if not pos-2<0:
                 if tagged_words[pos-2][0] in BHK or  tagged_words[pos-2][0] in budget:
                    continue
                 elif tagged_words[pos-2][0] in ["a","an"] and not leafs:
                    leafs.append("1")
                 elif tagged_words[pos-2][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos-2][0] == '>':
                                         adj.append('more')
                 elif tagged_words[pos-2][1] == 'CD':
                             leafs.append(tagged_words[pos-2][0])
                         
                 elif (tagged_words[pos-2][1]=="RB") or (tagged_words[pos-2][1]=="RBR") or (tagged_words[pos-2][1]=="RBS") or (tagged_words[pos-2][1]=="IN") or (tagged_words[pos-2][1]=="JJR"):
                         adj.append(tagged_words[pos-2][0])
                         
             if not pos-3<0:
                 if tagged_words[pos-3][0] in BHK or tagged_words[pos-3][0] in budget:
                    continue

                 elif tagged_words[pos-3][0] in ["a","an"] and not leafs:
                    leafs.append("1")

                 elif tagged_words[pos-3][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos-3][0] == '>':
                                         adj.append('more')
                 elif tagged_words[pos-3][1] == 'CD':
                             leafs.append(tagged_words[pos-3][0])
                         
                 elif (tagged_words[pos-3][1]=="RB") or (tagged_words[pos-3][1]=="RBR") or (tagged_words[pos-3][1]=="RBS") or (tagged_words[pos-3][1]=="IN" or (tagged_words[pos-3][1]=="JJR")):
                         adj.append(tagged_words[pos-3][0])

    #print tagged_words                        
    if not leafs:
        leafs+=''
    if not adj:
        adj+=''
    if not item1:
        item1+=''                     
    return ([leafs,adj,item1])


def Area(word,tagged_words):
    pos_type=['year','years','yr','yrs','month','months','mnth','mnths']
    budget=['lac','l','lakh','cr','crore','lacs','lakhs','crores','million' ]
    BHK=['bedroom','rk','kitchen','bathroom','bhk','room','rooms','hall','bedrooms','house',"flat"]
    area=['sqft','sft','area','ft','meter','mtrsqr','metersquare']
    item1=[]
    leafs=[]
    adj=[]

    
    for item in area:
        if item in word:
             length=len(tagged_words)-1
             pos=word.index(item)
             item1.append(item)
             if not pos-1<0:
                 if tagged_words[pos-1][0] in BHK or tagged_words[pos-1][0] in budget or tagged_words[pos-1][0] in pos_type:
                    continue

                 elif tagged_words[pos-1][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos-1][0] == '>':
                                         adj.append('more')

                 
                 elif tagged_words[pos-1][1] == 'CD':
                             leafs.append(tagged_words[pos-1][0])
                         
                 elif (tagged_words[pos-1][1]=="RB") or (tagged_words[pos-1][1]=="RBR") or (tagged_words[pos-1][1]=="RBS") or (tagged_words[pos-1][1]=="IN") or (tagged_words[pos-1][1]=="JJR"):
                         adj.append(tagged_words[pos-1][0])
             
             # if not pos+1>length:
             #     if tagged_words[pos+1][1] == 'CD':
             #                 leafs.append(tagged_words[pos+1][0])
                         
             #     if (tagged_words[pos+1][1]=="JJ") or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
             #             adj.append(tagged_words[pos+1][0])
                         
             if not pos-2<0:
                 if tagged_words[pos-2][0] in BHK or  tagged_words[pos-2][0] in budget or tagged_words[pos-2][0] in pos_type:
                    continue
                 elif tagged_words[pos-2][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos-2][0] == '>':
                                         adj.append('more')
                 elif tagged_words[pos-2][1] == 'CD':
                             leafs.append(tagged_words[pos-2][0])
                         
                 elif (tagged_words[pos-2][1]=="RB") or (tagged_words[pos-2][1]=="RBR") or (tagged_words[pos-2][1]=="RBS") or (tagged_words[pos-2][1]=="IN") or (tagged_words[pos-2][1]=="JJR"):
                         adj.append(tagged_words[pos-2][0])
                         
             if not pos-3<0:
                 if tagged_words[pos-3][0] in BHK or tagged_words[pos-3][0] in budget or tagged_words[pos-3][0] in pos_type:
                    continue

                 elif tagged_words[pos-3][0] == '<':
                                         adj.append('less')
                 elif tagged_words[pos-3][0] == '>':
                                         adj.append('more')
                 elif tagged_words[pos-3][1] == 'CD':
                             leafs.append(tagged_words[pos-3][0])
                         
                 elif (tagged_words[pos-3][1]=="RB") or (tagged_words[pos-3][1]=="RBR") or (tagged_words[pos-3][1]=="RBS") or (tagged_words[pos-3][1]=="IN" or (tagged_words[pos-3][1]=="JJR")):
                         adj.append(tagged_words[pos-3][0])

    #print tagged_words                        
    if not leafs:
        leafs+=''
    if not adj:
        adj+=''
    if not item1:
        item1+=''                     
    return ([leafs,adj,item1])



def AptType(word):
    apartment=["apartment","flat"]
    villa=["bunglow","villa"]
    plot=["land","plot"]
    result=[]    

    for apt in apartment:
            if apt in word:
                result.append("APARTMENT")
    for apt in villa:
            if apt in word:
                result.append("VILLA")
    for apt in plot:
            if apt in word:
                result.append("PLOT")


    return(result)                

def Amenities(word):
    amenities=pd.read_csv('amenities.csv',index_col=None, header=0)
    result=[]    
    for pos,rows in enumerate(amenities['Ammenities_Keyword']):
                items=rows.split()
                for item in items:
                    #print "ITEM",item
                    if str(item) in word:
                        #print amenities['Amenity_Desc'][pos]
                        result.append(amenities['Amenity_code'][pos])
                
    return(list(set(result)))
    


def start(query):
    num_dict={"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20,"thirty":30,"fourty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90,"hundred":100}

    m_s=[]
    for word in query.split():
        if word in num_dict.keys():m_s.append(num_dict[word]) 
        else: m_s.append(word)

    modified=[]
    for i,item in enumerate(m_s):
            if type(item)is int:
                try:
                    if type(m_s[i+1]) is int:
                        item+=m_s[i+1]
                        del m_s[i+1]
                except:
                    print "error"
            modified.append(item)

    string1=""
    for i,item in enumerate(modified):
            if item==100 :
                try:
                    if modified[i+1]=="and" and type(modified[i+2]) is int:
                        item+=modified[i+2]
                        del modified[i+1]
                        del modified[i+1]
                except:
                    print "error"
            if type(item) is int:
                try:
                    if modified[i+1]=="point" and type(modified[i+2]) is int:
                        item=str(item)+"."+str(modified[i+2])
                        del modified[i+1]
                        del modified[i+1]
                except:
                    print "error"
            string1+=" "+str(item)
  
    query=string1
    
    print query
    ls = []
    for x in query:

         if x in string.punctuation and not x=='.' and not x=='>' and not x=='<':
                ls.append(' ')
         else:
            ls.append(x)

    query="".join(ls)
    #Adding space between digits and words
    w=re.split('(\d+\.?\d*)',query)
    query=" ".join(w)

    #Converting to Lower Case
    query = str(query.lower())
    words=word_tokenize(query)


    tagged_words=pos_tag(words)
    [bhk,bhk_desc,bhk_item]=BHK(words,tagged_words)      
    [budget,budget_adj,budget_item]=Budget(words,tagged_words)
    [possession,possession_desc,date]=Possession(words,tagged_words)
    [area,area_type,dim]=Area(words,tagged_words)

    st=PorterStemmer()
    stemmed_words=[words for words in query.split()] 
    apt_type=AptType(stemmed_words)

    amenities=Amenities(stemmed_words)

    #query = str(query.upper())
    qr_mod=[]
    for word in tagged_words:
        if word[1] in ["NN","NNP","NNS","RB","RBR","RBS","JJ","JJR","JJS"]:
            qr_mod.append(word[0].title())
        else:
            qr_mod.append(word[0].lower())
    query=' '.join(qr_mod) 
    [location,adv_location]=Location(query,tagged_words)

    print "BHK ", bhk,bhk_desc,bhk_item
    print "BUDGET " ,budget,budget_adj,budget_item
    print "LOCATION",location,adv_location
    print "POSSESSION",possession,possession_desc,date
    print "TYPE",apt_type   
    print "AMENITIES",amenities     
    print "AREA",area,area_type,dim

    end = time.time()
    #print "TIME",end - start
    return query,bhk,bhk_desc,apt_type,budget,budget_item,budget_adj,amenities,location,possession,possession_desc,date

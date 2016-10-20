import sys
import pandas as pd
import nltk
from nltk.parse import stanford
from nltk.parse import RecursiveDescentParser as rd
from nltk.parse import malt
from nltk.internals import find_jar, config_java, java, _java_options, find_jars_within_path
import os
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse import stanford
import string
from nltk.tag import pos_tag
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
import argparse
from googleapiclient import discovery
import httplib2
import json
from oauth2client.client import GoogleCredentials
import time
import MySQLdb

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

OOGLE_APPLICATION_CREDENTIALS='test_api.json'

def Cleaning(words):
    words.append([word.lower() for word in phrases])



def BHK(word):
    BHK=['bedroom','rk','kitchen','bathroom','bhk','room','rooms','hall','bedrooms','house',"flat"]
    leafs=[]
    adj=[]
    item1=[]      

    for item in BHK:
                     if item in word:
                         tagged_words=pos_tag(word)
                         length=len(tagged_words)-1
                         pos=word.index(item)
                         item1.append(item)
                         if tagged_words[pos][0] == '<':
                                         adj.append('less')
                         if tagged_words[pos][0] == '>':
                                         adj.append('more')
                         if tagged_words[pos][1] == 'CD':
                                         leafs.append(tagged_words[pos][0])
                                         
                                     
                         if (tagged_words[pos][1]=="JJ") or (tagged_words[pos][1]=="JJR") or (tagged_words[pos][1]=="JJS"):
                                     adj.append(tagged_words[pos][0])
                         
                         if not pos-1<0:
                             if tagged_words[pos-1][0] == '<':
                                         adj.append('less')
                             if tagged_words[pos-1][0] == '>':
                                         adj.append('more')
                             if tagged_words[pos-1][1] == 'CD':
                                         leafs.append(tagged_words[pos-1][0])
                                     
                             if (tagged_words[pos-1][1]=="JJ") or (tagged_words[pos-1][1]=="JJR") or (tagged_words[pos-1][1]=="JJS"):
                                     adj.append(tagged_words[pos-1][0])
                         
                         # if not pos+1>length:
                         #     if tagged_words[pos+1][1] == 'CD':
                         #                 leafs.append(tagged_words[pos+1][0])
                                     
                         #     if (tagged_words[pos+1][1]=="JJ") or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
                         #             adj.append(tagged_words[pos+1][0])
                                     
                         if not pos-2<0:
                             if tagged_words[pos-2][0] == '<':
                                         adj.append('less')
                             if tagged_words[pos-2][0] == '>':
                                         adj.append('more')
                             if tagged_words[pos-2][1] == 'CD':
                                         leafs.append(tagged_words[pos-2][0])
                                     
                             if (tagged_words[pos-2][1]=="JJ") or (tagged_words[pos-2][1]=="JJR") or (tagged_words[pos-2][1]=="JJS"):
                                     adj.append(tagged_words[pos-2][0])
                                     
                         if not pos-3<0:
                             if tagged_words[pos-3][0] == '<':
                                         adj.append('less')
                             if tagged_words[pos-3][0] == '>':
                                         adj.append('more')
                             if tagged_words[pos-3][1] == 'CD':
                                         leafs.append(tagged_words[pos-3][0])
                                     
                             if (tagged_words[pos-3][1]=="JJ") or (tagged_words[pos-3][1]=="JJR") or (tagged_words[pos-3][1]=="JJS"):
                                     adj.append(tagged_words[pos-3][0])
    if not leafs:
        leafs+=''
    if not adj:
        adj+=''
    if not item1:
        item1+=''
    #print leafs,adj
    return ([leafs,adj,item1])


def Budget(word):
    budget=['lac','l','lakh','cr','crore','lacs','lakhs','crores','million' ]
    BHK=['bedroom','rk','kitchen','bathroom','bhk','room','rooms','hall','bedrooms','house',"flat"]
    leafs=[]
    adj=[] 
    word1=[]
    item1=[]


    word1=pos_tag(word)
    for w in word1:            
        if w[1]=="CD":               
            try:
                if int(w[0])>100000:
                     
                     pos=word1.index(w)
                     leafs.append(w[0])
                     tagged_words=pos_tag(word)
                     length=len(tagged_words)-1

                                 
                     if not pos-1<0:
                         if tagged_words[pos-1][0] == '<':
                                         adj.append('less')
                         if tagged_words[pos-1][0] == '>':
                                         adj.append('more')                                           
                         if (tagged_words[pos-1][1]=="RB") or (tagged_words[pos-1][1]=="RBR") or (tagged_words[pos-1][1]=="RBS") or (tagged_words[pos-1][1]=="IN"):
                                 adj.append(tagged_words[pos-1][0])
                         if (tagged_words[pos-1][1]=="JJ") or (tagged_words[pos-1][1]=="JJR") or (tagged_words[pos-1][1]=="JJS"):
                                adj.append(tagged_words[pos-1][0])

                     
                     if not pos+1>length:
                         if tagged_words[pos+1][0] == '<':
                                         adj.append('less')
                         if tagged_words[pos+1][0] == '>':
                                         adj.append('more')
                         if (tagged_words[pos+1][1]=="RB") or (tagged_words[pos+1][1]=="RBR") or (tagged_words[pos+1][1]=="RBS") or (tagged_words[pos+1][1]=="IN"):
                                 adj.append(tagged_words[pos+1][0])
                         if (tagged_words[pos+1][1]=="JJ") or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
                                adj.append(tagged_words[pos+1][0])

                                 
                     if not pos-2<0:                                             
                         if tagged_words[pos-2][0] == '<':
                                         adj.append('less')
                         if tagged_words[pos-2][0] == '>':
                                         adj.append('more')
                         if (tagged_words[pos-2][1]=="RB") or (tagged_words[pos-2][1]=="RBR") or (tagged_words[pos-2][1]=="RBS") or (tagged_words[pos-2][1]=="IN"):
                                 adj.append(tagged_words[pos-2][0])
                         if (tagged_words[pos-2][1]=="JJ") or (tagged_words[pos-2][1]=="JJR") or (tagged_words[pos-2][1]=="JJS"):
                                adj.append(tagged_words[pos-2][0])
                                 
                     if not pos+2>length:                                           
                         if tagged_words[pos+2][0] == '<':
                                         adj.append('less')
                         if tagged_words[pos+2][0] == '>':
                                         adj.append('more')
                         if (tagged_words[pos+2][1]=="RB") or (tagged_words[pos+2][1]=="RBR") or (tagged_words[pos+2][1]=="RBS") or (tagged_words[pos+2][1]=="IN"):
                                 adj.append(tagged_words[pos+2][0])
                         if (tagged_words[pos+2][1]=="JJ") or (tagged_words[pos+2][1]=="JJR") or (tagged_words[pos+2][1]=="JJS"):
                                adj.append(tagged_words[pos+2][0])

                     if not pos-3<0:                                           
                         if tagged_words[pos-3][0] == '<':
                                         adj.append('less')
                         if tagged_words[pos-3][0] == '>':
                                         adj.append('more')
                         if (tagged_words[pos-3][1]=="RB") or (tagged_words[pos-3][1]=="RBR") or (tagged_words[pos-3][1]=="RBS") or (tagged_words[pos-3][1]=="IN"):
                                 adj.append(tagged_words[pos-3][0])
                         if (tagged_words[pos-3][1]=="JJ") or (tagged_words[pos-3][1]=="JJR") or (tagged_words[pos-3][1]=="JJS"):
                                adj.append(tagged_words[pos-3][0])
          
                     break
                    
            except:
                print"error"
                        

                  
                        
    
    
    for pos,item in enumerate(word) :
         if item in budget:
             tagged_words=pos_tag(word)
             length=len(tagged_words)-1
             # pos=word.index(item)
             item1.append(item)
                         
             if not pos-1<0:
                 if tagged_words[pos-1][0] in BHK:
                    continue
                 if tagged_words[pos-1][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos-1][0] == '>':
                                         adj.append('more')
                 if tagged_words[pos-1][1] == 'CD':
                             leafs.append(tagged_words[pos-1][0])

                         
                 if (tagged_words[pos-1][1]=="JJ") or (tagged_words[pos-1][1]=="JJR") or (tagged_words[pos-1][1]=="JJS"):
                         adj.append(tagged_words[pos-1][0])
                         
                 if (tagged_words[pos-1][1]=="RB") or (tagged_words[pos-1][1]=="RBR") or (tagged_words[pos-1][1]=="RBS") or (tagged_words[pos-1][1]=="IN"):
                         adj.append(tagged_words[pos-1][0])
             
             if not pos+1>length:
                 if tagged_words[pos+1][0] in BHK:
                    continue
                 if tagged_words[pos+1][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos+1][0] == '>':
                                         adj.append('more')
                 if tagged_words[pos+1][1] == 'CD':
                             leafs.append(tagged_words[pos+1][0])
                         
                 if (tagged_words[pos+1][1]=="JJ") or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
                         adj.append(tagged_words[pos+1][0])
                         
                 if (tagged_words[pos+1][1]=="RB") or (tagged_words[pos+1][1]=="RBR") or (tagged_words[pos+1][1]=="RBS") or (tagged_words[pos+1][1]=="IN"):
                         adj.append(tagged_words[pos+1][0])
                         
             if not pos-2<0:
                 if tagged_words[pos-2][0] in BHK:
                    continue
                 if tagged_words[pos-2][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos-2][0] == '>':
                                         adj.append('more')
                 if tagged_words[pos-2][1] == 'CD':
                             leafs.append(tagged_words[pos-2][0])
                         
                 if (tagged_words[pos-2][1]=="JJ") or (tagged_words[pos-2][1]=="JJR") or (tagged_words[pos-2][1]=="JJS"):
                         adj.append(tagged_words[pos-2][0])
                         
                 if (tagged_words[pos-2][1]=="RB") or (tagged_words[pos-2][1]=="RBR") or (tagged_words[pos-2][1]=="RBS") or (tagged_words[pos-2][1]=="IN"):
                         adj.append(tagged_words[pos-2][0])

             if not pos-3<0:
                 if tagged_words[pos-3][0] in BHK:
                    continue
                 if tagged_words[pos-3][1] == 'CD':
                             leafs.append(tagged_words[pos-3][0])
                         
                 if tagged_words[pos-3][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos-3][0] == '>':
                                         adj.append('more')
                 if (tagged_words[pos-3][1]=="JJ") or (tagged_words[pos-3][1]=="JJR") or (tagged_words[pos-3][1]=="JJS"):
                         adj.append(tagged_words[pos-3][0])
                         
                 if (tagged_words[pos-3][1]=="RB") or (tagged_words[pos-3][1]=="RBR") or (tagged_words[pos-3][1]=="RBS") or (tagged_words[pos-3][1]=="IN"):
                         adj.append(tagged_words[pos-3][0])

             if not pos+2>length:
                 if tagged_words[pos+2][0] in BHK:
                    continue
                 if tagged_words[pos+2][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos+2][0] == '>':
                                         adj.append('more')
                 if tagged_words[pos+2][1] == 'CD':
                             leafs.append(tagged_words[pos+2][0])

                         
                 if (tagged_words[pos+2][1]=="JJ") or (tagged_words[pos+2][1]=="JJR") or (tagged_words[pos+2][1]=="JJS"):
                         adj.append(tagged_words[pos+2][0])
                         
                 if (tagged_words[pos+2][1]=="RB") or (tagged_words[pos+2][1]=="RBR") or (tagged_words[pos+2][1]=="RBS") or (tagged_words[pos+2][1]=="IN"):
                         adj.append(tagged_words[pos+2][0])

    
    if not leafs:
        leafs+=''
    if not adj:
        adj+=''
    if not item1:
        item1+=''                     
    return ([leafs,adj,item1])
    
def Location(words): ##
  adv=[]
  item1=[]
  http = httplib2.Http()
  credentials = GoogleCredentials.get_application_default().create_scoped(
                ['https://www.googleapis.com/auth/cloud-platform'])
  http=httplib2.Http()
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
    tagged_words=pos_tag(words)
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



def Possession(word):
    pos_type=['year','yr','yrs','years','month','months','mnth','mnths','available','ready','possession']
    budget=['lac','l','lakh','cr','crore','lacs','lakhs','crores','million' ]
    BHK=['bedroom','rk','kitchen','bathroom','bhk','room','rooms','hall','bedrooms','house',"flat"]
    item1=[]
    leafs=[]
    adj=[]

    
    for item in pos_type:
        if item in word:
             tagged_words=pos_tag(word)
             length=len(tagged_words)-1
             pos=word.index(item)
             item1.append(item)
             # print tagged_words
             if not pos-1<0:
                 if tagged_words[pos-1][0] in BHK or tagged_words[pos-1][0] in budget:
                    continue
                 if tagged_words[pos-1][0] in ["a","an"] and not leafs:
                    leafs.append("1")

                 if tagged_words[pos-1][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos-1][0] == '>':
                                         adj.append('more')

                 
                 if tagged_words[pos-1][1] == 'CD':
                             leafs.append(tagged_words[pos-1][0])
                         
                 if (tagged_words[pos-1][1]=="RB") or (tagged_words[pos-1][1]=="RBR") or (tagged_words[pos-1][1]=="RBS") or (tagged_words[pos-1][1]=="IN") or (tagged_words[pos-1][1]=="JJR"):
                         adj.append(tagged_words[pos-1][0])
             
             # if not pos+1>length:
             #     if tagged_words[pos+1][1] == 'CD':
             #                 leafs.append(tagged_words[pos+1][0])
                         
             #     if (tagged_words[pos+1][1]=="JJ") or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
             #             adj.append(tagged_words[pos+1][0])
                         
             if not pos-2<0:
                 if tagged_words[pos-2][0] in BHK or  tagged_words[pos-2][0] in budget:
                    continue
                 if tagged_words[pos-2][0] in ["a","an"] and not leafs:
                    leafs.append("1")
                 if tagged_words[pos-2][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos-2][0] == '>':
                                         adj.append('more')
                 if tagged_words[pos-2][1] == 'CD':
                             leafs.append(tagged_words[pos-2][0])
                         
                 if (tagged_words[pos-2][1]=="RB") or (tagged_words[pos-2][1]=="RBR") or (tagged_words[pos-2][1]=="RBS") or (tagged_words[pos-2][1]=="IN") or (tagged_words[pos-2][1]=="JJR"):
                         adj.append(tagged_words[pos-2][0])
                         
             if not pos-3<0:
                 if tagged_words[pos-3][0] in BHK or tagged_words[pos-3][0] in budget:
                    continue

                 if tagged_words[pos-3][0] in ["a","an"] and not leafs:
                    leafs.append("1")

                 if tagged_words[pos-3][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos-3][0] == '>':
                                         adj.append('more')
                 if tagged_words[pos-3][1] == 'CD':
                             leafs.append(tagged_words[pos-3][0])
                         
                 if (tagged_words[pos-3][1]=="RB") or (tagged_words[pos-3][1]=="RBR") or (tagged_words[pos-3][1]=="RBS") or (tagged_words[pos-3][1]=="IN" or (tagged_words[pos-3][1]=="JJR")):
                         adj.append(tagged_words[pos-3][0])

    #print tagged_words                        
    if not leafs:
        leafs+=''
    if not adj:
        adj+=''
    if not item1:
        item1+=''                     
    return ([leafs,adj,item1])


def Area(word):
    pos_type=['year','years','yr','yrs','month','months','mnth','mnths']
    budget=['lac','l','lakh','cr','crore','lacs','lakhs','crores','million' ]
    BHK=['bedroom','rk','kitchen','bathroom','bhk','room','rooms','hall','bedrooms','house',"flat"]
    area=['sqft','sft','area','ft','meter','mtrsqr','metersquare']
    item1=[]
    leafs=[]
    adj=[]

    
    for item in area:
        if item in word:
             tagged_words=pos_tag(word)
             length=len(tagged_words)-1
             pos=word.index(item)
             item1.append(item)
             # print tagged_words
             if not pos-1<0:
                 if tagged_words[pos-1][0] in BHK or tagged_words[pos-1][0] in budget or tagged_words[pos-1][0] in pos_type:
                    continue

                 if tagged_words[pos-1][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos-1][0] == '>':
                                         adj.append('more')

                 
                 if tagged_words[pos-1][1] == 'CD':
                             leafs.append(tagged_words[pos-1][0])
                         
                 if (tagged_words[pos-1][1]=="RB") or (tagged_words[pos-1][1]=="RBR") or (tagged_words[pos-1][1]=="RBS") or (tagged_words[pos-1][1]=="IN") or (tagged_words[pos-1][1]=="JJR"):
                         adj.append(tagged_words[pos-1][0])
             
             # if not pos+1>length:
             #     if tagged_words[pos+1][1] == 'CD':
             #                 leafs.append(tagged_words[pos+1][0])
                         
             #     if (tagged_words[pos+1][1]=="JJ") or (tagged_words[pos+1][1]=="JJR") or (tagged_words[pos+1][1]=="JJS"):
             #             adj.append(tagged_words[pos+1][0])
                         
             if not pos-2<0:
                 if tagged_words[pos-2][0] in BHK or  tagged_words[pos-2][0] in budget or tagged_words[pos-2][0] in pos_type:
                    continue
                 if tagged_words[pos-2][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos-2][0] == '>':
                                         adj.append('more')
                 if tagged_words[pos-2][1] == 'CD':
                             leafs.append(tagged_words[pos-2][0])
                         
                 if (tagged_words[pos-2][1]=="RB") or (tagged_words[pos-2][1]=="RBR") or (tagged_words[pos-2][1]=="RBS") or (tagged_words[pos-2][1]=="IN") or (tagged_words[pos-2][1]=="JJR"):
                         adj.append(tagged_words[pos-2][0])
                         
             if not pos-3<0:
                 if tagged_words[pos-3][0] in BHK or tagged_words[pos-3][0] in budget or tagged_words[pos-3][0] in pos_type:
                    continue

                 if tagged_words[pos-3][0] == '<':
                                         adj.append('less')
                 if tagged_words[pos-3][0] == '>':
                                         adj.append('more')
                 if tagged_words[pos-3][1] == 'CD':
                             leafs.append(tagged_words[pos-3][0])
                         
                 if (tagged_words[pos-3][1]=="RB") or (tagged_words[pos-3][1]=="RBR") or (tagged_words[pos-3][1]=="RBS") or (tagged_words[pos-3][1]=="IN" or (tagged_words[pos-3][1]=="JJR")):
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
    #query = "I need a greater than 2 BHK in Andheri less than 5 Cr and more than 2 Cr"
    #query="A small 2 or 3 BHK within 1 Cr and less than 1 year"

    #query="Any flat available within a year"
    #query="a 4BHK property between andheri and goregaon less than 200000"
    #query="a small bhk under 5CR"
    #query="a 4 BHK property with  BUDGET BETWEEN 2 and 3 Cr"
    #query="a one BHK under 2Cr "
    #query="I need a 4-bedroom flat"
    #query=" a 476-bhk property"
    #query="<2 bhk Apartment in the range of 1-2 cr having a swimming pool,lift,tennis,security nearby Bandra after 30 months"
    #query="need a 3 bhk house inbetween 50 and 70 lakhs with club house"
    #query ="need a 1.3 BHK of 2+ CR"
    #query="1BHK,2.56Cr"
    #query=" home with 2 rooms"
    #query="2 BHk,2000000"
    #query="need a 1 BHK in 1 Cr to 10 Cr"
    # query="I need a 2 BHk near Andheri"
    #query="2 BHk flat in Mumbai Central <20000000"
    #query="2bhk in mumbai below 30 lacs with park"
    #query="cheap 2 bhk in Khargar"
    # query = raw_input()
    #query = sys.argv[1]
    #removing Punctuations
    #query = re.sub(r'[^\w\s]',' ',query)
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



    [bhk,bhk_desc,bhk_item]=BHK(words)      
    [budget,budget_adj,budget_item]=Budget(words)
    [possession,possession_desc,date]=Possession(words)
    [area,area_type,dim]=Area(words)

    st=PorterStemmer()
    stemmed_words=[words for words in query.split()] 
    apt_type=AptType(stemmed_words)

    amenities=Amenities(stemmed_words)

    query = str(query.upper())
    [location,adv_location]=Location(query)

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

from urllib import urlopen
url = "http://hdfcred.com/apimaster/mobile_v3/nlp_listing_v1?LocKeyword=in&inLocation=Powai&inLat=19.1198169815697770000&inLong=72.9033694027192200000&cityid=1&propType=APARTMENT&maxBHK=3&limit=0,20"
url = urlopen(url).read()
print url

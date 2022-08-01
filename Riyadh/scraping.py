import requests,csv
import pandas as pd

url="https://sa.aqar.fm/graphql"
#url api

def get_d(cat,direction)--> list: #fun get all distrcts
  districts=[]
  payload={
  "operationName": "getAllDistricts",
  "variables": {
   "category": cat,
   "city_id": 21,
   "direction_id": direction
   },
  "query": "query getAllDistricts($category: Int!, $city_id: Int!, $direction_id: Int) {\n  Web {\n    districts(category: $category, city_id: $city_id, direction_id: $direction_id) {\n      name\n      title\n      uri\n      path\n      district_id\n      category {\n        name\n        uri\n        id\n        __typename\n      }\n      city {\n        uri\n        city_id\n        __typename\n      }\n      direction {\n        uri\n        direction_id\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n"
  }
  res=requests.get(url,json=payload).json()
  all=res["data"]["Web"]["districts"]
  for i in range(len(all)):
  	districts.append(all[i]["district_id"])
  	
  return districts

def search_data(cat,direction,dist):# fun search by direction and districts
	
	pay={
	"operationName": "findListings",
	"variables": {
	"size": 20,
        "from": 0,
        "sort": {
        "create_time": "desc",
        "has_img": "desc"
        },
        "where": {
        "category": {
	"eq": cat
	},
        "city_id": {
	"eq": 21
	},
      	"direction_id": {
	"eq": direction
	},
	"district_id": {
        "eq": dist
        }}
        },
	"query": "query findListings($size: Int, $from: Int, $sort: SortInput, $where: WhereInput, $polygon: [LocationInput!]) {\n  Web {\n    find(size: $size, from: $from, sort: $sort, where: $where, polygon: $polygon) {\n      ...WebResults\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WebResults on WebResults {\n  listings {\n    user_id\n    id\n    uri\n    title\n    price\n    content\n    imgs\n    refresh\n    category\n    beds\n    livings\n    wc\n    area\n    type\n    street_width\n    age\n    last_update\n    street_direction\n    ketchen\n    ac\n    furnished\n    location {\n      lat\n      lng\n      __typename\n    }\n    path\n    user {\n      review\n      img\n      name\n      phone\n      iam_verified\n      rega_id\n      __typename\n    }\n    native {\n      logo\n      title\n      image\n      description\n      external_url\n      __typename\n    }\n    rent_period\n    city\n    district\n    width\n    length\n    advertiser_type\n    create_time\n    __typename\n  }\n  total\n  __typename\n}\n"
	}
	data=requests.get(url,json=pay)
	all=data.json()["data"]["Web"]["find"]["listings"]
	#lists columns
	prices,area,beds,wc,live,street,age,last,direction,ketchen,location0,location1=[],[],[],[],[],[],[],[],[],[],[],[]
	for i in range(len(all)):
		prices.append(all[i]["price"])
		area.append(all[i]["area"])
		beds.append(all[i]["beds"])
		wc.append(all[i]["wc"])
		live.append(all[i]["livings"])
		street.append(all[i]["street_width"])
		age.append(all[i]["age"])
		last.append(all[i]["last_update"])
		direction.append(all[i]["street_direction"])
		ketchen.append(all[i]["ketchen"])
		location0.append(all[i]["location"]["lat"])
		location1.append(all[i]["location"]["lng"])
		
	
	#save file csv
	with open('agar.csv', 'a+', encoding='UTF8', newline='') as f:
		writer = csv.writer(f)
		for p,a,b,w,lll,s,ag,la,d,k,loc0,loc1 in zip(prices,area,beds,wc,live,street,age,last,direction,ketchen,location0,location1):
			# add data in file
			writer.writerow([p,a,b,w,lll,s,ag,la,d,k,loc0,loc1])
		
def main():
	categorys={
  "شقق0":1,
  "شقق1":6,
  "ارض0":15,
  "ارض1":2,
  "فلل1":3,
  "فلل0":5,
  "دور0":4,
  "دور1":22,
  "عم0":16,
  "عم1":7,
  "محل0":8,
  "محل1":20,
  "بيت0":11,
  "بيت1":9,
  "استراحة0":13,
  "استراحة1":10,
  "مكتب":14,
  "مزرعة":12,
  "مستودع":17,
  "مخيم":18,
  "شاليه":23,
  "غرف":19,
  "شقه":21
  }
	print(20*"=+")
	for i,x in enumerate(categorys.keys()):
		print(f"{i}-{x}")
	print(20*"=+")
	
	x=input("Enter Category String =")
	cat=categorys.get(x,"Error")
	print(cat)
	print("waiting...for scraping")
	header=["price","area","bedroom","wc","live_room","street_width","house_age","last_update","direction","ketchen","latitude","longitude"]
	with open('agar.csv', 'w', encoding='UTF8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(header)
	dirctions=[4,3,6,7,1]
	for dirction in dirctions:
		for d in get_d(cat,dirction):
			search_data(cat,dirction,d)
		
if __name__ == "__main__":
	main()


import requests,csv

class Aqar_API:
	def __init__(self):
		self.url_api="https://sa.aqar.fm/graphql"
		
	def length(self):
		payload={
		"operationName": "getAllDirections",
		"variables": {"category": 1,"city_id": 21},
		"query": "query getAllDirections($category: Int!, $city_id: Int!) {\n  Web {\n    directions(category: $category, city_id: $city_id) {\n      name\n      title\n      uri\n      path\n      direction_id\n      category {\n        name\n        uri\n        id\n        __typename\n      }\n      city {\n        uri\n        city_id\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n"}
		
		req=requests.post(self.url_api,json=payload)
		data=req.json()["data"]["Web"]["directions"]
		name=[data[i]["name"] for i in range(len(data))]
		count=[data[i]["count"] for i in range(len(data))]
		
		all_count=[]
		for c in count:
			all_count.append(c)
		
		return all_count
		
	def search_data(self,count,category,dirction):
		prices,district,area,beds,wc,live,street,age,last,direction,ketchen,location0,location1=[],[],[],[],[],[],[],[],[],[],[],[],[]
		
		for u in range(count):
			payload={
			"operationName": "findListings",
			"variables": {"size": 200,"from":u,
			"sort": {"create_time": "desc",
			"has_img":"desc"},
			"where": {"category": {"eq": category},
			"city_id": {"eq": 21},
			"direction_id": {"eq": dirction}}},
			"query": "query findListings($size: Int, $from: Int, $sort: SortInput, $where: WhereInput, $polygon: [LocationInput!]) {\n  Web {\n    find(size: $size, from: $from, sort: $sort, where: $where, polygon: $polygon) {\n      ...WebResults\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WebResults on WebResults {\n  listings {\n    user_id\n    id\n    uri\n    title\n    price\n    content\n    imgs\n    refresh\n    category\n    beds\n    livings\n    wc\n    area\n    type\n    street_width\n    age\n    last_update\n    street_direction\n    ketchen\n    ac\n    furnished\n    location {\n      lat\n      lng\n      __typename\n    }\n    path\n    user {\n      review\n      img\n      name\n      phone\n      iam_verified\n      rega_id\n      __typename\n    }\n    native {\n      logo\n      title\n      image\n      description\n      external_url\n      __typename\n    }\n    rent_period\n    city\n    district\n    width\n    length\n    advertiser_type\n    create_time\n    __typename\n  }\n  total\n  __typename\n}\n"
			}
			req=requests.post(self.url_api,json=payload)
			all=req.json()["data"]["Web"]["find"]["listings"]
			#print(len(all))
			
			for i in range(len(all)):
				prices.append(all[i]["price"])
				district.append(all[i]["district"])
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
				
			with open('agar.csv', 'a+', encoding='UTF8', newline='') as f:
				writer = csv.writer(f)
				for p,dis,a,b,w,lll,s,ag,la,d,k,loc0,loc1 in zip(prices,district,area,beds,wc,live,street,age,last,direction,ketchen,location0,location1):
					# add data in file
					writer.writerow([p,dis,a,b,w,lll,s,ag,la,d,k,loc0,loc1])



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
	cats=[i for i in categorys.values()]
	dirctions=[4,3,6,7,1]
	print("waiting...for scraping")
	header=["price","district","area","bedroom","wc","live_room","street_width","house_age","last_update","direction","ketchen","latitude","longitude"]
	with open('agar.csv', 'w', encoding='UTF8', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(header)
	
	cat=1
	dirction=1
	bot=Aqar_API()
	k=bot.length()
	
	print(f"num pages dirctions ={k}")
	bot.search_data(k[-1],cat,dirction)
	print("="*10,"done file csv","="*10)
	
	
if __name__ =="__main__":
		main()
		
 

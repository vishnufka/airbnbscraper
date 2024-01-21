import requests
import json
import sys
from bs4 import BeautifulSoup

#gets the urls from a file line by line
#only tested this on Mac OSX so if sys.path has
#problems then declare the urls in the urls array
urls = []
with open(sys.path[0] + "/urls.txt") as file:
	urls = file.readlines()
	urls = [x.strip() for x in urls] 
file.close()

#loops through all urls and scrapes the pages
for url in urls:
	print("\n====================================================================")

	page = requests.get(url)

	soup = BeautifulSoup(page.text, 'html.parser')

	#this lets us find the element that contains the listing json
	identifyJson = "reduxData"
	
	#find the element, load it in as json so we can read it
	for list_item in soup.find_all('script'):
		if (list_item.getText().find(identifyJson) > -1):
			data = list_item.getText()
	data = data.replace("<!--", "").replace("-->", "")
	jdata = json.loads(data)

	#gets the json of the listing
	listing = jdata["bootstrapData"]["reduxData"]["marketplacePdp"]["listingInfo"]["listing"]

	#property url to help identify
	print("\nPROPERTY URL: " + url)

	#property name
	print("\nPROPERTY NAME: " + listing["name"])

	#property type
	print("\nPROPERTY TYPE: " + listing["room_and_property_type"])

	#number of beds/baths
	print("\nPROPERTY HAS: " + listing["bed_label"] + 
		" in " + listing["bedroom_label"] +
		" and " + listing["bathroom_label"] + 
		" with space for " + listing["guest_label"])

	#room details if present, do not show if empty
	if (len(listing["listing_rooms"]) > 0 ):

		print("\nROOMS ARRANGED AS FOLLOWS:")
		count = 1;
		for room in listing["listing_rooms"]:
			print("Room " + str(count) + " has:")
			for bed_entry in room.get("beds"):
				print (str(bed_entry["quantity"]) + "x " + bed_entry["type"].replace("_", " "))
			count += 1

	#amenities
	amenities = listing["listing_amenities"]
	true_amenities = []
	false_amenities = []

	for entry in amenities:
		if (entry["is_present"]):
			true_amenities.append(entry["name"])
		else:
			false_amenities.append(entry["name"])

	print ("\nTHE FOLLOWING AMENITIES ARE PRESENT: ")
	for amen in true_amenities:
		amen = amen.replace("&amp;", "&")
		print(amen)

	#can show absent amenities if necessary
	#print ("\nTHE FOLLOWING AMENITIES ARE ABSENT: ")
	#for amen in false_amenities:
	#	amen = amen.replace("&amp;", "&")
	#	print(amen)

print("\n====================================================================")


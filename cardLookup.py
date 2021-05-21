import os
import re
import requests
from bs4 import BeautifulSoup
import concurrent.futures

def GetCardPrice(card):
	cardname = card[1]
	url = 'https://www.cardmarket.com/en/Magic/Cards/' + cardname
	info = None
	attempts = 0
	while info==None and attempts < 10:
		response = requests.get(url)
		contents = response.text
		soup = BeautifulSoup(contents, 'html.parser')
		info = soup.find("div", "infoContainer")
		attempts += 1
	if info==None:
		print('Couldn\'t find',cardname)
		return 0
	elems = info.find_all("dd")
	price_format = re.compile('(\\d+),(\\d+) €')
	price_raw = elems[3].string
	match = re.match(price_format, price_raw)
	price = float(match[1]+'.'+match[2])
	return price

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def IterativePriceFinder(filename):
	path = os.path.join(__location__, 'buylist.txt')
	f = open(path, 'r')
	card_string = f.read()
	close(f)
	total_price = 0
	card_format = re.compile('^(\d*)x? ?(.*)', re.MULTILINE)
	cards = re.findall(card_format, card_string)
	for card in cards:
		quantitystring = card[0]
		quantity = 1 if (quantitystring == '') else int(quantitystring)
		cardname = card[1]
		price = GetCardPrice(cardname)
		print(cardname+":",price,"€")
		total_price += quantity * price
		
	print("Total price: ",total_price,"€")
	return total_price

def ConcurrentPriceFinder(filename):
	path = os.path.join(__location__, 'buylist.txt')
	f = open(path, 'r')
	card_string = f.read()
	total_price = 0
	card_format = re.compile('^(\d*)x? ?(.*)', re.MULTILINE)
	cards = re.findall(card_format, card_string)
	with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
		future_to_card = {executor.submit(GetCardPrice, card): card for card in cards}
		for future in concurrent.futures.as_completed(future_to_card):
			card = future_to_card[future]
			quantity = 1 if (card[0] == '') else int(card[0])
			cardname = card[1]
			price = future.result()
			print(cardname+":",price,"€")
			total_price += quantity * price
	return(total_price)

total_price = ConcurrentPriceFinder('buylist.txt')
print("Total price: ",total_price,"€")
import requests
import re
from bs4 import BeautifulSoup

def trim(s):
    """Trims given str, s, down to alphanumeric characters"""
    trimmed=""
    for st in s:
        if st.isalnum():
            trimmed+=st
    return trimmed

def parsePrice(p):
    """Parses str p, which is formatted as $(price)/n, into a float"""
    price=float(p[2:-1])
    return price

#input your keyword as a str that is all lowercase with no spaces
keyword="arcteryx"
#input your maximum price
max_price=400
#input your sizes as an array of lowercase, one letter strs
sizes=["s","m","l"]
pagen=1


while pagen<30:
    URL="https://www.geartrade.com/clothing/mens-clothing/mens-jackets?sort=new&page="+str(pagen)
    page=requests.get(URL)

    soup=BeautifulSoup(page.content,"html.parser")
    results=soup.find(id="results")
    links = [i['href'] for i in results.find_all("a", href=True)]
    names=results.find_all("a",class_="product-card")
    c=0
    for piece in names:
        item_name=piece.find("div",class_="product-card__name").text
        item_price=str(piece.find("div",class_="product-card__price").text)
        item_size=piece.find("div",class_="product-card__brand").text
        item_link=links[c]
        if(keyword in trim(item_name.strip().lower()) and parsePrice(item_price)<=max_price and str(item_size[1]).lower() in sizes):
            print(item_name.strip())
            print(item_price.strip())
            print(item_size.strip())
            print(item_link)
        c+=1
    pagen+=1



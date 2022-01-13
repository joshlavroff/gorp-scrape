import requests
import sys
from PyQt5.QtWidgets import QLineEdit,QComboBox,QGridLayout,QLabel,QApplication,QWidget, QPushButton, QTextEdit
from PyQt5 import QtGui
from bs4 import BeautifulSoup


def trim(s):
    """Trims given str down to alphanumeric characters"""
    trimmed=""
    for st in s:
        if st.isalnum():
            trimmed+=st.lower()
    return trimmed

def parsePrice(p):
    """Parses str p, which is formatted as $(price)/n, into a float"""
    price=float(p[2:-1])
    return price



def search():
    keyword = trim(key.text())
    max_price = float(pri.text())
    sizes = ["s", "m", "l"]
    category = cat.currentText().lower()
    pagen=1
    while pagen<30:
        URL="https://www.geartrade.com/clothing/mens-clothing/mens-"+category+"?sort=new&page="+str(pagen)
        page=requests.get(URL)

        soup=BeautifulSoup(page.content,"html.parser")
        results=soup.find(id="results")
        links = [i['href'] for i in results.find_all("a", href=True)]
        names=results.find_all("a",class_="product-card")
        c=0
        for piece in names:
            item_name=piece.find("div",class_="product-card__name").text
            if keyword in trim(item_name.strip().lower()):
                item_price=str(piece.find("div",class_="product-card__price").text)
                if parsePrice(item_price)<=max_price:
                    item_size=piece.find("div",class_="product-card__brand").text
                    if str(item_size[1]).lower() in sizes:
                        item_link=links[c]
                        print(item_name.strip())
                        print(item_price.strip())
                        print(item_size.strip())
                        print(item_link)

            c+=1
        pagen+=1




app=QApplication(sys.argv)
window=QWidget()
window.setWindowTitle('GorpScrape')
window.setWindowIcon(QtGui.QIcon("gs.png"))
window.setGeometry(100,100,280,80)
window.move(60,15)
layout=QGridLayout()
cat=QComboBox()
key=QLineEdit()
siz=QLineEdit()
pri=QLineEdit()
res=QTextEdit()
sear=QPushButton("Search")
sear.clicked.connect(search)
cat.addItems(["Jackets","Pants","Shirts","Hats"])
layout.addWidget(QLabel("Category"),0,0)
layout.addWidget(QLabel("Keyword"),1,0)
layout.addWidget(QLabel("Sizes"),2,0)
layout.addWidget(QLabel("Max Price"),3,0)
layout.addWidget(cat,0,1)
layout.addWidget(key,1,1)
layout.addWidget(siz,2,1)
layout.addWidget(pri,3,1)
layout.addWidget(sear,4,0,1,2)
layout.addWidget(res,0,3,5,2)
window.setLayout(layout)
window.show()
sys.exit(app.exec_())

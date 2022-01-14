import requests
import sys
import priceEstimate
import pandas as pd
import trim
from PyQt5.QtWidgets import QLineEdit,QComboBox,QGridLayout,QLabel,QApplication,QWidget, QPushButton, QProgressBar, \
    QTextBrowser
from PyQt5 import QtGui
from bs4 import BeautifulSoup


def search():
    keyword = trim.trimStr(key.text())
    max_price = float(pri.text())
    sizes =siz.text().lower().split(",")
    for i in range(len(sizes)):
        sizes[i]=sizes[i][0]
    category = cat.currentText().lower()
    pagen=1
    na=[]
    si=[]
    pr= []
    lp=[]
    while pagen<10:
        URL="https://www.geartrade.com/clothing/mens-clothing/mens-"+category+"?searchTerm="+keyword.replace(" ","+")+"&sort=new&page="+str(pagen)
        page=requests.get(URL)

        soup=BeautifulSoup(page.content,"html.parser")
        results=soup.find(id="results")
        links = [i['href'] for i in results.find_all("a", href=True)]
        names=results.find_all("a",class_="product-card")
        c=0
        for piece in names:
            item_name=piece.find("div",class_="product-card__name").text
            item_price=str(piece.find("div",class_="product-card__price").text)
            if trim.parsePrice(item_price)<=max_price:
                item_size=piece.find("div",class_="product-card__brand").text
                if str(item_size[1]).lower() in sizes:
                    item_link=links[c]
                    na.append(item_name.strip())
                    si.append(item_size.strip())
                    pr.append(item_price.strip())
                    lp.append(priceEstimate.getAvgPrice(item_name))
                    res.append("<a href="+item_link+">"+item_name.strip()+"</a>")
                    res.append(item_price.strip())
                    res.append(item_size.strip())
                    res.append("")
                    res.append("---------------")
                    res.append("")

            c+=1
        pagen+=1
        pro.setValue(pagen)
    data = {"Name": na, "Size": si, "Price": pr, "Average List Price": lp}
    print(data)
    d=pd.DataFrame(data)
    print(d)
    d.to_csv(r"C:\Users\JoshL\Desktop\results1.csv")




app=QApplication(sys.argv)
window=QWidget()
window.setWindowTitle('GorpScrape')
window.setWindowIcon(QtGui.QIcon("gs.png"))
window.setGeometry(100,100,660,660)
window.move(60,15)
layout=QGridLayout()
cat=QComboBox()
key=QLineEdit()
key.setPlaceholderText("Enter the product or keyword you would like to search")
siz=QLineEdit()
siz.setPlaceholderText("Enter sizes separated by commas")
pri=QLineEdit()
res=QTextBrowser()
res.setOpenExternalLinks(True)
pro=QProgressBar()
pro.setMaximum(10)
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
layout.addWidget(pro,5,0,1,5)
window.setLayout(layout)
window.show()
sys.exit(app.exec_())


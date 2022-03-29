import requests
from bs4 import BeautifulSoup
import sqlite3

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru'
}

db = sqlite3.connect('result.db')
cur = db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS info (

    name TEXT,
    address TEXT,
    phone TEXT,
    site TEXT,
    email TEXT,
    rubrika TEXT
)''')
db.commit()
cur.close()
db.close()
countw = 0
def get_data(url):
    response = requests.get(url = url,headers=headers)
    response.encoding = 'cp1251'

    with open(file='index.html',mode='w+') as file:
        file.write(response.text)
    with open(file='index.html',mode='r') as file:
        src = file.read()

    soup = BeautifulSoup(src,'lxml')
    try:
        name = soup.find(class_= "head")
        name = name.text
        
        address = soup.find_all("tr", class_="mes")
        address = (address[0].text).replace("Почтовый адрес",'')
        

        phone = soup.find_all("tr", class_="mes")
        phone = (phone[1].text).replace("Телефон/Факс",'')
        

        site = soup.find_all("tr", class_="mes")
        site = (site[2].text).replace("Сайт",'')
        

        email = soup.find_all("tr", class_="mes")
        email = (email[3].text).replace("E-mail",'')
        

        rubrika = soup.find_all("tr", class_="mes")
        rubrika = (rubrika[4].text).replace("Рубрика",'')
        
        try:
            db = sqlite3.connect('result.db')
            cur = db.cursor()
            if email != "Нет":
                cur.execute(f"INSERT INTO info(name,address,phone,site,email,rubrika) VALUES('{name}','{address}','{phone}','{site}','{email}','{rubrika}')")
                db.commit()
        except:
            print("err")
            print(type(name.text))
            
            
        global countw
        countw+=1
    except: 
        print("ERROR!", url)


def main():
    number = 14000
    for i in range(1999): #494/999
        get_data(url=f'http://org16.ru/{number}/') #15655 last
        number+=1 #15723 last
    print(countw)
 

if __name__ == "__main__":
    main()
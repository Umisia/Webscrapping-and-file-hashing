import os, sys, time, mechanize, http.cookiejar, html2text, hashlib, getpass
from bs4 import BeautifulSoup

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = http.cookiejar.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

# The site we will navigate into, handling it's session
print("Connecting: https://xxxx/login/ ... \n")
time.sleep(1)
br.open('https://xxxx/login/')

# View available forms
#for f in br.forms():
  #  print(f)

# Select the second (index one) form (the first form is a search query box)
br.select_form(nr=0)

try:
    # User credentials
    
    email = input("Enter email address: ")
    br.form['email'] = email
    
    password = getpass.getpass("Enter password (wont be displayed): ")
    #password = input("\nEnter password: ")
    br.form['password'] = password 
    
    # Login
    br.submit()
    print("\nLogged in \n")
except:
    print("\nUnauthorized access. Closing...")
    time.sleep(2)
    sys.exit(0)

time.sleep(1)
print("Scrapping http://xxxx/manage/activity.cfm?id=590114 ...")
time.sleep(0.5)
content = br.open('http://xxxx/manage/activity.cfm?id=590114').read()

print("Listing files from website..")
time.sleep(0.5)

soup = BeautifulSoup(content, "html.parser")
zupa = soup.find_all("td", {"class":"notranslate"})
linki = zupa[0].find_all('a', href=True)


teksty_linki={}

for li in linki:
    tekst = li.get_text()
    linczek=  li.get('href')
    teksty_linki[tekst]=linczek


def haszowanie(nazwa_pliku):
    #BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(nazwa_pliku, 'rb') as afile:
        buf = afile.read()
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read()
            hasz = hasher.hexdigest()
            return hasz

print("Creating list.txt...")
time.sleep(0.5)
print("Listing files from folders and subfolders...")
time.sleep(0.5)
print("Hashing files...")
time.sleep(0.5)
print("Comparing lists...")


print("Writing to list.txt...")
time.sleep(0.5)

with open("list.txt", "w", encoding="utf-8") as filewrite:
    for root, dirs, files in os.walk("."):
        for name in files:
            nazwa_pliku = os.path.join(root, name)
            podzielona_nazwa = nazwa_pliku.rsplit('\\', 1)[1]
            if "." in podzielona_nazwa:
                pass
            else:
                hasz = haszowanie(nazwa_pliku)
                if podzielona_nazwa in teksty_linki:
                    tekst_i_link = teksty_linki[podzielona_nazwa]
                    dozapisu = podzielona_nazwa + ","+ tekst_i_link +"," + str(hasz).upper()+";"+"\n"
                    filewrite.write(dozapisu)
                else:
                    pass
                    dozapisu = podzielona_nazwa + ","  + str(hasz).upper() +";"+"\n"
                    filewrite.write(dozapisu)

print("\nDone")
os.system('pause')

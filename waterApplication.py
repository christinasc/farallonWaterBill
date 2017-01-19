import mechanicalsoup 
import re
from sys import argv

loginInfo = { 'LOGIN':"login", 
              'PASSWORD':"password",
              'USER_NAME': "username"}

configFile = "login.config.me"
URL = "https://www.midpeninsulawater.org/billpay/"

def readConfigFile():
    with open(configFile) as fp:
        for line in fp:
            entry = line.split(":")
            key = entry[0].strip()
            val = entry[1].strip()
            loginInfo[key] = val            
    print("this is logininfo", loginInfo)
    

def getLoginInfo(browser):
    # req. login name
    login_page = browser.get(URL)
    login_form = login_page.soup.find("form", {"class":"ywploginform"})

    login_form.find("input", {"name": "login[username]"})["value"]= loginInfo['LOGIN']
    login_form.find("input", {"name": "login[password]"})["value"] = loginInfo['PASSWORD']
    response = browser.submit(login_form, login_page.url)
    return response

def main():
    readConfigFile()

    # create a browser object
    browser = mechanicalsoup.Browser()
    response = getLoginInfo(browser)
    if response:
        print("Your're connected as " + loginInfo['USER_NAME'])
        print response
    else:
        print("Not connected")

'''
        acctInfo = response.soup
        if acctInfo:
            print " response found"        
            #print (acctInfo.get_text())
            acctText = acctInfo.get_text()
            print acctText
            print " ================================"
'''


'''
            print " ================================"

        for link in response.soup.find_all('a'):
            availUrls = str(link.get('href'))
           # print ":", availUrls, ":"
            if re.search(r"history", availUrls):
                print "link found for history, following...."
                print(link.get('href'))
                history_page = browser.get(availUrls)
                if history_page:
                        print "got history page"
                        print history_page.soup.get_text()
'''

#    print(response.soup.title.text)
#    user = response.soup.find("span", {"class":"u-linkComplex-target"}).string
#    user = response.soup.find("")
#    if USERNAME_NAME in user:

if __name__ == "__main__":
    main()

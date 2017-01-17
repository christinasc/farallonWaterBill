import mechanicalsoup 
import re

if __name__ == "__main__":

    URL = "https://www.midpeninsulawater.org/billpay/"
    LOGIN = ""
    PASSWORD = ""
    USER_NAME = ""

    # create a browser object
    browser = mechanicalsoup.Browser()

    # req. Twitter login name
    login_page = browser.get(URL)

    login_form = login_page.soup.find("form", {"class":"ywploginform"})
#    print login_form

    login_form.find("input", {"name": "login[username]"})["value"]=LOGIN
    login_form.find("input", {"name": "login[password]"})["value"] = PASSWORD

    response = browser.submit(login_form, login_page.url)

#    user = response.soup.find("span", {"class":"u-linkComplex-target"}).string
#    user = response.soup.find("")

#    if USERNAME_NAME in user:
    if response:
        print("Your're connected as " + USER_NAME)
        print response
        acctInfo = response.soup
        if acctInfo:
            print " response found"
#        
            #print (acctInfo.get_text())
            acctText = acctInfo.get_text()
            print acctText
            print " ================================"
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

#        print(response.soup.title.text)
    else:
        print("Not connected")

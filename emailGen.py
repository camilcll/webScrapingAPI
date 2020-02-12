import nav_fonctions
import names
import random
from password_generator import PasswordGenerator



nav = nav_fonctions.nav()
f = open("account.txt", "a+")
nav.get("https://outlook.live.com/owa/")
nav.click('//*[@class="action-wrapper"]',path2='//*[@class="action-wrapper"]', mode=4)
fname = names.get_first_name(gender='male').lower()
lname = names.get_last_name().lower()
email = fname + "." + lname + str(random.randint(10,50))
nav.fill('//*[@id="MemberName"]', email)
nav.click('//*[@id="iSignupAction"]',path2='//*[@id="iSignupAction"]',mode=4)
pwo = PasswordGenerator()
pwo.minlen = 10
pwo.minschars = 1
pwo.minnumbers = 2
pwo.minuchars = 1
psw = pwo.generate()
nav.fill('//*[@id="PasswordInput"]', psw)
nav.click('//*[@id="iOptinEmail"]')
nav.click('//*[@id="iSignupAction"]', path2='//*[@id="iSignupAction"]', mode=4)
nav.fill('//*[@id="FirstName"]',fname)
nav.fill('//*[@id="LastName"]',lname)
nav.click('//*[@id="iSignupAction"]', path2='//*[@id="iSignupAction"]', mode=4)
nav.click('//*[@id="BirthMonth"]')
nav.click('//*[@id="BirthMonth"]/option['+str(random.randint(2,13))+']')
nav.click('//*[@id="BirthDay"]')
nav.click('//*[@id="BirthDay"]/option['+ str(random.randint(2,20))+']')
nav.click('//*[@id="BirthYear"]')
nav.click('//*[@id="BirthYear"]/option['+ str(random.randint(21,35))+']')
nav.click('//*[@id="iSignupAction"]', path2='//*[@id="iSignupAction"]',mode=4)
f.write("\nEMAIL : " + email + "@outlook.com\nPWD : " + psw + "\n------------------")
f.close()

# new //*[contains(@title,"new")]
# audio //*[contains(@title,"audio")]
#audioplay //*[contains(@title,"audio")]
#next //*[@id="iSignupAction"]

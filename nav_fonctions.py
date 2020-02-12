from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium import webdriver
import os
cassis_path = "CASSIS".join(os.path.dirname(os.path.abspath(__file__)).split("CASSIS")[:-1]) + "CASSIS"

import time
import autoit
import pywinauto

from threading import Lock

import updateChromeDriver as i

lock = Lock()
userdirs = os.listdir("users")
nbusers = len(userdirs)

class nav:
    def __init__(self, headless = False, tOUT=5):
        """
        entrée : headless un booléen
        postcond : ouvre une fenêtre visible si headless est faux et invisible si headless est vrai
        """

        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time>tOUT*60:
                raise Exception

            lock.acquire()
            global userdirs
            global nbusers
            if len(userdirs)==nbusers:
                i.install()
            if len(userdirs)>0:
                self._user = userdirs[-1]
                userdirs = userdirs[:-1]
            else:
                lock.release()
                continue
            lock.release()
            try:
                self._headless_options = Options()
                self._headless_options.add_argument("--headless")
                self._headless_options.add_argument("--window-size=1280x720")
                self._headless_options.add_argument("--disable-gpu")
                #self._headless_options.add_argument("--remote-debugging-port=9999")
                self._headless_options.add_argument("log-level=2")
                #self._headless_options.add_argument("--test-type")
                self._headless_options.add_argument('--user-data-dir=' + cassis_path + '\\users\\' + self._user)
                self._headless_options.add_experimental_option('w3c', False)

                self._options = Options()
                self._options.add_argument("--start-maximized")
                self._options.add_argument('--user-data-dir=' + cassis_path + '\\users\\' + self._user)
                #self._options.add_argument('--profile-directory=ANTICAPTCHA')
                self._options.add_experimental_option('excludeSwitches', ['enable-automation'])
                self._options.add_experimental_option('w3c', False)
                #PROXY = "37.187.116.199:80"
                #self._options.add_argument('--proxy-server=%s' % PROXY)

                self._driver = None

                if headless:
                    self._driver = webdriver.Chrome(executable_path = "chromedriver.exe", chrome_options=self._headless_options)
                else:
                    self._driver = webdriver.Chrome(executable_path = cassis_path + "\\chromedriver\\chromedriver.exe", chrome_options=self._options)
                break
                #https://intoli.com/blog/not-possible-to-block-chrome-headless/
                #https://antoinevastel.com/bot%20detection/2018/01/17/detect-chrome-headless-v2.html

                #print(self._headless_options.arguments)
            except:
                pass

    def currenturl(self):
        """
        postcond : retourne l'url de la page actuelle
        """
        try:
            return self._driver.current_url
        except:
            return ""

    def setproxy(self, PROXY):
        """
        non fonctionnel pour le moment!
        """
        try:
            self._headless_options.add_argument('--proxy-server=%s' % PROXY)
            return True
        except Exception as ex:
            #print(ex)
            return False

    def back(self):
        """
        postcond : va à la page précédente et retourne vrai si ça a réussi, faux sinon
        """
        try:
            self._driver.back()
            return True
        except Exception as ex:
            #print(ex)
            return False

    def compt(self, path):
        """
        entrée : path un str
        sortie : entier positif ou nul
        postcond : retourne le nombre d'éléments de chemin path
        """
        try:
            return len(self._driver.find_elements_by_xpath(path))
        except Exception as ex:
            return 0
            #print(ex)

    def source(self):
        """
        retourne le code source de la page
        """
        try:
            return self._driver.page_source
        except Exception as ex:
            return ""
            #print(ex)

    def get(self, url):
        """
        entrée : url un str
        postcond : la page va à l'url url et retourne vrai si la page est bien chargée et faux si non
        """
        try:
            self._driver.get(url)
            return True
        except Exception as ex:
            if 'NoneType' in str(ex):
                #print("Pas ouvert!")
                return False
            #print(ex)
            return False

    def click(self, path, tOUT=5, freq=1, mode=1, path2="", attrib="", val="", js=""):
        """
        entrées : path, attrib, val, js et path2 des str, tOUT, mode et freq des entiers
        precond : tOUT, mode et freq positifs
        postcond : essaye de cliquer sur un element tous les freq secondes pendant au maximum tOUT secondes jusqu'à ce que le clique soit bon :
                mode 1 : le clique est bon si l'élément est trouvée et cliqué
                mode 2 : le clique est bon quand l'élément de chemin path2 existe
                mode 3 : le clique est bon quand l'élément de chemin path2 est visible
                mode 4 : le clique est bon quand l'élément de chemin path2 n'existe pas
                mode 5 : le clique est bon quand l'élément de chemin path2 est invisible
                mode 6 : le clique est bon quand l'élément de chemin path2 a val comme valeur pour l'attribut attrib
                mode 7 : le clique est bon quand le javascript js executé retourne val (ne pas oublier de mettre "return")
            retourne vrai si le clique est bon, faux si le temps de clique a depassé tOUT secondes
        """
        try:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time

                try:
                    if mode==1:
                        self._driver.find_element_by_xpath(path).click()
                    elif mode==2:
                        self._driver.find_element_by_xpath(path2)
                    elif mode==3:
                        try:
                            if not self._driver.find_element_by_xpath(path2).is_displayed():
                                raise Exception()
                        except Exception as e:
                            #print(e)
                            raise Exception("element not visible")
                    elif mode==4:
                        try :
                            self._driver.find_element_by_xpath(path2)
                        except:
                            return True
                        raise Exception("element exists")
                    elif mode==5:
                        if self._driver.find_element_by_xpath(path2).is_displayed():
                            raise Exception("element not visible")
                    elif mode==6:
                        if not getattrib(path2, attrib)==val:
                            raise Exception("element attrib doesn't matche")
                    elif mode==7:
                        if not self._driver.execute_script(js)==val:
                            raise Exception("js not good")
                    else:
                        return False
                    return True
                except:
                    try:
                        self._driver.find_element_by_xpath(path).click()
                    except:
                        pass
                    time.sleep(freq)

                if (elapsed_time>tOUT):
                    return False

        except Exception as ex:
            #print(ex)
            return False

    def fill(self, path, keys, tOUT=5, backspace=0, delScript=None):
        """
        entrées : path, delScript et keys des str, tOUT et backspace des entiers positifs
        sortie : booléen
        postcond : essaye jusqu'à ce que tOUT secondes se soient écoulées et retourne vrai si l'élément de chemin path a pu être rempli avec keys et faux sinon.
        La fonction va effacer le champ de l'élément en envoyant backspace fois la touche "effacer" si backspace>0 ou va effacer diréctement le cas échéant (mais il faut que l'élément soit un input.)
        Si delScript est renseigné la fonction enverra la touche "effacer" jusqu'à ce que le javascript delScript retourne vrai pour effacer le champ.
        """
        try:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                #
                try:
                    if backspace==0 and delScript==None:
                        if self._driver.find_element_by_xpath(path).get_attribute('value')!="":
                            self._driver.find_element_by_xpath(path).clear();
                        else:
                            self._driver.find_element_by_xpath(path).send_keys(keys)
                            return True
                    elif backspace>0:
                        for i in range(backspace):
                            self._driver.find_element_by_xpath(path).send_keys("\b")
                        self._driver.find_element_by_xpath(path).send_keys(keys)
                        return True
                except Exception as e:
                    #print(e)
                    pass

                #print (elapsed_time)
                #
                if (elapsed_time>tOUT):
                    return False
            #self._driver.find_element_by_xpath(path).click();


        except Exception as ex:
            #print(ex)
            return False

    def getattrib(self, path, attrib, tOUT=1):
        """
        entrées : path et attrib des str, tOUT un entier positif
        sortie : str
        postcond : retourne l'attribut attrib de l'élément de chemin path en essayant à répetition jusqu'à tOUT secondes
        """
        try:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                #
                try:
                    val = self._driver.find_element_by_xpath(path).get_attribute(attrib)
                    return val
                except:
                    pass

                #print (elapsed_time)
                #
                if (elapsed_time>tOUT):
                    return None
            #self._driver.find_element_by_xpath(path).click();
        except Exception as ex:
            #print(ex)
            return None

    def gettext(self, path, tOUT=1):
        """
        entrées : path un str, tOUT un entier positif
        sortie : str
        postcond : retourne le texte de l'élément de chemin path en essayant à répetition jusqu'à tOUT secondes
        """
        try:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                #
                try:
                    val = self._driver.find_element_by_xpath(path).text
                    return val
                except:
                    pass

                #print (elapsed_time)
                #
                if (elapsed_time>tOUT):
                    return ""
            #self._driver.find_element_by_xpath(path).click();
        except Exception as ex:
            #print(ex)
            return ""

    def close(self):
        """
        sortie : bool
        postcond : retourne vrai si la fenêtre s'est fermée correctement, faux sinon
        """
        try:
            try:
                self._driver.quit()
            except:
                pass
            self._driver = None
            lock.acquire()
            global userdirs
            userdirs.append(self._user)
            lock.release()
            return True
        except Exception as ex:
            #print(ex)
            return False

    def screenShot(self, screenEmplacement):
        """
        entrée : screenEmplacement un str
        sortie : bool
        postcond : fais un screenshot et le sauvegarde à l'emplacement screenEmplacement, retourne vrai si le screenshot a bien été enregistré, faux sinon
        """
        try:
            self._driver.save_screenshot(screenEmplacement)
            return True
        except Exception as ex:
            #print(ex)
            return False

    def execscript(self, script):
        """
        entrée : script un str
        sortie : booléen
        postcond : execute le script script et retourne vrai s'il s'est bien executé, faux sinon
        """
        try:
            self._driver.execute_script(script)
            return True
        except Exception as ex:
            #print(ex)
            return False

    def openfiledialog(self, file, tOUT=5):
        """
        entrées : file un str, tOUT un entier positif
        precond : une boite de dialogue pour ouvrir un fichier sur le navigateur doit être ouverte
        sortie : booléen
        postcond : essaye d'ouvrir le fichier file pendant max tOUT secondes et retourne vrai s'il y arrive, faux sinon
        """
        dialogWindow = pywinauto.application.Application()

        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            #

            try:
                windowHandle = pywinauto.findwindows.find_windows(title=u'Open', class_name='#32770')[0]
                break
            except Exception as ex:
                pass
                #print(ex)

            #print (elapsed_time)
            #
            if (elapsed_time>tOUT):
                return False
        
        window = dialogWindow.connect(handle=windowHandle)

        window["Open"]["Edit1"].set_edit_text(file)

        try:
            r = True

            ouvrirtext = window.top_window()["Button1"].texts()[0]
            while ouvrirtext in window.top_window()["Button1"].texts()[0]:
                window["Open"]["Button1"].click()

            r = False

            while "OK" in window.top_window()["Button1"].texts()[0]:
                window.top_window()["Button1"].click()

            while ouvrirtext in window.top_window()["Button1"].texts()[0]:
                window.top_window()["Button2"].click()
        except Exception as ex:
            pass
            #print(ex)

        return r

    def changeframe(self, id):
        """
        entrée :
        sortie :
        postcond :
        """
        try:
            try:
                self._driver.switch_to.frame(id)
            except:
                self._driver.switch_to.frame(self._driver.find_element_by_xpath(id))
            return True
        except Exception as ex:
            print(ex)
            return False

    def default_content(self):
        """
        entrée :
        sortie :
        postcond :
        """
        try:
            self._driver.switch_to.default_content()
            return True
        except Exception as ex:
            #print(ex)
            return False

    def select(self, path, valueorindex, tOUT=5):
        """
        entrées : path un str, valueorindex un int ou un str, tOUT un entier positif
        sortie : bool
        postcond : retourne vrai si l'option de value ou d'index valueorindex est bien selectionnée
        """
        try:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                #
                try:
                    select = Select(self._driver.find_element_by_xpath(path))
                    if type(valueorindex)==int:
                        select.select_by_index(valueorindex)
                    else:
                        select.select_by_value(valueorindex)
                    return True
                except:
                    pass

                #print (elapsed_time)
                #
                if (elapsed_time>tOUT):
                    return False
            #self._driver.find_element_by_xpath(path).click();
        except Exception as ex:
            #print(ex)
            return False

    def getFocussedWin(self, tOUT=5):
        """

        """
        try:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                #
                try:
                    return(self._driver.window_handles.index(self._driver.current_window_handle))
                except:
                    pass

                #print (elapsed_time)
                #
                if (elapsed_time>tOUT):
                    return None
            #self._driver.find_element_by_xpath(path).click();
        except Exception as ex:
            #print(ex)
            return None

    def focusOnWin(self, win = 0, tOUT=5):
        """

        """
        try:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                #
                try:
                    self._driver.switch_to_window(self._driver.window_handles[win])
                    return True
                except:
                    pass

                #print (elapsed_time)
                #
                if (elapsed_time>tOUT):
                    return False
            #self._driver.find_element_by_xpath(path).click();
        except Exception as ex:
            #print(ex)
            return False

    def closeWin(self, tOUT=5):
        """

        """
        try:
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                #
                try:
                    f = self._driver.window_handles.index(self._driver.current_window_handle)
                    self._driver.close()
                    self._driver.switch_to_window(self._driver.window_handles[f-1])
                    return True
                except:
                    pass

                #print (elapsed_time)
                #
                if (elapsed_time>tOUT):
                    return False
            #self._driver.find_element_by_xpath(path).click();
        except Exception as ex:
            #print(ex)
            return False

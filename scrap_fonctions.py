import requests
from lxml import etree
import nav_fonctions

"""
Norme des dictionnaires de produits:

"prix" : le prix en euros (ex : "2.5")
"imgs" : un tableau de lien vers les images du produit (ex : ["http://lien1", "http://lien1"])

Je mettrai à jour au fur et à mesure
"""

def simple_scrap(url, xPathDict, useNav = False):
    """
    entrees : url un str, xPathDict un tableau à 2 dimentions [[clé, xPath, "text"], [clé, xPath, "val", 'champ'], [clé, xPath, "text"], ...] et useNav un booleen
    sortie : sortie un dictionnaire
    postcond : ...
    """
    sortie = {}
    for i in xPathDict:
        sortie[i[0]]=None
    if not useNav:
        try:
            resp = requests.get(url)
            tree = etree.HTML(resp.text)
            for i in xPathDict:
                if i[2]=='text':
                    try:
                        sortie[i[0]] = tree.xpath(i[1])[0].text
                    except:
                        sortie[i[0]] = None
                elif i[2]=='val':
                    try:
                        sortie[i[0]] = tree.xpath(i[1])[0].attrib[i[3]]
                    except:
                        sortie[i[0]] = None
        except Exception as e:
            print(e)
    else:
        try:
            resp = nav_fonctions.nav()
            resp.get(url)
            for i in xPathDict:
                if i[2]=='text':
                    try:
                        sortie[i[0]] = resp.gettext(i[1])
                    except:
                        sortie[i[0]] = None
                elif i[2]=='val':
                    try:
                        sortie[i[0]] = resp.getattrib(i[1], i[3])
                    except:
                        sortie[i[0]] = None
            resp.close()
        except Exception as e:
            print(e)
    return sortie

def scrap_all(url,xPath,val = None):
    """
    entrees : url et xPath des str et val n'importequoi (None ou un champ)
    sortie : sortie un tableau
    postcond : ...
    """
    sortie = []
    try:
        resp = requests.get(url)
        tree = etree.HTML(resp.text)
        for i in xPath:
            if val==None:
                try:
                    sortie += [i.text for i in tree.xpath(xPath)]
                except:
                    sortie = None
            else:
                try:
                    sortie += [i.attrib[val] for i in tree.xpath(xPath)]
                except:
                    sortie = None
    except Exception as e:
        print(e)
    return sortie

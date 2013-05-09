# -*-coding:iso-8859-1 -*
import sys,os,pygame,xml.dom.minidom
from pygame.locals import *
sys.path.append(os.pardir)
from interacteur import *

class Appli:
    def executer(self):
        """Exécute le script"""
        if len(sys.argv) < 2:
            print("Vous devez indiquer une image.")
            raise SystemExit
        cheminImage = sys.argv[1]
        cheminTileset = cheminImage[:cheminImage.find(".png")] + ".tsx"
        nomTileset = os.path.basename(cheminTileset)
        if os.path.lexists(cheminTileset) is True:
            print("Un tileset correspondant existe déjà.")
            interacteur = Interacteur()
            if interacteur.yesNoQuestion("Voulez-vous écraser le tileset {0} ?".format(nomTileset), yesParDefaut=False) is False:
                print("Très bien, nous ne ferons rien.")
                raise SystemExit
            else:
                print("Parfait !")
        try:
            surfaceTileset = pygame.image.load(cheminImage)
        except:
            print("Impossible de charger {0}".format(cheminImage))
            raise SystemExit
        orgaXML = xml.dom.minidom.getDOMImplementation().createDocument(None,"tileset",None)
        tilesetXML = orgaXML.documentElement
        tilesetXML.setAttribute("name",nomTileset)
        tilesetXML.setAttribute("tilewidth","32")
        tilesetXML.setAttribute("tileheight","32")
        tilesetXML.appendChild(orgaXML.createElement("image"))
        imageXML = tilesetXML.getElementsByTagName("image")[0]
        imageXML.setAttribute("source", nomTileset )
        longueur,largeur = surfaceTileset.get_width(), surfaceTileset.get_height()
        imageXML.setAttribute("width", str(longueur) )
        imageXML.setAttribute("height", str(largeur) )
        nombreTiles = int(longueur / 32) * int(largeur / 32)
        i = 0
        while i < nombreTiles:
            tile = orgaXML.createElement("tile")
            tile.setAttribute("id",str(i))
            tilesetXML.appendChild(tile)
            propris = orgaXML.createElement("properties")
            tile.appendChild(propris)
            propri = orgaXML.createElement("property")
            propri.setAttribute("name","Praticabilite")
            propri.setAttribute("value","True")
            propris.appendChild(propri)
            i += 1
        with open(cheminTileset,"w") as fichier:
            orgaXML.writexml(fichier, addindent="    ", newl="\n", encoding="UTF-8")
        orgaXML.unlink()
        print("Le tileset {0} a bien été créé !".format(nomTileset))

if __name__ == "__main__":
    appli = Appli()
    appli.executer()


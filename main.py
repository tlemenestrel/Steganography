# Stéganographie - v0.1
# Ce script est l'interface d'un programme qui dissimule du texte dans une image
# License libre CC
# Colin Laganier - Thomas Lemenestrel - 2017.12.13

from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import *
from PIL import Image, ImageTk

root = Tk() # On crée une fenêtre
root.geometry('800x600') # On donne les dimensions de la fenêtre
root.configure(background='#333d4f')

frameTitle = Frame(root, bg="yellow", colormap="new")
frameTitle.pack(side=TOP)

title = Label(frameTitle, text="STEGANOGRAPHIE", bg="#333d4f", fg="white", font=("Helvetica", 16)) # Titre du programme à display
title.pack()

frameImg = Frame(root, bg="light grey", colormap="new")
frameImg.pack(side = TOP, pady = 3)

canvas = Canvas(frameImg, width=500, height=350) # Création d'une zone canvas
canvas.pack(side=LEFT)

canvas.create_rectangle(0, 0, 500, 350, fill="white") # Création d'un rectangle pour indiquer où l'image inséré sera placer
canvas.pack(side=LEFT)

imgName = 0
message = " "

def InsertImg(): # Fonction pour déterminer et insérer l'image dans l'interface
	global imgName, largeur, hauteur
	imgName = filedialog.askopenfilename(initialdir = "/",title = "Choisir image",filetypes = (("png files","*.png"),("all files","*.*")))
	image = Image.open(imgName)
	imgBrut= ImageTk.PhotoImage(image)
	labelImg = Label(canvas, image = imgBrut)
	labelImg.image = imgBrut
	labelImg.pack()

boutonInsertImg = Button(frameImg, text = 'Insert Image', command = InsertImg) # Bouton pour insérer image
boutonInsertImg.pack(side = LEFT, padx = 5)

frameVar = Frame(root, bg="pink", colormap="new")
frameVar.pack(side = TOP)

def InsertText(): # Fonction qui verifie l'image et qui initie le programme
    if imgName == 0:
        showinfo("Erreur", "Il faut inseré une image pour faire fonctionner le programme !")
    im = Image.open(imgName)
    #on récupère les dimensions de l'image
    largeur,hauteur=im.size
    #On éclate l'image en trois (rouge vert bleu)
    r,g,b=im.split()
    #on transforme l'image en liste
    redPix=list(r.getdata())
    print(redPix[2:30])
    #le message à  coder
    Texte=entreTxt.get() # On importe le texte depuis l'interface TKinter
    #on note la longueur de la chaine et on la transforme en binaire
    longTxt=len(Texte)
    longBin=bin(len(Texte))[2:].rjust(8,"0")
    #on transforme la chaine en une liste de 0 et de 1
    ListeBinaire=[bin(ord(x))[2:].rjust(8,"0") for x in Texte]
    #transformation de la liste en chaine
    ChaineBinaire=''.join(ListeBinaire)
    #on code la longueur de la liste dans les 8 premiers pixels rouges
    for j in range(8):
        redPix[j]=2*int(redPix[j]//2)+int(longBin[j])
    #on code la chaine dans les pixels suivants
    for i in range(8*longTxt):
        redPix[i+8]=2*int(redPix[i+8]//2)+int(ChaineBinaire[i])
    # On recrée l'image rouge, avec "L" pour obtenir une image avec seulement un faisceau/une couleur
    ImageRefaite = Image.new("L",(largeur,hauteur))
    ImageRefaite.putdata(redPix)
    # On fusionne les trois images RGB pour donner l'image finale
    ImageFinale = Image.merge('RGB',(ImageRefaite,g,b))
    nomSave = entreNom.get() + ".png"
    ImageFinale.save(nomSave, format="png")
    print(redPix[2:30])

def InsertCode():
    global message
    im = Image.open(imgName) # On importe l'image avec le message codé
    r,g,b=im.split() # On redivise l'image en rouge, vert, bleu transparent
    redPix2=list(r.getdata())
    #lecture de la longueur de la chaine
    Listelong=[str(x%2) for x in redPix2[0:8]]
    Stringlong="".join(Listelong)
    Stringlong=int(Stringlong,2)
    #lecture du message
    MsgList=[str(x%2) for x in redPix2[8:8*(Stringlong+1)]]
    MsgString="".join(MsgList)
    message=""
    for k in range(0,Stringlong):
        StringFin=MsgString[8*k:8*k+8]
        message=message+chr(int(StringFin,2))
    return message


def fonctionEntre(): # Fonction qui insert zone d'entrée de texte
    if canvasSortie.winfo_exists() == 1: # Si zone d'entré est déja ouverte, détruit pour afficher
        canvasSortie.destroy()
    elif boiteStart1.winfo_exists() == 1:
    	boiteStart1.destroy()
    	boiteStart2.destroy()
    	boutonInsertTextStart.destroy()
    elif boite3.winfo_exists() == 1:
    	boite3.destroy()
    	canvasSortie.destroy()
    global entreTxt, boite1, boite2, boutonInsertText, entreNom
    entreTxt = StringVar()
    boite1 = Entry(frameTxt, textvariable = entreTxt, bg = '#009999', width = '40') # Zone entré du texte
    boite1.insert(0, 'Texte à dissimuler')
    boite1.bind("<FocusIn>", lambda args: boite1.delete('0', 'end'))
    boite1.pack(side = LEFT, ipady = 15)
    entreNom = StringVar()
    boite2 = Entry(frameTxt, textvariable = entreNom, bg = '#009999', width = '15') # Zone entré du nom de la nouvelle image
    boite2.insert(0, 'Nouveau nom')
    boite2.bind("<FocusIn>", lambda args: boite2.delete('0', 'end'))
    boite2.pack(side = LEFT, padx = 20, ipady = 15)
    boutonInsertText = Button(frameTxt,text = 'Insert Text', command = InsertText) 
    boutonInsertText.pack(side = LEFT, padx = 10)        

def fonctionSortie(): # Fonction qui display le texte dissimuler dans une image
    global canvasSortie, boite3
    if boiteStart1.winfo_exists() == 1:
    	boiteStart1.destroy()
    	boiteStart2.destroy()
    	boutonInsertTextStart.destroy()
    elif boite1.winfo_exists() == 1:
        boite1.destroy()
        boite2.destroy()
        boutonInsertText.destroy()
    elif boite3.winfo_exists() == 1:
    	boite3.destroy()
    	canvasSortie.destroy()
    canvasSortie = Canvas(frameTxt, width=420, height=50, bg="#009999") # Création d'une canvas pour display le texte dissimulé dans l'image
    canvasSortie.pack(side = LEFT)
    boite3 = canvasSortie.create_text((75,27), text=InsertCode())

boutonEntre = Button(frameVar, text='Entre', command = fonctionEntre) # Bouton pour inséré du texte dans une image, premiere fonciton du programme
boutonEntre.pack(side = LEFT)

boutonSortie = Button(frameVar, text='Sortie', command = fonctionSortie) # Bouton pour traiter et obtenir le texte dissimulé dans une image, deuxieme fonction du programme
boutonSortie.pack(side = LEFT)


frameTxt = Frame(root, bg="#333d4f", colormap="new")
frameTxt.pack(side = TOP, pady = 20)

global entreTxt, boite1, boite2, boutonInsertText, entreNom # Zone d'entrée de texte display a l'ouverture de l'interface
entreTxt = StringVar()
boiteStart1 = Entry(frameTxt, textvariable = entreTxt, bg = '#009999', width = '40')
boiteStart1.insert(0, 'Texte à dissimuler')
boiteStart1.bind("<FocusIn>", lambda args: boiteStart1.delete('0', 'end'))
boiteStart1.pack(side = LEFT, ipady = 15)
entreNom = StringVar()
boiteStart2 = Entry(frameTxt, textvariable = entreNom, bg = '#009999', width = '15')
boiteStart2.insert(0, 'Nouveau nom')
boiteStart2.bind("<FocusIn>", lambda args: boiteStart2.delete('0', 'end'))
boiteStart2.pack(side = LEFT, padx = 20, ipady = 15)
boutonInsertTextStart = Button(frameTxt,text = 'Insert Text', command = InsertText)
boutonInsertTextStart.pack(side = LEFT, padx = 10) 

frameSup = Frame(root, bg="pink", colormap="new")
frameSup.pack(side = TOP, pady = 13)

def InsertInfo(): # information a propos de l'utilisation du programme
	showinfo("Information", "Ce programme dissimule un un texte dans votre image ! \nPour faire fonctionner le programme :\n      # Insérez une image\n      # Insérez votre texte ainsi que le nom de la nouvelle image\n      # Appuyez sur le bouton 'insert text'\nPour afficher le code dissimulé dans une image, ré-ouvrir le programme et charger l'image en question et suivre les instruction du bouton 'Sortie'")

boutonInfo = Button(frameSup, text='Info', command = InsertInfo) # Bouton pour fournir des informations a propos du programme
boutonInfo.pack(side = RIGHT)

boutonExit = Button(frameSup, text='Exit', command = root.destroy) # Bouton pour fermer le programme
boutonExit.pack(side = RIGHT)

root.mainloop() # On démarre la boucle Tkinter qui s'interompt quand on ferme la fenêtre

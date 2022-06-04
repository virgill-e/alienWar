import sqlite3
from tkinter import *
import smtplib, ssl
from random import randint
import pygame
import sys
from menu import main_menu
import hashlib


class Pagedeco(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("fenetre de connexion")
        self['bg'] = '#2693BC'
        self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.adresse=""
        self.code=""
        self.point=0
        
        #image bouton
        self.img_Bouton_valider = PhotoImage( file="img/bouton/bout_valider.png" )
        self.img_Bouton_quitter = PhotoImage( file="img/bouton/bout_quitter.png" )
        self.img_Bouton_connexion = PhotoImage( file="img/bouton/bout_connexion.png" )
        self.img_Bouton_inscription = PhotoImage( file="img/bouton/bout_inscription.png" )

        #base de donnée
        self.connex= sqlite3.connect("BigVir_bd.sq3")#création connexion
        self.cur= self.connex.cursor() #création curseur
        #taille colonne/ligne
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=5)
        self.rowconfigure(7, weight=5)

        #image logo
        can1 = Canvas(self, width =400, height =200, bg ='white')
        photo = PhotoImage(file ='img/logo_tfe.png')
        can1.create_image(200, 100, image =photo)
        can1.grid(row=0,column=0,columnspan=2,sticky='s')

        #label + entry
        self.labeladresse=Label(self,text="adresse mail: ",fg="white",bg="#5E8796")
        self.labelcode=Label(self,text="mot de passe: ",fg="white",bg="#5E8796")
        self.labelerreur=Label(self,text="",fg="white",bg="#2693BC")
        self.entradresse = Entry(self)
        self.entrcode = Entry(self,show = "*")
        
        self.labeladresse.grid(row=1,column=0,sticky="se")
        self.labelcode.grid(row=2,column=0,sticky="e")
        self.entradresse.grid(row=1,column=1,sticky="sw")
        self.entrcode.grid(row=2,column=1,sticky="w")
        self.labelerreur.grid(row=5,column=1,sticky="nw")
        
        #boutton
        bouconnexion = Button(self,height=100, width=300, image=self.img_Bouton_connexion, command=self.connexion)
        bouinscription = Button(self,height=100, width=300, image=self.img_Bouton_inscription,command=self.inscription)
        bouttonquitter=Button(self,height=100, width=300, image=self.img_Bouton_quitter, command=self.quit)
        bouconnexion.grid(row=3,column=1,sticky="sw")
        bouinscription.grid(row=4,column=1,sticky="nw")
        bouttonquitter.grid(row=7,column=1,sticky="se")

        print("Il faut faire un ratio pour la taille des bouton des le menu et pour les images genre logo !!!")
        
        
        self.mainloop()



    def inscription(self):#s'inscrire
        self.adresse,self.code=self.entradresse.get(),self.entrcode.get()
        self.labelerreur.configure(text ="",bg="#2693BC")
        if self.adresse!="" and self.code!="":
            self.cur.execute("SELECT adresse FROM joueur WHERE adresse = '" + self.adresse + "'")
            lrep=self.cur.fetchall()#transforme la reponse en liste de tuple --> l'utiliser
            if len(lrep)==0:
                h = hashlib.md5(self.code.encode())
                self.cur.execute("INSERT INTO joueur(adresse,code,niveau_max,niveau_actuel,argent,degat,vie,prix) VALUES(?,?,?,?,?,?,?,?)",(self.adresse,h.hexdigest(),0,1,0,0,0,1))
                self.connex.commit()#valider les modifications
                self.jeu()
            else:
                self.labelerreur.configure(text ="adresse déja existant",bg="#5E8796")
        else:
            if self.adresse=="":
                self.labelerreur.configure(text ="Entrez votre adresse !",bg="#5E8796")
            else:
                self.labelerreur.configure(text ="Entrez votre mot de passe !",bg="#5E8796")


    def connexion(self):#se connecter
        self.adresse,self.code=self.entradresse.get(),self.entrcode.get()
        if self.adresse!="" and self.code!="":
            self.cur.execute("SELECT * FROM joueur WHERE adresse = '" + self.adresse + "'")
            lrep=self.cur.fetchall()#transforme la reponse en liste de tuple --> l'utiliser
            if len(lrep)!=0:
                h = hashlib.md5(self.code.encode())
                print(h.hexdigest())
                if h.hexdigest()==lrep[0][2]:
                    self.labelerreur.configure(text ="Vous êtes connecté !",bg="#5E8796")
                    self.jeu()
                else:
                    self.labelerreur.configure(text ="mot de passe ou adresse incorrect",bg="#5E8796")
        else:
            if self.adresse=="":
                self.labelerreur.configure(text ="entrez votre adresse",bg="#5E8796")
            else:
                self.labelerreur.configure(text ="entrez votre mot de passe",bg="#5E8796")




    def jeu(self):
        self.destroy()
        main_menu(self,self.adresse)


app=Pagedeco()
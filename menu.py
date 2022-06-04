import sqlite3
from tkinter import * 
import pygame 
from mainpygame import maindupygame
import sys
import webbrowser


class Menu(Tk):
    def __init__(self,adresse):
        Tk.__init__(self)

        self.title("Menu")
        self['bg'] = '#2693BC'
        self.overrideredirect(True)
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight())) #mettre en pleine ecran


        #base de donnée
        self.connex= sqlite3.connect("BigVir_bd.sq3")#création connexion
        self.cur= self.connex.cursor() #création curseur

        self.adresse=adresse


        self.lichoixSkin=["img/skin/witch.png","img/skin/witch_inverse.png"]
        self.largeur=self.winfo_screenwidth()#adaptation taille de l'écran
        self.hauteur=self.winfo_screenheight()
        


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=3)
        #image logo
        can1 = Canvas(self, width =400, height =200, bg ='white')
        photo = PhotoImage(file ='img/logo_tfe.png')
        can1.create_image(200, 100, image =photo)
        can1.grid(row=0,column=1,sticky='s')

        #label
        self.cur.execute("SELECT niveau_actuel,niveau_max FROM joueur WHERE adresse = '" + self.adresse + "'")
        lrep=self.cur.fetchall()
        self.niveau_actuel=lrep[0][0]
        self.niveau_max=lrep[0][1]
        self.label_niveau_actuel=Label(self,text="niveau actuel: "+str(self.niveau_actuel),font=("Courier", 30))
        self.label_niveau_actuel.grid(row=0,column=0,sticky="s")

        self.label_niveau_max=Label(self,text="niveau max: "+str(self.niveau_max),font=("Courier", 30))
        self.label_niveau_max.grid(row=0,column=0,sticky="n")


        #Image des boutons
        self.img_Bouton_continuer = PhotoImage( file="img/bouton/bout_continuer.png" )
        self.img_Bouton_recomencer = PhotoImage( file="img/bouton/bout_recommencer.png" )
        self.img_Bouton_shop = PhotoImage( file="img/bouton/bout_shop.png" )
        self.img_Bouton_skin = PhotoImage( file="img/bouton/bout_skin.png" )
        self.img_Bouton_trophee = PhotoImage( file="img/bouton/bout_trophee.png" )
        self.img_Bouton_quitter = PhotoImage( file="img/bouton/bout_quitter.png" )
        self.img_Bouton_classement = PhotoImage( file="img/bouton/bout_classement.png" )
        self.img_Bouton_site = PhotoImage( file="img/bouton/bout_site.png" )
        self.img_Bouton_site = PhotoImage( file="img/bouton/bout_site.png" )
        self.img_Bouton_valider = PhotoImage( file="img/bouton/bout_valider.png" )
        self.img_Bouton_amelioration = PhotoImage( file="img/bouton/bout_amelioration.png" )

        #bouton
        boucontinuer = Button(self, height=100, width=300, image=self.img_Bouton_continuer,command=self.continuer)
        bourestart = Button(self, height=100, width=300, image=self.img_Bouton_recomencer, command=self.restart)
        boushop = Button(self, height=100, width=300, image=self.img_Bouton_shop,command=self.shop)
        bouskin = Button(self, height=100, width=300, image=self.img_Bouton_skin,command=self.ecran_skin)
        boutson = Button(self, height=100, width=300, image=self.img_Bouton_trophee,command=self.trophee)
        bouquitter = Button(self, height=100, width=300, image=self.img_Bouton_quitter, command=self.fermer_fenetre)
        bouclassement = Button(self, height=100, width=300, image=self.img_Bouton_classement,command=self.top5)
        boupageweb = Button(self, height=100, width=300, image=self.img_Bouton_site,command=self.ouvrir_site)

        boushop.grid(row=2,column=0,sticky='n')
        bouskin.grid(row=3,column=0,sticky='n')
        boucontinuer.grid(row=1,column=1,sticky='s')
        bourestart.grid(row=2,column=1,sticky='n')
        boutson.grid(row=3,column=1,sticky='n')
        bouquitter.grid(row=0,column=2)
        bouclassement.grid(row=2,column=2,sticky='n')
        boupageweb.grid(row=3,column=2,sticky='n')


        self.mainloop()

    def trophee(self):

        self.trophee_tpl=Toplevel(self)
        self.trophee_tpl.title("trophee")
        self.trophee_tpl['bg'] = '#2693BC'
        self.trophee_tpl.overrideredirect(True)
        self.trophee_tpl.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

        self.trophee_tpl.rowconfigure(0, weight=1)
        self.trophee_tpl.rowconfigure(1, weight=1)
        self.trophee_tpl.rowconfigure(2, weight=1)

        self.trophee_tpl.columnconfigure(0, weight=1)
        self.trophee_tpl.columnconfigure(1, weight=1)
        self.trophee_tpl.columnconfigure(2, weight=1)
        self.trophee_tpl.columnconfigure(3, weight=1)
        self.trophee_tpl.columnconfigure(4, weight=1)

        li_trophee=['img/boss/menu/snake.png','img/boss/menu/ghost.png','img/boss/menu/dragon.png','img/boss/menu/zeus.png','img/boss/menu/alien.png']
        li_trophee_hide=['img/boss/menu/hide/snake.png','img/boss/menu/hide/ghost.png','img/boss/menu/hide/dragon.png','img/boss/menu/hide/zeus.png','img/boss/menu/hide/alien.png']


        #-----------------------------image des trophee--------------------------------------------------------------

        #can snake
        can_trophee_snake = Canvas(self.trophee_tpl, width =256, height =256, bg ='white')#skin witch
        if self.niveau_max>10:
            self.trophee_snake = PhotoImage(file =li_trophee[0])
            self.labelsnake=Label(self.trophee_tpl,text="SNAKE",fg="white",bg="#2693BC",font=("Courier", 30))
        else:
            self.trophee_snake = PhotoImage(file =li_trophee_hide[0])
            self.labelsnake=Label(self.trophee_tpl,text="???",fg="white",bg="#2693BC",font=("Courier", 30))
        self.labelsnake.grid(row=1,column=0,sticky="s")
        can_trophee_snake.create_image(128,128, image =self.trophee_snake)
        can_trophee_snake.grid(row=1,column=0)

        #can ghost
        can_trophee_ghost = Canvas(self.trophee_tpl, width =256, height =256, bg ='white')#skin witch
        if self.niveau_max>20:
            self.trophee_ghost = PhotoImage(file =li_trophee[1])
            self.labelghost=Label(self.trophee_tpl,text="GHOST",fg="white",bg="#2693BC",font=("Courier", 30))
        else:
            self.trophee_ghost = PhotoImage(file =li_trophee_hide[1])
            self.labelghost=Label(self.trophee_tpl,text="???",fg="white",bg="#2693BC",font=("Courier", 30))
        can_trophee_ghost.create_image(128,128, image=self.trophee_ghost)
        can_trophee_ghost.grid(row=1,column=1)
        self.labelghost.grid(row=1,column=1,sticky="s")

        #can dragon
        can_trophee_dragon = Canvas(self.trophee_tpl, width =256, height =256, bg ='white')#skin witch
        if self.niveau_max>30:
            self.trophee_dragon = PhotoImage(file =li_trophee[2])
            self.labeldragon=Label(self.trophee_tpl,text="DRAGON",fg="white",bg="#2693BC",font=("Courier", 30))
        else:
            self.trophee_dragon = PhotoImage(file =li_trophee_hide[2])
            self.labeldragon=Label(self.trophee_tpl,text="???",fg="white",bg="#2693BC",font=("Courier", 30))
        can_trophee_dragon.create_image(128, 128, image =self.trophee_dragon)
        can_trophee_dragon.grid(row=1,column=2)
        self.labeldragon.grid(row=1,column=2,sticky="s")

        #can zeus
        can_trophee_zeus = Canvas(self.trophee_tpl, width =256, height =256, bg ='white')#skin witch
        if self.niveau_max>40:
            self.trophee_zeus = PhotoImage(file =li_trophee[3])
            self.labelzeus=Label(self.trophee_tpl,text="ZEUS",fg="white",bg="#2693BC",font=("Courier", 30))
        else:
            self.trophee_zeus = PhotoImage(file =li_trophee_hide[3])
            self.labelzeus=Label(self.trophee_tpl,text="???",fg="white",bg="#2693BC",font=("Courier", 30))
        can_trophee_zeus.create_image(128, 128, image =self.trophee_zeus)
        can_trophee_zeus.grid(row=1,column=3)
        self.labelzeus.grid(row=1,column=3,sticky="s")

        #can alien
        can_trophee_alien = Canvas(self.trophee_tpl, width =256, height =256, bg ='white')#skin witch
        if self.niveau_max>50:
            self.trophee_alien = PhotoImage(file =li_trophee[4])
            self.labelalien=Label(self.trophee_tpl,text="ALIEN",fg="white",bg="#2693BC",font=("Courier", 30))
        else:
            self.trophee_alien = PhotoImage(file =li_trophee_hide[4])
            self.labelalien=Label(self.trophee_tpl,text="???",fg="white",bg="#2693BC",font=("Courier", 30))
        can_trophee_alien.create_image(128, 128, image =self.trophee_alien)
        can_trophee_alien.grid(row=1,column=4)
        self.labelalien.grid(row=1,column=4,sticky="s")

        boutquitter = Button(self.trophee_tpl, height=100, width=300, image=self.img_Bouton_quitter,command=self.trophee_tpl.destroy)
        boutquitter.grid(row=2,column=2)

    def restart(self):
        self.cur.execute("SELECT niveau_actuel FROM joueur WHERE adresse = '" + self.adresse + "'")
        lrep=self.cur.fetchall()
        niveau_actuel=str(lrep[0][0])
        self.cur.execute("UPDATE joueur SET niveau_actuel='1' WHERE niveau_actuel='"+niveau_actuel+"' and adresse='" + self.adresse + "'")
        self.connex.commit()

        maindupygame(self,self.largeur,self.hauteur,self.adresse,self.lichoixSkin,1)
    
    def continuer(self):
        self.cur.execute("SELECT niveau_actuel FROM joueur WHERE adresse = '" + self.adresse + "'")
        lrep=self.cur.fetchall()
        niveau_actuel=str(lrep[0][0])
        maindupygame(self,self.largeur,self.hauteur,self.adresse,self.lichoixSkin,int(niveau_actuel))


    def top5(self):
        self.top5_tpl=Toplevel(self)
        self.top5_tpl.title("Top 5")
        self.top5_tpl['bg'] = '#2693BC'
        self.top5_tpl.overrideredirect(True)
        self.top5_tpl.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.cur.execute("SELECT adresse,niveau_max FROM joueur ORDER BY niveau_max DESC ")#doit se trier par seconde
        lclassement=self.cur.fetchall()

        self.top5_tpl.columnconfigure(0, weight=1)
        self.top5_tpl.columnconfigure(1, weight=1)

        self.top5_tpl.rowconfigure(0, weight=1)
        self.top5_tpl.rowconfigure(1, weight=1)
        self.top5_tpl.rowconfigure(2, weight=1)
        self.top5_tpl.rowconfigure(3, weight=1)
        self.top5_tpl.rowconfigure(4, weight=1)
        self.top5_tpl.rowconfigure(5, weight=1)
        self.top5_tpl.rowconfigure(6, weight=3)

        #boutton
        bouquitter = Button(self.top5_tpl, height=100, width=300, image=self.img_Bouton_quitter, command=self.top5_tpl.destroy)
        bouquitter.grid(row=6,column=0,columnspan=2)

        self.labelnomtop1=Label(self.top5_tpl,text=lclassement[0][0]+"->",font=("Courier", 30),background="gold")
        self.labelnomtop2=Label(self.top5_tpl,text=lclassement[1][0]+"->",font=("Courier", 30),background="silver")
        self.labelnomtop3=Label(self.top5_tpl,text=lclassement[2][0]+"->",font=("Courier", 30),background="#cd7f32")
        self.labelnomtop4=Label(self.top5_tpl,text=lclassement[3][0]+"->",font=("Courier", 30),background='#2693BC')
        self.labelnomtop5=Label(self.top5_tpl,text=lclassement[4][0]+"->",font=("Courier", 30),background='#2693BC')

        self.labelnomtop1.grid(column=0,row=1,sticky="e")
        self.labelnomtop2.grid(column=0,row=2,sticky="e")
        self.labelnomtop3.grid(column=0,row=3,sticky="e")
        self.labelnomtop4.grid(column=0,row=4,sticky="e")
        self.labelnomtop5.grid(column=0,row=5,sticky="e")

        self.labelpointtop1=Label(self.top5_tpl,text=str(lclassement[0][1])+"points",font=("Courier", 30),background="gold")
        self.labelpointtop2=Label(self.top5_tpl,text=str(lclassement[1][1])+"points",font=("Courier", 30),background="silver")
        self.labelpointtop3=Label(self.top5_tpl,text=str(lclassement[2][1])+"points",font=("Courier", 30),background="#cd7f32")
        self.labelpointtop4=Label(self.top5_tpl,text=str(lclassement[3][1])+"points",font=("Courier", 30),background='#2693BC')
        self.labelpointtop5=Label(self.top5_tpl,text=str(lclassement[4][1])+"points",font=("Courier", 30),background='#2693BC')

        self.labelpointtop1.grid(column=1,row=1,sticky="w")
        self.labelpointtop2.grid(column=1,row=2,sticky="w")
        self.labelpointtop3.grid(column=1,row=3,sticky="w")
        self.labelpointtop4.grid(column=1,row=4,sticky="w")
        self.labelpointtop5.grid(column=1,row=5,sticky="w")


    def ouvrir_site(self):
        webbrowser.open('http://www.virgill-e.be/pages/contact.php')
    def fermer_fenetre(self):
        self.destroy()

    def ecran_skin(self):
        self.skin_tpl=Toplevel(self)
        self.skin_tpl.title("Skin")
        self.skin_tpl['bg'] = '#2693BC'
        self.skin_tpl.overrideredirect(True)
        self.skin_tpl.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        
        #taille colonne / ligne
        self.skin_tpl.columnconfigure(0, weight=1)
        self.skin_tpl.columnconfigure(1, weight=1)
        self.skin_tpl.columnconfigure(2, weight=1)

        self.skin_tpl.rowconfigure(0, weight=1)
        self.skin_tpl.rowconfigure(1, weight=1)
        self.skin_tpl.rowconfigure(2, weight=1)
        self.skin_tpl.rowconfigure(3, weight=1)
        self.skin_tpl.rowconfigure(4, weight=1)
        self.skin_tpl.rowconfigure(5, weight=1)
        self.skin_tpl.rowconfigure(6, weight=1)

        #boutton
        bouquitter = Button(self.skin_tpl, height=100, width=300, image=self.img_Bouton_quitter, command=self.skin_tpl.destroy)
        bouquitter.grid(row=4,column=0,sticky="e")

        bouvalider = Button(self.skin_tpl, height=100, width=300, image=self.img_Bouton_valider,command=self.valider_choix_skin)
        bouvalider.grid(row=4,column=2,sticky="w")

        #radio bouton
        self.var_skin=StringVar()
        self.var_skin.set("1")

        radio_skin1=Radiobutton(self.skin_tpl,text="Witch",variable=self.var_skin,value='witch',bg='#2693BC')
        radio_skin1.grid(row=1,column=0)

        radio_skin2=Radiobutton(self.skin_tpl,text="Witch Brown",variable=self.var_skin,value='witchBrun',bg='#2693BC')
        radio_skin2.grid(row=1,column=1)

        radio_skin2=Radiobutton(self.skin_tpl,text="Witch dark matter",variable=self.var_skin,value='witchDarkmatter',bg='#2693BC')
        radio_skin2.grid(row=1,column=2)

        radio_skin3=Radiobutton(self.skin_tpl,text="Witch gold",variable=self.var_skin,value='witchGold',bg='#2693BC')
        radio_skin3.grid(row=3,column=0)

        radio_skin4=Radiobutton(self.skin_tpl,text="Witch purple",variable=self.var_skin,value='witchMauve',bg='#2693BC')
        radio_skin4.grid(row=3,column=1)

        radio_skin5=Radiobutton(self.skin_tpl,text="Witch space",variable=self.var_skin,value='witchSpace',bg='#2693BC')
        radio_skin5.grid(row=3,column=2)

        #image
        can_skin1 = Canvas(self.skin_tpl, width =256, height =256, bg ='white')#skin witch
        self.photo_skin1 = PhotoImage(file ='img/skin/witch.png')
        can_skin1.create_image(128, 128, image =self.photo_skin1)
        can_skin1.grid(row=0,column=0)

        can_skin2 = Canvas(self.skin_tpl, width =256, height =256, bg ='white')#skin witchBrun
        self.photo_skin2 = PhotoImage(file ='img/skin/witchBrun.png')
        can_skin2.create_image(128, 128, image =self.photo_skin2)
        can_skin2.grid(row=0,column=1)

        can_skin3 = Canvas(self.skin_tpl, width =256, height =256, bg ='white')#skin witchDarkmatter
        self.photo_skin3 = PhotoImage(file ='img/skin/witchDarkmatter.png')
        can_skin3.create_image(128, 128, image =self.photo_skin3)
        can_skin3.grid(row=0,column=2)

        can_skin4 = Canvas(self.skin_tpl, width =256, height =256, bg ='white')#skin witchGold
        self.photo_skin4 = PhotoImage(file ='img/skin/witchGold.png')
        can_skin4.create_image(128, 128, image =self.photo_skin4)
        can_skin4.grid(row=2,column=0)

        can_skin5 = Canvas(self.skin_tpl, width =256, height =256, bg ='white')#skin witchMauve
        self.photo_skin5 = PhotoImage(file ='img/skin/witchMauve.png')
        can_skin5.create_image(128, 128, image =self.photo_skin5)
        can_skin5.grid(row=2,column=1)
        
        can_skin6 = Canvas(self.skin_tpl, width =256, height =256, bg ='white')#skin witchMauve
        self.photo_skin6 = PhotoImage(file ='img/skin/witchSpace.png')
        can_skin6.create_image(128, 128, image =self.photo_skin6)
        can_skin6.grid(row=2,column=2)

    def valider_choix_skin(self):
        self.lichoixSkin=["img/skin/"+self.var_skin.get()+".png","img/skin/"+self.var_skin.get()+"_inverse.png"]

    def shop(self):
        self.shop_tpl=Toplevel(self)
        self.shop_tpl.title("Shop")
        self.shop_tpl['bg'] = '#2693BC'
        self.shop_tpl.overrideredirect(True)
        self.shop_tpl.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

        self.shop_tpl.columnconfigure(0, weight=1)
        self.shop_tpl.columnconfigure(1, weight=1)
        self.shop_tpl.columnconfigure(2, weight=1)

        self.shop_tpl.rowconfigure(0, weight=1)
        self.shop_tpl.rowconfigure(1, weight=1)
        self.shop_tpl.rowconfigure(2, weight=1)
        self.shop_tpl.rowconfigure(3, weight=1)

        #image logo shop
        can_shop = Canvas(self.shop_tpl, width =400, height =200, bg ='#2693BC',highlightthickness=0)#skin witch
        self.photo_shop = PhotoImage(file ='img/logo_shop.png')
        can_shop.create_image(200, 100, image =self.photo_shop)
        can_shop.grid(row=0,column=1)

        #image vie
        can_shop_vie = Canvas(self.shop_tpl, width =256, height =256, bg ='white')#skin witch
        self.photo_shop_vie = PhotoImage(file ='img/vie.png')
        can_shop_vie.create_image(128, 128, image =self.photo_shop_vie)
        can_shop_vie.grid(row=1,column=0,sticky="e")

        #image degat
        can_shop_degat = Canvas(self.shop_tpl, width =256, height =256, bg ='white')#skin witch
        self.photo_shop_degat = PhotoImage(file ='img/degat.png')
        can_shop_degat.create_image(128, 128, image =self.photo_shop_degat)
        can_shop_degat.grid(row=2,column=0,sticky="e")

        #bouton du shop
        bou_upgrade_vie = Button(self.shop_tpl,height=100, width=300, image=self.img_Bouton_amelioration,command=lambda:self.upgrade(0) )
        bou_upgrade_vie.grid(row=1,column=1)

        bou_upgrade_degat = Button(self.shop_tpl,height=100, width=300, image=self.img_Bouton_amelioration,command=lambda:self.upgrade(1))
        bou_upgrade_degat.grid(row=2,column=1)

        bou_quitter = Button(self.shop_tpl, height=100, width=300, image=self.img_Bouton_quitter,command=self.shop_tpl.destroy)
        bou_quitter.grid(row=3,column=2,sticky="e")

        #label
        self.cur.execute("SELECT vie,degat,argent,prix FROM joueur where adresse='"+self.adresse+"' ")
        lrep=self.cur.fetchall()
        vie=lrep[0][0]
        self.label_vie=Label(self.shop_tpl,text="Niveau de vie: "+str(vie),font=("Courier", 30))
        self.label_vie.grid(row=1,column=2,sticky="w")

        degat=lrep[0][1]
        self.label_degat=Label(self.shop_tpl,text="Niveau de degat: "+str(degat),font=("Courier", 30))
        self.label_degat.grid(row=2,column=2,sticky="w")

        self.label_argent=Label(self.shop_tpl,text="argent: "+str(round(lrep[0][2],2)),font=("Courier", 30),fg="blue")
        self.label_argent.grid(row=0,column=0,sticky="nw")

        self.label_prix=Label(self.shop_tpl,text="prix: "+str(round(lrep[0][3],2)),font=("Courier", 30),fg="blue")
        self.label_prix.grid(row=0,column=2,sticky="ne")

    def upgrade(self,comp):
        #récupértion valeur actuel
        self.cur.execute("SELECT vie,degat,argent,prix FROM joueur where adresse='"+self.adresse+"' ")
        lrep=self.cur.fetchall()
        vie_actuel=int(lrep[0][0])
        degat_actuel=int(lrep[0][1])
        argent_actuel=float(lrep[0][2])
        prix=float(lrep[0][3])

        #update BD
        if comp==0:
            if argent_actuel>=prix:
                self.label_argent.configure(text="argent: "+str(round(argent_actuel-(prix),2)))
                self.cur.execute("UPDATE joueur SET argent=(?) WHERE argent=(?) and adresse='" + self.adresse + "'",(argent_actuel-prix,argent_actuel))
                self.cur.execute("UPDATE joueur SET vie=(?) WHERE vie=(?) and adresse='" + self.adresse + "'",(vie_actuel+1,vie_actuel))
                self.cur.execute("UPDATE joueur SET prix=(?) WHERE prix=(?) and adresse='" + self.adresse + "'",(prix*1.15,prix))
        else:
            if argent_actuel>=prix:
                self.label_argent.configure(text="argent: "+str(round(argent_actuel-(prix),2)))
                self.cur.execute("UPDATE joueur SET argent=(?) WHERE argent=(?) and adresse='" + self.adresse + "'",(argent_actuel-prix,argent_actuel))
                self.cur.execute("UPDATE joueur SET degat=(?) WHERE degat=(?) and adresse='" + self.adresse + "'",(degat_actuel+1,degat_actuel))
                self.cur.execute("UPDATE joueur SET prix=(?) WHERE prix=(?) and adresse='" + self.adresse + "'",(prix*1.15,prix))
        self.connex.commit()

        #mise a jour des label
        self.cur.execute("SELECT vie,degat,prix FROM joueur where adresse='"+self.adresse+"' ")
        lrep=self.cur.fetchall()
        vie_actuel=lrep[0][0]
        degat_actuel=lrep[0][1]
        prix_actuel=lrep[0][2]
        self.label_vie.configure(text="Niveau de vie: "+str(vie_actuel),font=("Courier", 30))
        self.label_degat.configure(text="Niveau de degat: "+str(degat_actuel),font=("Courier", 30))
        self.label_prix.configure(text="prix: "+str(round(prix_actuel,2)),font=("Courier", 30))


    def restart_menu(self,adresse):
        self.cur.execute("SELECT niveau_actuel,niveau_max FROM joueur WHERE adresse = '" + self.adresse + "'")
        lrep=self.cur.fetchall()
        self.niveau_max=lrep[0][1]
        self.niveau_actuel=lrep[0][0]
        self.label_niveau_actuel.configure(text="niveau actuel: "+str(self.niveau_actuel))
        self.label_niveau_max.configure(text="niveau max: "+str(self.niveau_max))




#fonction qui lance le menu depuis le menu de connexion
def main_menu(self,adresse):
    app=Menu(adresse)
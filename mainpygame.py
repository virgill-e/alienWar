import sqlite3
from tkinter import *
import tkinter as tk
from random import randint
import pygame
import sys
import time


def maindupygame(menu,largeur,hauteur,adresse,liskin,niveau):
    global running
    pygame.init()
    clock=pygame.time.Clock()
    FPS=60

    #base de donnée
    connex= sqlite3.connect("BigVir_bd.sq3")#création connexion
    cur=connex.cursor() #création curseur
    cur.execute("SELECT niveau_actuel FROM joueur WHERE adresse = '" + adresse + "'")
    lrep=cur.fetchall()

    """chargement des élément"""
    #generer la fenetre du jeu
    pygame.display.set_caption("jeu sorciere")

    screen_width = largeur 
    screen_height = hauteur
    
    screen=pygame.display.set_mode((screen_width,screen_height))#ouvrir la fenetre avec la bone taille de l'ecran

    #importer arriere plan du jeu
    background=pygame.image.load("img/foret_dessin.jpg")


    #charge le jeu
    jeuencours=True
    jeu=Jeu(menu,screen,jeuencours,screen_width,screen_height,adresse,liskin,niveau)
    print("prout")
    #apparition de l'ennemi
    if int(lrep[0][0])%10!=0:
        jeu.spawn_ennemi(20,5,adresse)
    else:
        jeu.spawn_boss()
    """ boucle de la fentre"""
    running = True
    #boucle tant que cette condition est vrai
    while running==True:
        #gérer le nombre d'image par seconde
        clock.tick(FPS)
        #apliquer arriere plan de notre jeu
        screen.blit(background,(0,(-100/screen_height)*1080))
        jeu.update()#vérification des évènement
 
#classe qui gère les monstres
class Ennemi(pygame.sprite.Sprite):

    def __init__(self,jeu,maxvie,degat,adresse):
        super().__init__()
        self.jeu=jeu
        self.maxvie=maxvie*1.05**self.jeu.niveau
        self.vie=self.maxvie
        self.degat=degat*(self.jeu.niveau)/4
        self.image=pygame.image.load("img/ennemi.png")
        self.taille_ennemi_ratio=int(256/1080*self.jeu.height)
        self.image=pygame.transform.scale(self.image,(self.taille_ennemi_ratio,self.taille_ennemi_ratio))
        self.rect=self.image.get_rect()
        self.rect.x=self.jeu.width
        self.rect.y=randint(self.taille_ennemi_ratio//2,self.jeu.height-self.taille_ennemi_ratio)
        self.vitesse=7
        self.sens="gauche"
        self.adresse=adresse
        
        #base de donnée
        self.connex= sqlite3.connect("BigVir_bd.sq3")#création connexion
        self.cur= self.connex.cursor() #création curseur

        self.cur.execute("SELECT niveau_actuel FROM joueur WHERE adresse = '" + self.adresse + "'")
        lrep=self.cur.fetchall()
        self.niv_start=int(lrep[0][0])
        

    def mouvement(self):
        if self.rect.x<=0 or self.jeu.collision(self,self.jeu.alljoueur) and self.sens=="gauche":
            self.sens="droite"
            self.rect.x+=50
        elif self.rect.x>=self.jeu.width-self.taille_ennemi_ratio or self.jeu.collision(self,self.jeu.alljoueur) and self.sens=="droite":
            self.sens="gauche"
            self.rect.x-=50
        if self.sens=="gauche":
            self.rect.x-=self.vitesse
        else:
            self.rect.x+=self.vitesse
        if self.jeu.collision(self,self.jeu.alljoueur):
            self.jeu.joueur.dommage(self.degat) #infliger des degat

    def barre_vie(self,surface):
        #définir la couleur/position/epaiseur/longueur de la bare de vie
        barre_couleur=(55, 231, 20)
        barre_position=[self.rect.x,self.rect.y-20,(self.vie/self.maxvie)*self.taille_ennemi_ratio,10]

        #afficher la barre de vie
        pygame.draw.rect(surface,barre_couleur, barre_position)

    def dommage(self,degat):
        self.vie-=degat
        if self.vie<=0:
            self.jeu.allennemi.remove(self)
            self.jeu.niveau+=1

            if self.jeu.niveau%10!=0:
                self.jeu.spawn_ennemi(20,5,self.adresse)
            else:
                self.jeu.spawn_boss()

class Boss(pygame.sprite.Sprite):
    def __init__(self,jeu):
        super().__init__()

        self.jeu=jeu
        self.maxvie=300*self.jeu.niveau/10
        self.vie=self.maxvie
        self.degat=20*self.jeu.niveau/10

        li_boss=['img/boss/snake.png','img/boss/ghost.png','img/boss/dragon.png','img/boss/zeus.png','img/boss/alien.png']
        if self.jeu.niveau<=50:
            self.image=pygame.image.load(li_boss[(self.jeu.niveau-1)//10])
        else:
            self.image=pygame.image.load(li_boss[4])

        self.taille_boss_ratio=int(512/1080*self.jeu.height)
        self.image=pygame.transform.scale(self.image,(self.taille_boss_ratio,self.taille_boss_ratio))
        self.rect=self.image.get_rect()
        self.rect.x=self.jeu.width-self.taille_boss_ratio
        self.rect.y=self.jeu.height-self.taille_boss_ratio+20

    def barre_vie(self,surface):
        #définir la couleur/position/epaiseur/longueur de la bare de vie
        barre_couleur=(133, 6, 6)
        barre_position=[self.jeu.width//2-(self.taille_boss_ratio//2),50,(self.vie/self.maxvie)*self.taille_boss_ratio,self.jeu.height/40]

        #afficher la barre de vie
        pygame.draw.rect(surface,barre_couleur, barre_position)
    
    def tir(self):
        self.jeu.allbossprojectile.add(BossProjectile(self))

    def dommage(self,degat):
        self.vie-=degat
        if self.vie<=0:
            self.jeu.allboss.remove(self)
            self.jeu.niveau+=1

            if self.jeu.niveau%10!=0:
                self.jeu.spawn_ennemi(20,5,self.jeu.adresse)
            else:
                self.jeu.spawn_boss()

class BossProjectile(pygame.sprite.Sprite):

    #définir le constructeur
    def __init__(self, boss):
        super().__init__()

        self.boss=boss
        self.vitesse=8
        self.vitesse_y=randint(-8,4)


        li_boss_shoot=['img/boss/shoot/snake.png','img/boss/shoot/ghost.png','img/boss/shoot/dragon.png','img/boss/shoot/zeus.png','img/boss/shoot/alien.png']
        if self.boss.jeu.niveau<=50:
            self.image=pygame.image.load(li_boss_shoot[(self.boss.jeu.niveau-1)//10])
        else:
            self.image=pygame.image.load(li_boss_shoot[4])


        self.taille_tir_boss_ratio=int(128/1080*self.boss.jeu.height)
        self.image=pygame.transform.scale(self.image,(self.taille_tir_boss_ratio,self.taille_tir_boss_ratio))

        self.rect=self.image.get_rect()
        self.rect.x = boss.rect.x-50
        self.rect.y = boss.rect.y+50
        self.degat=self.boss.degat

    def mouvement(self):
        self.rect.x-=self.vitesse
        self.rect.y+=self.vitesse_y
        if self.rect.x>self.boss.jeu.width or self.rect.x<0:
            self.supprimer()

        for bossprojectile in self.boss.jeu.collision(self,self.boss.jeu.alljoueur):
            self.boss.jeu.joueur.dommage(self.boss.degat) #infliger des degat
            self.supprimer()

    def supprimer(self):
        self.boss.jeu.allbossprojectile.remove(self)



#class qui représente le jeu
class Jeu():
    def __init__(self,menu,screen,jeuencours,width,height,adresse,liskin,niveau):

        self.width=width
        self.height=height
        self.alljoueur=pygame.sprite.Group()
        self.joueur=Joueur(self,liskin,adresse)#apelle de la classe joueur pour le créer
        self.alljoueur.add(self.joueur)
        self.pressed={}#dictionnaire des touches pressé grace a True/False
        self.allennemi=pygame.sprite.Group()
        self.allboss=pygame.sprite.Group()
        self.allbossprojectile=pygame.sprite.Group()
        self.menu=menu
        self.spawn_ennemi
        self.niveau=niveau
        self.screen=screen
        self.adresse=adresse
        self.jeuencours=jeuencours
        self.perdu=False

        self.connex= sqlite3.connect("BigVir_bd.sq3")#création connexion
        self.cur= self.connex.cursor() #création curseur


    def update(self):
        global running
        if self.jeuencours==True or self.perdu==True:
            if self.jeuencours==True:
                #aficher score
                font=pygame.font.SysFont("monospace",30,)
                txtscore = font.render('score: '+str(self.niveau),10,(255,0,0))
                self.screen.blit(txtscore,(0,0))

                #appliquer joueur
                self.screen.blit(self.joueur.image,(self.joueur.rect))


                #actualiser barre de vie de joueur
                self.joueur.barre_vie(self.screen)

                #déplacement projectile et monstre
                for projectile in self.joueur.allprojectile:
                    projectile.mouvement()

                for ennemi in self.allennemi:
                    ennemi.mouvement()
                    ennemi.barre_vie(self.screen)

                for bossprojectile in self.allbossprojectile:
                    bossprojectile.mouvement()

                for boss in self.allboss:
                    boss.barre_vie(self.screen)
                
                #faire tirer le boss
                for boss in self.allboss:
                    nb1=randint(1,100)
                    nb2=randint(1,100)
                    if nb1==nb2:
                        boss.tir()
                        boss.tir()
                        boss.tir()

                #dessiner d'image des projectile/ennemi
                self.joueur.allprojectile.draw(self.screen)
                self.allennemi.draw(self.screen)
                self.allboss.draw(self.screen)
                self.allbossprojectile.draw(self.screen)

                #Créer des actions sur les touche pressé
                if self.pressed.get(pygame.K_RIGHT)and self.joueur.rect.x+self.joueur.rect.width < self.screen.get_width():#limite coté
                    self.joueur.move_right()

                elif self.pressed.get(pygame.K_LEFT) and self.joueur.rect.x>0:#limite coté
                    self.joueur.move_left()

                elif self.pressed.get(pygame.K_UP) and self.joueur.rect.y>50:#limite hauteur
                    self.joueur.move_up()

                elif self.pressed.get(pygame.K_DOWN) and self.joueur.rect.y<self.height-250:#limite hauteur
                    self.joueur.move_down()


            #mettre a jour écran
            elif self.perdu==True:
                #charger le png du game over
                banner=pygame.image.load("img/image_fin.png")
                self.taille_banner_ratio=int(512/1080*self.height)
                banner=pygame.transform.scale(banner,(self.taille_banner_ratio,self.taille_banner_ratio))

                self.screen.blit(banner,((self.width//2)-self.taille_banner_ratio//2,(self.height//2)-self.taille_banner_ratio//2))

                if self.pressed.get(pygame.K_SPACE):
                    running= False
                    pygame.quit()
                    self.menu.restart_menu(self.adresse)


            pygame.display.flip()


            for event in pygame.event.get():
                #que l'évenement est fermeture de fenetre
                if event.type ==pygame.QUIT:
                    running= False
                    pygame.quit()
                    

                #détecter si joueur pousse une touche
                
                elif event.type==pygame.KEYDOWN:
                    self.pressed[event.key]=True
                    print(event.type)
                    #detecter si espace appuyer (ici pour éviter de tirer beaucoup en restant appuyer)
                    if event.key==pygame.K_SPACE:
                        self.joueur.launch()
                        if self.perdu==True:
                            running= False
                            pygame.quit()
                            self.menu.restart_menu(self.adresse)

                elif event.type==pygame.KEYUP:
                    self.pressed[event.key]=False
                    print(event.type)
                    
    def game_over(self):
            self.perdu=True
            self.jeuencours=False
            #mise a jour du niveau max et actuel
            self.cur.execute("SELECT niveau_max,niveau_actuel FROM joueur WHERE adresse = '" + self.adresse + "'")
            lrep=self.cur.fetchall()
            niveauMax=int(lrep[0][0])
            if int(self.niveau)>int(niveauMax):
                self.cur.execute("UPDATE joueur SET niveau_max=(?) WHERE niveau_max=(?) and adresse=(?)",(self.niveau,niveauMax,self.adresse))
                self.connex.commit()  
            niveauActuel=lrep[0][1]
            self.cur.execute("UPDATE joueur SET niveau_actuel=(?) WHERE niveau_actuel=(?) and adresse='" + self.adresse + "'",(self.niveau,niveauActuel))
            self.connex.commit()


    def spawn_ennemi(self,viemax,degat,adresse):
            self.cur.execute("SELECT argent FROM joueur where adresse='"+self.adresse+"' ")
            lrep=self.cur.fetchall()
            argent=lrep[0][0]
            self.cur.execute("UPDATE joueur SET argent=(?) WHERE argent=(?) and adresse='" + self.adresse + "'",(argent+1,argent))
            self.connex.commit()

            self.allennemi.add(Ennemi(self,viemax,degat,self.adresse))

    def spawn_boss(self):
            self.cur.execute("SELECT argent FROM joueur where adresse='"+self.adresse+"' ")
            lrep=self.cur.fetchall()
            argent=lrep[0][0]
            self.cur.execute("UPDATE joueur SET argent=(?) WHERE argent=(?) and adresse='" + self.adresse + "'",(argent+10,argent))
            self.connex.commit()

            self.allboss.add(Boss(self))

    def collision(self,sprite,group):
        return pygame.sprite.spritecollide(sprite,group,False,pygame.sprite.collide_mask)


#creeer classe de la sorcière
class Joueur(pygame.sprite.Sprite):
    """class joueur"""
    def __init__(self,jeu,liskin,adresse):
        super().__init__()

        self.adresse=adresse

        self.connex= sqlite3.connect("BigVir_bd.sq3")#création connexion
        self.cur= self.connex.cursor() #création curseur
        self.cur.execute("SELECT vie,degat FROM joueur where adresse='"+self.adresse+"' ")
        lrep=self.cur.fetchall()

        self.jeu=jeu
        self.vitesse=6
        self.liskin=liskin
        self.taille_joueur_ratio=int(256/1080*self.jeu.height)
        self.image=pygame.image.load(self.liskin[0])
        self.image=pygame.transform.scale(self.image,(self.taille_joueur_ratio,self.taille_joueur_ratio))

        self.rect=self.image.get_rect()
        self.rect.x=50
        self.rect.y=self.jeu.height//2
        self.allprojectile=pygame.sprite.Group()
        self.sens="droite"
        self.degat=3*(1.1**lrep[0][1])
        self.maxvie=10*(1.1**lrep[0][0])
        self.vie=self.maxvie

    def move_right(self):
        self.image=pygame.image.load(self.liskin[0])
        self.image=pygame.transform.scale(self.image,(self.taille_joueur_ratio,self.taille_joueur_ratio))
        self.sens="droite"
        if not self.jeu.collision(self,self.jeu.allennemi):
            self.rect.x += self.vitesse
    def move_left(self):
        self.image=pygame.image.load(self.liskin[1])
        self.image=pygame.transform.scale(self.image,(self.taille_joueur_ratio,self.taille_joueur_ratio))
        self.sens="gauche"
        if not self.jeu.collision(self,self.jeu.allennemi):
            self.rect.x-=self.vitesse

    def move_up(self):
        if not self.jeu.collision(self,self.jeu.allennemi):
            self.rect.y-=self.vitesse+4
        else:
            self.rect.y+=50

    def move_down(self):
        if not self.jeu.collision(self,self.jeu.allennemi):
            self.rect.y+=self.vitesse+4
        else:
            self.rect.y-=50

    def launch(self):
        #créer une nouvelle instance
        self.allprojectile.add(Projectile(self))

    def barre_vie(self,surface):
        #définir la couleur/position/epaiseur/longueur de la bare de vie
        barre_couleur=(55, 231, 20)
        barre_position=[self.rect.x,self.rect.y-20,(self.vie/self.maxvie)*256,15]

        #afficher la barre de vie
        pygame.draw.rect(surface,barre_couleur, barre_position)

    def dommage(self,degat):
        self.vie-=degat
        if self.vie<=0:
            self.jeu.game_over()


class Projectile(pygame.sprite.Sprite):

    #définir le constructeur
    def __init__(self, joueur):
        super().__init__()
        self.joueur=joueur
        self.vitesse=25
        self.image=pygame.image.load("img/fire.png")
        self.taille_tir_joueur_ratio=int(256/1080*self.joueur.jeu.height)
        self.image=pygame.transform.scale(self.image,(self.taille_tir_joueur_ratio,self.taille_tir_joueur_ratio))

        self.rect=self.image.get_rect()
        self.rect.x = joueur.rect.x+100
        self.rect.y = joueur.rect.y+75
        self.sens=joueur.sens
        self.degat=self.joueur.degat

    def mouvement(self):
        if self.sens=="droite":
            self.image=pygame.image.load("img/fire.png")
            self.rect.x+=self.vitesse
        else:
            self.image=pygame.image.load("img/fire_inverse.png")
            self.rect.x-=self.vitesse
        if self.rect.x>self.joueur.jeu.width or self.rect.x<0:
            self.supprimer()

        for ennemi in self.joueur.jeu.collision(self,self.joueur.jeu.allennemi):
            ennemi.dommage(self.degat) #infliger des degat
            self.supprimer()

        for boss in self.joueur.jeu.collision(self,self.joueur.jeu.allboss):
            boss.dommage(self.degat) #infliger des degat
            self.supprimer()

    def supprimer(self):
        self.joueur.allprojectile.remove(self)

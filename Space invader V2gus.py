import random
import pyxel


class App:
    def __init__(self):
        """
            Initialisation de la fenêtre et des éléments
        """
        # Fenêtre de 120 par 200 pyxels
        pyxel.init(120, 200, title="Space Invader",fps=30,quit_key=pyxel.KEY_P)
        # Vaisseau en (60,180)
        self.ship = Ship(60,180)
        #Banque d'image
        pyxel.load("impact.pyxres")
        # Toute les variables utilile au bon fonctionnement du code
        self.ennemi = []
        self.missile=[]
        self.missile_ennemi=[]
        self.score = 0
        self.vitesse = 0
        self.compteur = 0
        self.gameover = False
        self.sens = True
        self.position=10
        #Définit le fond du jeu
        self.background=Background()
        # On lance le moteur du jeu
        pyxel.run(self.update, self.draw)

    def update(self):
        """
            Mise à jour des positions et des états
        """
        # Déplacement à droite
        if pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT):
            self.ship.move(1,0)
        # Déplacement à gauche
        if pyxel.btn(pyxel.KEY_Q) or  pyxel.btn(pyxel.KEY_LEFT):
            self.ship.move(-1,0)
        #Lancé des missiles
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.missile.append(Missile(self.ship.x,self.ship.y-4))
        #Change de skin du vaiseau 
        if pyxel.btnp(pyxel.KEY_T):
            self.ship.skin = 1
        if pyxel.btnp(pyxel.KEY_Y):
            self.ship.skin = 0
        

        #Vérifie si il ya des enneemi
        if self.score == 0:  
            if len(self.ennemi) <= 11:
                self.ennemi.append(Ennemis(self.position,10))
                self.ennemi.append(Ennemis(self.position,25))
                self.position +=20
            
        if self.score != 0 and self.score % 12 == 0:
            self.position = 0
            for i in range(12):
                if len(self.ennemi) <= 11:
                    self.ennemi.append(Ennemis(self.position+5,10))
                    self.ennemi.append(Ennemis(self.position+5,25))
                    self.position +=20
            self.position = 0
        
        #gère la hitbox des ennemie
        for missile in self.missile:
            missile.y -= 5
            for ennemis in self.ennemi:
                if missile.x >= (ennemis.x - ennemis.taille//2) and missile.x <= (ennemis.x + ennemis.taille//2) and missile.y >= (ennemis.y - ennemis.taille//2) and missile.y <= (ennemis.y + ennemis.taille//2) :
                    self.missile.remove(missile)
                    ennemis.etat = 1
                    self.score += 1


        for missile_ennemi in self.missile_ennemi:
            if missile_ennemi.x >= (self.ship.x - self.ship.taille//4) and missile_ennemi.x <= (self.ship.x + self.ship.taille//4) and missile_ennemi.y >= (self.ship.y - self.ship.taille//4) and missile_ennemi.y <= (self.ship.y + self.ship.taille//4) :
                self.missile_ennemi.remove(missile_ennemi)
                self.ship.etat_verif()
                self.gameover=True
                
        
        #à changé !
        for ennemis in self.ennemi:
            if ennemis.y == 170:
                self.ennemi.remove(ennemis)
            if ennemis.y == 171:
                self.ennemi.remove(ennemis)
            if self.ennemi == []:
                self.gameover=True
        
        if self.ship.etat>=1:
            self.ship.etat_verif()

        #Vérifie les etats
        for ennemis in self.ennemi:
            if ennemis.etat == 1:
                ennemis.etat = 2
            elif ennemis.etat == 2:
                ennemis.etat = 3
                self.ennemi.remove(ennemis)
                    
        #Fait bougé les ennemis
        if self.sens == True:
            if self.compteur != 5:
                self.compteur += 1
                for Ennemi in self.ennemi:
                    Ennemi.x += 1
            else:
                self.compteur = 0
                self.sens = not self.sens
        else:
            if self.compteur != 5:
                self.compteur += 1
                for Ennemi in self.ennemi:
                    Ennemi.x -= 1
            else:
                self.compteur = 0
                self.sens = not self.sens
                

        #Lancé les missiles par les ennemis
        for ennemi in self.ennemi:
                if ennemis.etat == 0:
                    b=random.randint(0,len(self.ennemi)*(12-self.vitesse*2))
                    if b == 0:
                        self.missile_ennemi.append(Missile_ennemi(ennemi.x,ennemi.y))
                    ennemi.y += self.vitesse
        if self.score != 0 and self.score % 12 == 0:
            if len(self.ennemi) <= 11:
                self.vitesse += 0.5
                    

        for missile_ennemi in self.missile_ennemi:
            if missile_ennemi.y == 195:
                self.missile_ennemi.remove(missile_ennemi)
            missile_ennemi.y +=2
        


        #Définit le fond du jeu
        self.background.update()
                    
                
    def draw(self):
        """
            On affiche les éléments
        """
        
        # On rempli le fond avec une couleur
        pyxel.cls(0)
        if self.gameover == True:
            self.ship = Ship(600,180)
            self.ennemi = []
            self.missile=[]
            self.missile_ennemi=[]
            self.draw_score()
            pyxel.text(45,110,"GAMEOVER ",7)
            
        # On affiche le vaisseau
        self.ship.draw()
        #On affiche les ennemis
        for i in range(len(self.ennemi)):
            self.ennemi[i].draw_ennemi()
        #On affiche les missiles et on les supprime si il arrive en haut avec une animations 
        for missile in self.missile:
            missile.draw_missile()
            if missile.y == 4:
                missile.limit()
                self.missile.remove(missile)
        #On affiche les missiles ennemis
        for Missile_ennemi in self.missile_ennemi:
            Missile_ennemi.draw_missile()

        #On affiche le score
        self.draw_score()
        #Définit le fond du jeu
        self.background.draw()

    
    def draw_score(self):
        #La fonction permet de générer le score en format pyxel
        score = f"{self.score:04}"
        pyxel.text(1, 190, score, 7)
    
class Ship:
    """
        Vaisseau principal
    """
    def __init__(self, x, y):
        """
            Caractéristiques du vaisseau.
            C'est un carré dans un premier temps.
        """
        self.x = x
        self.y = y
        self.taille = 8
        self.etat = 0
        self.skin = 0

    def draw(self):
        """
            Affichage du vaisseau
        """
        if self.skin == 1:
            pyxel.blt(self.x-7, self.y-2, 0, 32, 0, 16, 16)
        if self.skin == 0:
            if self.etat == 0:
                pyxel.rect(self.x,self.y+7,1,1,7)
                pyxel.rect(self.x-1,self.y,3,7,7)
                pyxel.rect(self.x,self.y-1,1,1,7)
                pyxel.rect(self.x-2,self.y+3,1,2,7)
                pyxel.rect(self.x-4,self.y+3,2,3,7)
                pyxel.rect(self.x+2,self.y+3,1,2,7)
                pyxel.rect(self.x+3,self.y+3,2,3,7)
                pyxel.rect(self.x-3,self.y+2,1,1,7)
                pyxel.rect(self.x+3,self.y+2,1,1,7)
                pyxel.rect(self.x,self.y+1,1,2,0)
        elif self.etat == 1:
            pyxel.blt(self.x-3, self.y-3, 0, 16, 16, 16, 16)
        elif self.etat == 2:
            pyxel.blt(self.x-3, self.y-3, 0, 16, 16, 16, 16)
        elif self.etat == 2:
            pyxel.blt(self.x-3, self.y-3, 0, 16, 32, 16, 16)
        elif self.etat == 3:
            pyxel.blt(self.x-3, self.y-3, 0, 16, 32, 16, 16)
        elif self.etat == 4:
            pyxel.blt(self.x-3, self.y-3, 0, 32, 32, 16, 16)
        elif self.etat == 5:
            pyxel.blt(self.x-3, self.y-3, 0, 32, 32, 16, 16)
        elif self.etat == 6:
            pyxel.blt(self.x-3, self.y-3, 0, 48, 32, 16, 16)
        elif self.etat == 7:
            pyxel.blt(self.x-3, self.y-3, 0, 48, 32, 16, 16)
        elif self.etat == 8:
            pyxel.blt(self.x-3, self.y-3, 0, 32, 16, 16, 16)
        elif self.etat == 9:
            pyxel.blt(self.x-3, self.y-3, 0, 32, 16, 16, 16)
        elif self.etat == 10:
            pyxel.blt(self.x-3, self.y-3, 0, 48, 16, 16, 16)
        elif self.etat == 11:
            pyxel.blt(self.x-3, self.y-3, 0, 48, 16, 16, 16)

    def move(self, dx, dy):
        """
            Déplacement du vaisseau
        """
        self.x += dx
        self.y += dy
        if self.x == 116:
            self.x = 115
        if self.x == 3:
            self.x = 4

    def etat_verif(self):
        if self.etat ==0:
            self.etat +=1
        elif self.etat==1:
            self.etat+=1
        elif self.etat==2:
            self.etat+=1
        elif self.etat==3:
            self.etat+=1
        elif self.etat==4:
            self.etat+=1
        elif self.etat==5:
            self.etat+=1
        elif self.etat==6:
            self.etat+=1
        elif self.etat==7:
            self.etat+=1
        elif self.etat==8:
            self.etat+=1
        elif self.etat==9:
            self.etat+=1
        elif self.etat==10:
            self.etat+=1
        elif self.etat==11:
            self.etat+=1

class Ennemis:
    def __init__(self, x, y):
        """
            Caractéristiques du vaisseau.
            C'est un carré dans un premier temps.
        """
        self.x = x
        self.y = y
        self.taille = 10
        self.etat = 0

    def draw_ennemi(self):
        """
            Affichage de l'ennemis
        """
        if self.etat == 0:
            pyxel.rect(self.x-4,self.y,8,4,8)
            pyxel.rect(self.x-4,self.y+4,1,1,8)
            pyxel.rect(self.x-3,self.y+5,2,1,8)
            pyxel.rect(self.x+3,self.y+4,1,1,8)
            pyxel.rect(self.x+1,self.y+5,2,1,8)
            pyxel.rect(self.x+5,self.y+2,1,3,8)
            pyxel.rect(self.x-6,self.y+2,1,3,8)
            pyxel.rect(self.x+4,self.y+1,1,2,8)
            pyxel.rect(self.x-5,self.y+1,1,2,8)
            pyxel.rect(self.x-4,self.y-2,1,1,8)
            pyxel.rect(self.x-3,self.y-1,1,1,8)
            pyxel.rect(self.x+3,self.y-2,1,1,8)
            pyxel.rect(self.x+2,self.y-1,1,1,8)
            pyxel.rect(self.x-3,self.y+1,1,1,0)
            pyxel.rect(self.x+2,self.y+1,1,1,0)
        elif self.etat == 1:
            pyxel.blt(self.x-6, self.y-5, 0, 0, 0, 16, 16)
        elif self.etat == 2:
            pyxel.blt(self.x-6, self.y-5, 1, 0, 0, 16, 16)
        elif self.etat == 3:
            pyxel.blt(self.x-6, self.y-5, 2, 0, 0, 16, 16)
            
    
    
    
    
class Missile:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.taille = 1
        
    def draw_missile(self):
        """
            Affichage le missile
        """
        pyxel.rect(self.x,self.y,1,2,7)
        
    def limit(self):
        pyxel.blt(self.x-7, self.y, 0, 16, 8, 8, 8)
     
     
     
     
     
class Missile_ennemi:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.taille = 1
        
    def draw_missile(self):
        """
            Affichage le missile
        """
        pyxel.rect(self.x,self.y,1,2,11)
            
            
class Background:
    def __init__(self):
        self.stars = []
        for i in range(200):
            self.stars.append(
                (
                    pyxel.rndi(0, pyxel.width - 1),
                    pyxel.rndi(0, pyxel.height - 1),
                    pyxel.rndf(1, 2),
                )
            )
 
    def update(self):
        for i, (x, y, speed) in enumerate(self.stars):
            x += speed
            if x >= pyxel.height:
                x -= pyxel.height
            self.stars[i] = (x, y, speed)

 
    def draw(self):
        for (x, y, speed) in self.stars:
            pyxel.pset(x, y, 12 if speed > 1.8 else 5)

App()
 
# -*- coding: utf-8 -*-

""""
Voici le code du TP sur Space Invaders.


# TODO -----------------
# TODO  -Faire une seule classe 'SHIP' et en faire hériter la classe Player et Ennemy
# TODO  -Supprimer réellement chaque objet une fois qu'il n'est plus affiché
# TODO  -Faire différentes sous-classes de la classe Ennemy, comme des tanks (donc avec un attribut hp en plus),
        éclaireur (avec une vélocité plus elevée) etc
# TODO  -Faire une fenêtre de binding, pour permettre de modifier les touches.
# TODO  -Faire un cooldown de tir, par exemple de 2 secondes, pour accroître la difficuté
# TODO  -Faire un îlot de proctection ( ou plusieurs )
# TODO  -Se charger des erreurs créees par la méthode After de tkinter
# TODO  -Ajouter du son (mon module playsound ne fonctionne pas)
# TODO  -Régler le bug de l'historique
# TODO ------------------
#
Papa Birahim Seye, 3 ETI, CPE Lyon
Date: 14/01/2020
"""

from random import randint, uniform, choice
from tkinter import *
from tkinter.messagebox import showinfo
import pygame

pygame.mixer.init()  # Initialisation du mixeur qui gère le son

velocity = 5
wwidth = 1000  # Largeur de la fenêtre
wheight = 800  # Hauteur de la fenêtre
bonusList = []  # Liste des bonus crées


class Ennemy:

    def __init__(self, xcor=500, ycor=200):
        color = choice(["shiny", "simple", "shooter"])  # Choisis une couleur aleatoire pour les ennemis
        """" Ici on initialise le chaque objet de la classe des ennemis, chacun d'eux aura dans l'ordre de définition
        son image (pour le moment la même pour tous), sa coordonnée en X, en Y, sa vélocité, un sens de direction,
        une valeur ( qui s'ajoute aux points du joueur lorsqu'il touche sa cible), une liste de lasers, une variable
        booléenne qui détermine si l'objet est affiché à l'écran ou pas et sa représentation sur ce-dit écran.
        Lors de l'initialisationm les deux fonctions shoot et move sont lancées directement.
        """
        self.image = PhotoImage(file=f'Images/ennemy_{color}64.png')
        self.xcor = xcor
        self.ycor = ycor
        self.velocity = 5
        self.direction = -1
        self.value = 100
        self.lasers = []
        self.onscreen = True
        self.rep = place.create_image(xcor, ycor, image=self.image)

        self.move()
        self.shoot()

    def move(self):
        """
        C'est la fonction qui gère le déplacement automatique de chaque ennemi individuellement.
        Arrivé au bord de la fenêtre l'ennemi descend de 50 pixel et sa direction est invérsée.
        """
        self.xcor += self.velocity
        if self.xcor < 100 or self.xcor > 900:
            self.ycor += 50
            self.velocity *= self.direction

        place.coords(self.rep, self.xcor, self.ycor)
        mainwindow.after(30, self.move)

    def shoot(self):
        """
        Cette fonction fait tirer les ennemis de manière aléatoire.
        """
        nextTryIn = randint(300, 1000)
        chance = uniform(0, 1)

        if chance > 0.9:
            laser = Laser(xcor=self.xcor, ycor=self.ycor - 10, direction=-1)
            self.lasers += [laser]

        if self.onscreen:
            mainwindow.after(nextTryIn, self.shoot)

    def pop(self, element):
        """
        Permet de supprimer un élément, ici ca sera un des lasers tirés par l'ennemi.
        :param element:
        :return:
        """
        place.delete(element.rep)
        self.lasers = [laser for laser in self.lasers if laser != element]


class Horde:

    def __init__(self, number):
        """
        La classe Horde, qui sera un ensemble d'ennemis, son itialisation se fait avec le paramètre number, qui
        correspond au nombre d'ennemis à afficher.
        Les attributs de base sont soldiers (Une liste de tous les ennemis crées par la classe horde, un X initial, un
        Y initial, un space, qui correspond à l'espace entre deux ennemis, un paramètre line, qui pertmet de créer
        plusieurs lignes en fonction du nombre d'ennemis et la direction, qui sera donnée à chaque ennemis en fonction
        de la ligne sur laquelle il se trouve.
        :param number:
        """
        self.soldiers = []
        self.number = number
        self.xinit = 100
        self.yinit = 100
        self.space = 80
        self.speed = 20
        self.line = 1
        self.direction = -1

    def invade(self):
        """
        Permet "d'envahir" le terrain en créeant les différentes lignes des ennemis en fonction du xinit et du yinit.
        Ajoute chaque ennemi à la liste self.soldiers
        :return:
        """
        direction = -1
        for number in range(self.number):
            soldier = Ennemy(xcor=self.xinit, ycor=self.yinit)
            soldier.direction = direction
            self.soldiers += [soldier]

            self.xinit += self.space * self.line

            if not 0 < self.xinit + 100 < wwidth:
                self.line *= -1
                self.yinit += 50
                direction *= -1

    def pop(self, element):
        """
        Comme avec la classe Ennemy, cette fonction supprime un élément de la liste des ennemis et lui change son
        paramètre 'onscreen' pour qu'il ne soit plus affiché à l'écran.
        :param element:
        :return:
        """
        place.delete(element.rep)
        self.soldiers = [alien for alien in self.soldiers if alien != element]
        element.onscreen = False

    def setspeed(self, speed):
        """
        Cette fonction permet de donner une certaine vitesse aux ennemis.
        :param speed:
        :return:
        """
        for soldier in self.soldiers:
            soldier.velocity = speed * soldier.direction

    def reset(self):
        """
        Remet les paramètres initiaux nécessaires pour relancer une partie.
        :return:
        """
        for element in self.soldiers:
            self.pop(element)

        self.xinit = 100
        self.yinit = 100
        self.line = 1


class Player:

    def __init__(self, xcor, ycor, lives=3):
        """
        Définition de la classe du joueur. Caractérisé par une image, une coordonnée en X, une autre en Y, un nombre de
        vies, une liste de lasers, une direction, un score une représentation sur le canvas et une vitesse.
        :param xcor: Coordonnée en X
        :param ycor: Coordonnée en Y
        :param lives: Nombre de vies, par défaut 3
        """
        self.image = PhotoImage(file='Images/player64.png')
        self.xcor = xcor
        self.ycor = ycor
        self.lives = lives
        self.lasers = []
        self.direction = 1
        self.score = 0
        self.player = place.create_image(xcor, ycor, image=self.image)
        self.speed = 1  # a supprimer apres

    def action(self, event):
        """
        Cette fonction gère tous les inputs donnés par le joueur et les associe à différentes actions.
        La fonction "Shoot" n'a pas été faite séparement car il était compliqué d'asocier deux fonctions à un seul
        canvas.
        :param event: Gestionnaire d'événements
        :return:
        """
        key = event.keysym  # La touche sur laquelle on appuie

        # déplacement vers la droite

        if key == 'd':
            self.xcor += 20
            if self.xcor > wwidth:  # Limitation pour rester sur l'écran
                self.xcor = wwidth

        # déplacement vers la gauche

        if key == 'a':
            self.xcor -= 20
            if self.xcor < 0:  # Limitation pour rester sur l'écran
                self.xcor = 0

        # on déplace l'image à sa nouvelle position

        place.coords(self.player, self.xcor, self.ycor)

        if key == 'space':  # La fonction shoot. Permet au joueur de tirer.
            laser = Laser(xcor=self.xcor, ycor=self.ycor - 10)
            self.lasers += [laser]
            self.speed += 1  # Direction des ennemis quand la vitesse augmente.

        if key == 'c':  # Touche Bonus qui fait offiche de 'code de triche'
            createBonus()

        if key == 'p':  # Touche Bonus qui fait offiche de 'code de triche'
            player.score += 100

    def pop(self, element):
        """
        Supprimes un laser de la liste de lasers.
        :param element: Correspond au laser
        :return:
        """
        place.delete(element.rep)
        self.lasers = [laser for laser in self.lasers if laser != element]


class Laser:

    def __init__(self, xcor, ycor, direction=1):
        """
        Un laser est un objet commun aux ennemis et au joueur. De ce fait il est initialisé avec une variable direction
        ( -1 ou 1) qui sera multipliée à sa vitesse pour savoir si elle descends ou elle monte.
        Ses attributs sont dans l'ordre son image, sa velocité, sa coordonnée en X, celle en Y sa direction, un booléen
        pour savoir s'il est détruit ou pas et sa représentation.
        Les fonctions move et autodestroy sont appelées à chaque création d'un objet Laser.
        :param xcor: Variable qui dépends de la coordonnée de l'objet qui tire
        :param ycor: Variable qui dépends de la coordonnée de l'objet qui tire
        :param direction: Sens de déplacement, vers le haut ou vers le bas
        """
        self.image = PhotoImage(file='Images/laser_red64.png')
        self.velocity = 4
        self.xcor = xcor
        self.ycor = ycor
        self.direction = direction
        self.destroyed = False
        self.rep = place.create_image(self.xcor, self.ycor + 10, image=self.image)

        self.move()
        self.autodestroy()
        sound("lazer")

    def move(self):
        """
        Fonction qui permet au laser de se déplacer indéfiniment vers le haut ou vers le bas.
        :return:
        """
        if not self.destroyed:
            self.ycor -= 5 * self.direction
            place.coords(self.rep, self.xcor, self.ycor)

        else:  # Permet de ne pas rappeler la méthode after si le laser est détruit, économise des ressources.
            return None

        mainwindow.after(10, self.move)

    def autodestroy(self):
        """
        Vérifie si les coordonnées du laser ne sont pas trop grandes, si oui, cette fonction détruit sa représentation
        graphique.
        :return:
        """
        if not self.destroyed and (self.ycor < -50 or self.ycor > 850):
            place.delete(self)
            self.destroyed = True

        if self.destroyed:
            return None  # Cette ligne n'est là que pour éviter de d'utiliser after si la condition est vérifiée
        mainwindow.after(2000, self.autodestroy)


class Bonus:

    def __init__(self, xcor, ycor):
        """
        C'est un ennemi 'Bonus', pour les ennemis comme pour le joueur, il faut être le premier à tirer dessus.
        Il est caractérisé par sa coordonnée en X, celle en Y, une valeur plus élevée que celle des ennemis, une image
        et sa représentation sur le canvas.
        La fonction move est appelée lors de l'instanciation de l'objet.
        :param xcor: Coordonnée en X
        :param ycor: Coordonnée en Y
        """
        self.xcor = xcor
        self.ycor = ycor
        self.value = 300
        self.image = PhotoImage(file="Images/Star64.png")
        self.rep = place.create_image(self.xcor, self.ycor, image=self.image)

        self.move()

    def move(self):
        """
        Permet de déplaceer le Bonus sur l'axe des X à une certaine vitesse.
        :return:
        """
        self.xcor += 1
        place.coords(self.rep, self.xcor, self.ycor)
        mainwindow.after(4, self.move)

    def pop(self):
        """
        Supprime le Bonus de la liste des bonus et l'efface du canvas.
        :return:
        """
        global bonusList

        place.delete(self.rep)
        bonusList = [bonus for bonus in bonusList if bonus != self]


class UI:

    def __init__(self):
        """
        A la base je voulais mettre toute l'interface graphique ici, dont le HUD et les bouttons, mais je me suis rendu
        compte que ca serait bien plus complexe que de les separer.
        Donc cette classe UI permet juste d'afficher le score et le nombre de vie.
        Elle se met a jour automatiquement avec la méthode update.
        """
        self.score = 0
        self.lives = 3
        self.scoreboard = place.create_text(100, 30, fill="white", font=("8-bit_HUD", 20),
                                            text="Score : 0")
        self.livesui = place.create_text(900, 30, fill="white", font=("8-bit_HUD", 20),
                                         text="Lives : 3")

        self.update()

    def update(self):
        """
        Chaque 50 ms les éléments du HUD sont mis à jour.
        :return:
        """
        place.itemconfig(self.scoreboard, text=f"Score : {player.score}")
        place.itemconfig(self.livesui, text=f"Lives : {player.lives}")

        mainwindow.after(50, self.update)


def checkCollision(element1, element2):
    """
    Fonction basique qui gère la gestion des collisions.
    :param element1: Objet 1
    :param element2: Objet 2
    :return: True / False
    """
    if abs(element1.xcor - element2.xcor) < 30 and abs(element1.ycor - element2.ycor) < 15:
        return True
    else:
        return False


def checkLoop():
    """
    Dans cette fonction on utilise la fonction crée auparavant pour vérifier si une collision à été faite entre les
    objets affichés dans le canvas.
    :return:
    """
    global bonusList, velocity

    for laser in player.lasers:  # Check des lasers tirés par le joueur, cible : Bonus ou Ennemis

        for bonus in bonusList:
            if checkCollision(laser, bonus):
                bonus.pop()
                player.pop(laser)
                # sound("bonus")
                player.score += bonus.value  # Si la collision est confirmée, le score du joueur augmente.

        for alien in ennemies.soldiers:
            if checkCollision(laser, alien):
                ennemies.pop(alien)
                player.pop(laser)
                # sound("explosion")
                player.score += alien.value  # Si la collision est confirmée, le score du joueur augmente.
                checkWin()  # On vérifie qu'il ne reste plus d'ennemis
                #  ennemies.setspeed(velocity) Ici on devrait augmenter la vitesse à chaque fois qu'un ennemi tombe au
                #  velocity += 1 combat mais cela crée un bug, les ennemis chanqent direction en plus.

    for soldier in ennemies.soldiers:  # Pour chaque ennemi on va vérififer la collision de ses lasers.

        for laser in soldier.lasers:

            for bonus in bonusList:
                if checkCollision(laser, bonus):
                    bonus.pop()
                    soldier.pop(laser)
                    player.score -= bonus.value  # Attention, si l'ennemi touche le bonus , vous perdrez 300 points

            if checkCollision(laser, player):  # Si un laser ennemi touche le joueur, il perd un point de vie
                player.lives -= 1
                soldier.pop(laser)
                if player.lives == 0:
                    endGame()
                    showinfo(title="Lost", message="Humanity has been destroy !")  # Message affiché en cas de defaite

    mainwindow.after(50, checkLoop)


def sound(soundname):
    """
    Dans cette fonction on devrait pouvoir jouer un son, elle serait appelée à chaque fois que nécessaire comme par
    exemple lors d'un tir (en jouant le fichier sounds/lazer.mp3. Malheuresement le module ne fonctionne pas.
    Edit: J'ai réussi à faire marcher playsound.
    Edit2: Le module playground met en pause la mainloop de la fenêtre,du coup à chaque fois qu'on joue un son, le jeu
            se met en pause. J'ai donc utilisé la bibliothèque Pygame, et ca marche correctement.
    Edit3: Il n'y a que le son du laser qui est joué, les autres ne sont pas chargés par le mixer. Je les ai mis en
            commentaire.
    :param soundname: Nom du fichier
    :return:
    """

    # playsound(f"sounds/{soundname}.mp3")
    pygame.mixer.music.load(f"sounds/{soundname}.mp3")
    pygame.mixer.music.play()


def createBonus():
    """
    Cette fonction crée un Bonus à condition que les ennemis ne soient pas descendus à une certaine hauteur.
    :return:
    """
    global bonusList

    ymax = 0
    for ennemy in ennemies.soldiers:
        ymax = ennemy.ycor if ymax < ennemy.ycor else ymax

    if ymax <= 400:
        bonus = Bonus(xcor=-100, ycor=ymax + 200)
        bonusList += [bonus]


def bonusMaker():
    """
    Fonction qui est appelée au hasard dans une periode de temps et qui peut, si la chance est assez grande, crée un
    Bonus qui traversera le champ de bataille.
    :return:
    """
    nextTryIn = randint(300, 1000)
    chance = uniform(0, 1)

    if chance > 0.99:
        createBonus()

    mainwindow.after(nextTryIn, bonusMaker)


def checkWin():
    """
    On vérifie que le nombre d'ennemis n'est pas à 0 ou alors que le joueur n'est pas à cours de vie.
    :return:
    """
    if len(ennemies.soldiers) == 0:
        showinfo(title="Victory", message="You saved the humanity !")
        saveScore()
        endGame()
        showScore()

    elif player.lives == 0:
        showinfo(title="Lost", message="Humanity has been destroy !")


def close_window():
    """
    Ferme la fenêtre proprement.
    :return:
    """
    mainwindow.destroy()


def startGame():
    """
    Permet de recommencer une partie.
    :return:
    """
    endGame()
    ennemies.invade()


def endGame():
    """
    Permet d'arrêter une partie.
    :return:
    """
    player.lasers = []
    player.xcor = 500
    player.ycor = 750
    player.lives = 3
    player.score = 0
    place.coords(player.player, player.xcor, player.ycor)

    for soldier in ennemies.soldiers:  # Pour chaque ennemi on va supprimer ses lasers.
        for laser in soldier.lasers:
            soldier.pop(laser)

    ennemies.reset()


def saveScore():
    """
    Cette fonction permet d'enregistrer un score en cas de victoire
    :return:
    """
    with open("scores.txt", "a") as score:
        line = f"{player.score}/{player.lives}\n"
        score.writelines(line)


def showScore():
    """
    La fonction affiche les scores enregistrés dans le fichier score.txt
    :return:
    """
    with open("scores.txt", "r") as score:
        index = 1
        for line in score.readlines():
            infos = line.split(sep="/")
            write = f"Score: {infos[0]} | Lives: {infos[1]}"
            history.insert(index, write)
            index += 1


def showAbout():
    """
    Voici le fameux 'À propros ...'.
    :return:
    """
    endGame()
    showinfo(title="About...", message="You can try to press 'c' or 'p',  thank me later ;)")

def showOptions():
    """
    À terminer.
    :return:
    """
    endGame()
    showinfo(title="Options", message="Options are coming soon...")

mainwindow = Tk()  # Création de la fenêtre.
mainwindow.title("Space Invaders 2020")

gameplace = Frame(mainwindow)  # Frame dans laquelle le jeu et les commandes se trouveront.
gameplace.pack(side=LEFT)

place = Canvas(gameplace,
               width=wwidth,
               height=wheight,
               bg="grey")  # Canvas qui correspond au champ de bataille
Fond = PhotoImage(file='Images/spacejp.png')  # Fond du canvas
place.create_image(0, 0, anchor=NW, image=Fond)
place.pack()

player = Player(xcor=500, ycor=750)  # Création du joueur

place.focus_set()
place.bind("<Key>", player.action)  # Permet de gérer les événements du joueur.

ui = UI()  # Création de l'interface graphique dans le canvas.


gameFrame = LabelFrame(mainwindow,
                       text="Game")
gameFrame.pack()


uiplace = Frame(gameFrame)  # Deuxième interface graphique, celle qui contient les bouttons.
uiplace.pack(side=RIGHT)  # On place cette interface sur la gauche.

historyFrame = LabelFrame(uiplace)
historyFrame.pack()

historyLabel = Label(historyFrame,
                     text="History")
historyLabel.pack()

history = Listbox(historyFrame, height=5)
history.pack()


controlsFrame = LabelFrame(uiplace,
                           text="------------Controls------------",
                           width=100,
                           height=90)
controlsFrame.pack()

startButton = Button(controlsFrame,
                     text='Start',
                     command=startGame)  # Boutton qui lance une partie
startButton.pack(side=LEFT)

endButton = Button(controlsFrame,
                   text='End',
                   command=endGame)  # Boutton qui arrête une partie
endButton.pack(side=LEFT)

quitButton = Button(controlsFrame,
                    text='Quit',
                    command=close_window)  # Boutton qui permet de quitter
quitButton.pack(side=RIGHT)

optionsFrame = LabelFrame(mainwindow,
                          text="----------------More----------------")
optionsFrame.pack()


optionsButton = Button(optionsFrame,
                       text="Options",
                       command=showOptions)
optionsButton.pack(side=RIGHT)


aboutButton = Button(optionsFrame,
                     text="About...",
                     command= showAbout)
aboutButton.pack(side=LEFT)

ennemies = Horde(number=10)  # Création de la horde d'ennemis

checkLoop()  # Vérifie continuellement les collisions
bonusMaker()  # Crée un bonus de manière aleatoire
showScore()  # Affiche l'historique des scores

mainwindow.mainloop()  # Boucle principale de la fenêtre

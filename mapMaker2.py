import fltk
import os
import random
import time

MAX_H = 500
MAX_L = MAX_H
PATH = "ui/tuiles"

def effacer_multiple_objets(objets):
    for obj in objets:
        fltk.efface(obj)

def cree_interface(largeur, hauteur):
    grilleClics = []
    grilleTerm = []
    fltk.cree_fenetre(largeur, hauteur)
    for i, ligne in enumerate(range(0, hauteur, hauteur//10)):
        grilleClics.append([])
        grilleTerm.append([])
        for colonne in range(0, largeur, largeur//10):
            grilleClics[i].append([[ligne, ligne+hauteur//10],[colonne, colonne+largeur//10]])
            grilleTerm[i].append(None)
            
    return grilleClics, grilleTerm

def recuperer_tuiles():
    dicTuiles = {}
    for tuile in os.listdir(PATH):
        dicTuiles[tuile.split(".")[0]] = PATH + "/" + tuile
    return dicTuiles

def obtenir_clic(grille):
    # i = y, j = x
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j][0][0] < fltk.abscisse_souris() <= grille[i][j][0][1] and grille[i][j][1][0] < fltk.ordonnee_souris() <= grille[i][j][1][1]:
                return i, j

def clic_valide(grille, y, x):
    return 0 <= y < len(grille) and 0 <= x < len(grille[0])

def get_compatible_elements(grille, y, x, tuiles):
    directions = [
        (-1, 0, 0, 2),  # top
        (0, 1, 1, 3),   # right
        (1, 0, 2, 0),   # bottom
        (0, -1, 3, 1)   # left
    ]
    constraints = []

    for dy, dx, my_side, neighbor_side in directions:
        ny, nx = y + dy, x + dx
        if clic_valide(grille, ny, nx) and grille[ny][nx]:
            neighbor = grille[ny][nx]
            if isinstance(neighbor, str) and len(neighbor) == 4:
                constraints.append((my_side, neighbor[neighbor_side]))

    compatible = []
    for e in tuiles:
        if len(e) != 4:
            continue
        if all(e[side] == expected for side, expected in constraints):
            compatible.append(e)

    return compatible

def ile_automatique(grilleClics, grilleTerm):
    maxY, maxX = len(grilleTerm), len(grilleTerm[0])
    for i in range(maxX):
        grilleTerm[0][i] = "SSSS"
        grilleTerm[maxY-1][i] = "SSSS"
        fltk.image((grilleClics[0][i][0][0]+grilleClics[0][i][0][1])/2, (grilleClics[0][i][1][0]+grilleClics[0][i][1][1])/2, tuilesPng['SSSS'], largeur=50, hauteur=50, ancrage='center')
        fltk.image((grilleClics[maxY-1][i][0][0]+grilleClics[maxY-1][i][0][1])/2, (grilleClics[maxY-1][i][1][0]+grilleClics[maxY-1][i][1][1])/2, tuilesPng['SSSS'], largeur=50, hauteur=50, ancrage='center')
    for i in range(maxY):
        grilleTerm[i][0] = "SSSS"
        grilleTerm[i][maxX-1] = "SSSS"
        fltk.image((grilleClics[i][0][0][0]+grilleClics[i][0][0][1])/2, (grilleClics[i][0][1][0]+grilleClics[i][0][1][1])/2, tuilesPng['SSSS'], largeur=50, hauteur=50, ancrage='center')
        fltk.image((grilleClics[i][maxX-1][0][0]+grilleClics[i][maxX-1][0][1])/2, (grilleClics[i][maxX-1][1][0]+grilleClics[i][maxX-1][1][1])/2, tuilesPng['SSSS'], largeur=50, hauteur=50, ancrage='center')

def remplir_grille_possibilites(possibilites):
    minHauteur, maxHauteur = MAX_H*2//10, MAX_H*8//10
    minLargeur, maxLargeur = MAX_H*2//10, MAX_L*8//10
    tailleCase = (maxHauteur-minHauteur)//5
    grille = [[None for i in range(5)] for j in range(5)]
    grilleClics = []
    obj_index = 0
    for i,ligne in enumerate(range(len(grille))):
        grilleClics.append([])
        for j,colonne in enumerate(range(len(grille[i]))):
            if obj_index < len(possibilites):
                grille[i][j] = possibilites[obj_index]
                grilleClics[i].append([[minLargeur+j*tailleCase, minLargeur+(j+1)*tailleCase], [minHauteur+i*tailleCase, minHauteur+(i+1)*tailleCase]])
                obj_index += 1
            else:
                break
    return grille, grilleClics

def afficher_menu_possibilites(grillePoss, grillePossClics):
    objets = []
    for y in range(len(grillePoss)):
        for x in range(len(grillePoss[y])):
            if grillePoss[y][x] is None:
                return objets
            objets.append(fltk.image((grillePossClics[y][x][0][0]+grillePossClics[y][x][0][1])/2, (grillePossClics[y][x][1][0]+grillePossClics[y][x][1][1])/2, PATH + "/" + grillePoss[y][x] + ".png", largeur=40, hauteur=40, ancrage='center', tag=f'im{y}{x}'))
            objets.append(fltk.rectangle(grillePossClics[y][x][0][0]+10, grillePossClics[y][x][1][0]+10, grillePossClics[y][x][0][1]-10, grillePossClics[y][x][1][1]-10, 'grey'))

def menu_possibilites(grilleClics, possibilites):
    affichage = [fltk.rectangle(grilleClics[2][2][0][0], grilleClics[2][2][1][0], grilleClics[-3][-3][0][1], grilleClics[-3][-3][1][1], 'grey', 'white', 1, "menuPossib")]
    
    grillePoss, grillePossClics = remplir_grille_possibilites(possibilites)
    affichage += afficher_menu_possibilites(grillePoss, grillePossClics)
    
    #y,x = obtenir_clic(grille)
    while True:
        stat_clic = False
        clic = fltk.attend_ev()
        ty_clic = fltk.type_ev(clic)
        
        if ty_clic == "ClicGauche":
            y, x = obtenir_clic(grilleClics)
            y, x = y-2, x-2
            stat_clic = True
        
            effacer_multiple_objets(affichage)
            
            return stat_clic, grillePoss[x][y]

if __name__ == '__main__':
    grilleClics, grilleTerm = cree_interface(MAX_L, MAX_H)
    tuilesPng = recuperer_tuiles()
    
    ile_automatique(grilleClics, grilleTerm)
    
    #fltk.image((grilleClics[4][4][0][0]+grilleClics[4][4][0][1])/2, (grilleClics[4][4][1][0]+grilleClics[4][4][1][1])/2, tuilesPng['FFFF'], largeur=50, hauteur=50, ancrage='center', tag='im44')
    #grilleTerm[4][4] = 'FFFF'
    
    while True:
        clic = fltk.attend_ev()
        ty_clic = fltk.type_ev(clic)
        
        if ty_clic == "ClicDroit":
            break
        elif ty_clic == "ClicGauche":
            fltk.efface('texteVide')
            y, x = obtenir_clic(grilleClics)
            if not clic_valide(grilleTerm, y, x):
                continue
   
            options = get_compatible_elements(grilleTerm, y, x, tuilesPng)
            #print(options)
            #print(len(options))
            if options: #menu_possibilites(grilleClics, possibilites)
                st_clic, choice = menu_possibilites(grilleClics, options)
                #choice = random.choice(options)
                if st_clic:
                    grilleTerm[y][x] = choice
                    fltk.image((grilleClics[y][x][0][0]+grilleClics[y][x][0][1])/2, (grilleClics[y][x][1][0]+grilleClics[y][x][1][1])/2, tuilesPng[choice], largeur=50, hauteur=50, ancrage='center', tag=f'im{y}{x}')
            else:
                fltk.texte(250, 250, 'Aucune possibilité', couleur = 'red', remplissage = 'white', ancrage = 'center', police = 'Helvetica', taille = 30, tag = 'texteVide')
                
    fltk.attend_fermeture()
    
    
    
    
    
    
    
    
    
    

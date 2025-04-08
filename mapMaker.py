import fltk
import os
import random

MAX_H = 500
MAX_L = MAX_H

def creeInterface(largeur, hauteur):
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

def recupererTuiles():
    dicTuiles = {}
    path = "ui/tuiles"
    for tuile in os.listdir(path):
        dicTuiles[tuile.split(".")[0]] = path + "/" + tuile
    return dicTuiles

def obtenirClic(grille):
    # i = y, j = x
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j][0][0] < fltk.abscisse_souris() <= grille[i][j][0][1] and grille[i][j][1][0] < fltk.ordonnee_souris() <= grille[i][j][1][1]:
                return i, j

# le nom d'une figure : haut, droite, bas, gauche

def verifieAccord(grilleTerm, pos, tuiles):
    y, x = pos
    maxY, maxX = len(grilleTerm)-1, len(grilleTerm[0])-1
    tuilesPossibles = [] #list(tuiles)
    ### tuileAct = grilleTerm[y][x] # tuile située à la position (x,y)
    
    if 0 <= y-1 <= maxY and 0 <= x <= maxX:
        tuileHaute = grilleTerm[y-1][x]
        if tuileHaute != None:
            tuilesPossibles += list(tui for tui in tuiles if tui[0] == tuileHaute[2])
    
    if 0 <= y <= maxY and 0 <= x+1 <= maxX:
        tuileDroite = grilleTerm[y][x+1]
        if tuileDroite != None:
            tuilesPossibles += list(tui for tui in tuiles if tui[1] == tuileDroite[3])
        
    if 0 <= y+1 <= maxY and 0 <= x <= maxX:
        tuileBasse = grilleTerm[y+1][x]
        if tuileBasse != None:
            tuilesPossibles += list(tui for tui in tuiles if tui[2] == tuileBasse[0])
        
    if 0 <= y <= maxY and 0 <= x-1 <= maxX:
        tuileGauche = grilleTerm[y][x-1]
        if tuileGauche != None:
            tuilesPossibles += list(tui for tui in tuiles if tui[3] == tuileGauche[1])

    return tuilesPossibles

if __name__ == '__main__':
    grilleClics, grilleTerm = creeInterface(MAX_L, MAX_H)
    tuilesPng = recupererTuiles()
    
    fltk.image((grilleClics[4][4][0][0]+grilleClics[4][4][0][1])/2, (grilleClics[4][4][1][0]+grilleClics[4][4][1][1])/2, tuilesPng['FFFF'], largeur=50, hauteur=50, ancrage='center', tag='im44')
    grilleTerm[4][4] = 'FFFF'
    
    while True:
        clic = fltk.attend_ev()
        ty_clic = fltk.type_ev(clic)
        
        if ty_clic == "ClicDroit":
            break
        elif ty_clic == "ClicGauche":
            y, x = obtenirClic(grilleClics)
            rndd = random.choice(verifieAccord(grilleTerm, (y,x), tuilesPng))
            fltk.image((grilleClics[y][x][0][0]+grilleClics[y][x][0][1])/2, (grilleClics[y][x][1][0]+grilleClics[y][x][1][1])/2, tuilesPng[rndd], largeur=50, hauteur=50, ancrage='center', tag=f'im{y}{x}')
            grilleTerm[y][x] = rndd
            #fltk.rectangle(grilleClics[y][x][0][0], grilleClics[y][x][1][0], grilleClics[y][x][0][1], grilleClics[y][x][1][1])
        
    fltk.attend_fermeture()
    
    
    
    
    
    
    
    
    
    
    
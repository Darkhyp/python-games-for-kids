from .CONFIGS import *
import numpy as np


def coordinate(case):
    return GRID_STEP[0] * case[0] + GRID_STEP[0]/2,\
           GRID_STEP[1] * ((GRID_NXY[1]-1)-case[1]) + GRID_STEP[1]*3/2

def placer_pion(couleur, colonne, grille):
    isPlace = False
    line_gagne = None
    ind = np.where(grille[colonne,:] == -1)[0]
    isPlace = len(ind) > 0
    if isPlace:
        ligne = ind[0]
        grille[colonne,ligne] = couleur
        line_gagne = gagnant(couleur, colonne,ligne, grille)
    return isPlace,grille,line_gagne

def verifier_ensemble(n,couleur,pos,grille):
    """
    verifier que la ligne a un ensemble séquentiel de n éléments
    """
    if n>grille.size:
        return None
    if n>(np.where(grille==couleur)[0]).size:
        return None
    minval = 0 if(pos<(n-1)) else pos-(n-1)
    maxval = (pos if(pos<grille.size-(n-1)) else grille.size-n)
    for i in range(minval, maxval + 1):
        if np.all(grille[i:i+n] == couleur):
            return i,i+(n-1)

def verifier(line_gagne,func,couleur,pos,ensemble):
    tmp = None
    for n in range(4,7+1):
        tmp1 = verifier_ensemble(n, couleur, pos, ensemble)
        if tmp1 is None:
            break
        tmp = tmp1
    if not (tmp is None):
        line_gagne.append((func(tmp[0]),func(tmp[1])))

def gagnant(couleur, colonne,ligne, grille):
    line_gagne = []

    # colonne gagnant
    # if (ligne >= 3):
    #     if np.all(grille[colonne, ligne-3:ligne+1] == couleur):
    #         line_gagne.append(((colonne,ligne-3),(colonne,ligne)))
    verifier(line_gagne, lambda t: (colonne,t), couleur, ligne, grille[colonne,:])

    # ligne gagnant
    verifier(line_gagne, lambda t: (t,ligne), couleur, colonne, grille[:,ligne])

    # direct diag gagnant
    offset = ligne-colonne
    x0 = offset if offset<0 else 0
    y0 = offset if offset>0 else 0
    verifier(line_gagne, lambda t: (t - x0, y0 + t), couleur, colonne + x0, np.diagonal(grille, offset=offset))

    # indirect diag gagnant
    offset = ((grille.shape[1]-1)-ligne)-colonne
    x0 = offset if offset<0 else 0
    y0 = offset if offset>0 else 0
    verifier(line_gagne, lambda t: (t - x0,ligne - (t -x0 - colonne)), couleur, colonne + x0, np.diagonal(np.flip(grille,axis=1), offset=offset))

    return line_gagne
from optimisation import *
import sys


def main():
    try:
        donnees = sys.argv[1]
        solution = sys.argv[2]
        tempsMax = int(sys.argv[3])
    except:
        raise Exception("Erreur à la lecture des arguments. Syntaxe de la commande :\n\
            python3 evaluation.py <chemin_vers_fichier_d_entree> <chemin_vers_fichier_de_solution> <temps_max>")

    p = Programme(donnees, solution)
    p.recupererDonnees()
    p.setAlgorithmeResolution(Genetique(p, tempsMax=tempsMax, taillePopulation=15, maxNbToursDepuisEvolution= 2 * p.getNbIngredients()))
    p.trouverSolution()
    p.ecrireResultat()


if __name__ == "__main__":
    # import cProfile
    # import re
    # cProfile.run('main()')
    main()

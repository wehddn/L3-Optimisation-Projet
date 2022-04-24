from optimisation import *
import sys


def main():
    try:
        donnees = sys.argv[1]
        solution = sys.argv[2]
    except:
        raise Exception("Erreur à la lecture des arguments. Syntaxe de la commande :\n\
            python3 evaluation.py <chemin_vers_fichier_d_entree> <chemin_vers_fichier_de_solution>")

    p = Programme(donnees, solution)
    p.setAlgorithmeResolution(Genetique(p, 64, 300))
    p.trouverSolution()


if __name__ == "__main__":
    main()

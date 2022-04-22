from optimisation import *


def main():
    p = Programme()
    p.setAlgorithmeResolution(ExplorationTotale(p))
    p.trouverSolution("DonneesCodePizza/a_exemple.txt")
    print(p)


if __name__ == "__main__":
    main()

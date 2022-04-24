from typing import Iterable
import random
import sys

clients: list = []
ingredients: list = []
solution: list = []
nbIndividus = 50
nbEnfants = 40
scoreCible = 1740
tempsMax = 100

meilleurIndividu = ""
meilleurScore = -1

individus = dict()
enfants = dict()
selectionParents = list()
selectionEnfants = list()


def main():
    try:
        cheminDonnees = sys.argv[1]
        cheminSolution = sys.argv[2]
        nbIndividus = int(sys.argv[3])
        tempsMax = float(sys.argv[4])
    except:
        raise Exception("Erreur à la lecture des arguments. Syntaxe de la commande :\n\
            python3 evaluation.py <chemin_vers_fichier_d_entree> <chemin_vers_fichier_de_sortie> <nb_individus> <score_cible> <temps_max>")

    # p = Programme(cheminDonnees, solution)
    # p.setAlgorithmeResolution(Genetique(p, nbIndividus, tempsMax))
    # p.trouverSolution()
    # global clients
    # global ingredients
    # # Récupération des données
    gd = GestionnaireDonnees()
    gd.getDonnees(cheminDonnees)
    # # Algo de résolution

    recherche()
    print(f"{meilleurIndividu} : {meilleurScore}")


class Client:
    """
    Classe représentant un client

    Attributes
    ----------
    ingredientsAimes : set[int]
        La liste des ingrédients que le client aime (index)
    ingredientsNonAimes : set[int]
        La liste des ingrédients que le client n'aime pas (index)
    """
    ingredientsAimes: list[int]
    ingredientsNonAimes: list[int]

    def __init__(self) -> None:
        self.ingredientsAimes = list()
        self.ingredientsNonAimes = list()

    def addIngredientsAimes(self, indexIngredients: Iterable) -> None:
        """
        Ajoute l'ingredient à la liste des ingredients que le client aime

        Parameters
        ----------
        indexIngredient : int
            L'index de l'ingrédient
        """
        self.ingredientsAimes.extend(indexIngredients)

    def addIngredientsNonAimes(self, indexIngredient: Iterable) -> None:
        """
        Ajoute l'ingredient à la liste des ingredients que le client n'aime pas

        Parameters
        ----------
        indexIngredient : int
            L'index de l'ingrédient
        """
        self.ingredientsNonAimes.extend(
            indexIngredient)

    def recetteAcceptable(self, recette: str) -> bool:
        """
        Dit si le client peut manger une pizza contenant certains ingredients

        Parameters
        ----------
        recette : str
            la Recette de la pizza (1 à l'index i = ingredient no i présent)
        """
        recetteSet = list()
        for i in range(len(recette)):
            if recette[i] == '1':
                recetteSet.append(i)
        recetteSet = set(recetteSet)
        contientAimes = set(self.ingredientsAimes).issubset(
            recetteSet)
        neContientNonAimes = len(set(self.ingredientsNonAimes).intersection(
            recetteSet)) == 0
        return (contientAimes and neContientNonAimes)


class GestionnaireDonnees:

    def getInt(self, texte: str, message: str) -> int:
        """
        Donne l'entier correspondant du texte, dans le cas ou ce n'est pas un
        entier lance une exception

        Parameters
        ----------
        texte: str
            Le texte à convertir
        message: str
            Le message de l'exception
        """
        if (not texte.isdecimal()):
            raise Exception(message)
        return int(texte)

    def ajouterIngredients(self, ings: Iterable) -> Iterable:
        global ingredients
        index = set()
        for ingredient in ings:
            # Si l'ingrédient existe déjà on renvoie son index
            if ingredient in ingredients:
                index.add(ingredients.index(ingredient))
            else:
                # Sinon on le rajoute et on renvoie son nouvel index
                ingredients.append(ingredient)
                index.add(len(ingredients) - 1)
        return index

    def ajouterClient(self, noClient: int,  ligne1: str, ligne2: str) -> None:
        """
        Ajoute un client dans le programme avec les infos fournies et déclenche
        une exception en cas de problème

        Parameters
        ----------
        noClient: int
            Le numéro du client
        ligne1: str
            La ligne contenant les infos sur ses ingrédients aimés
        ligne2: str
            La ligne contenant les infos sur ses ingrédients non aimés
        """
        # Vérification de la validité des infos
        if not ligne1:
            raise Exception("La ligne des ingredients aimés du client no {noClient} est vide".format(
                noClient=noClient))
        if not ligne2:
            raise Exception("La ligne des ingredients non aimés du client no {noClient} est vide".format(
                noClient=noClient))

        ligne1 = ligne1.split(" ")
        ligne2 = ligne2.split(" ")

        nbIngredientsA = self.getInt(
            ligne1[0], "Le nombre d'ingrédients aimés du client {noClient} n'est pas spécifié".format(noClient=noClient))
        if nbIngredientsA != len(ligne1) - 1:
            raise Exception("Le nombre d'ingrédients aimés du client {noClient} ne correspond pas au nombre d'ingredients donnés".format(
                noClient=noClient))

        nbIngredientsNA = self.getInt(
            ligne2[0], "Le nombre d'ingrédients non aimés du client {noClient} n'est pas spécifié".format(noClient=noClient))
        if nbIngredientsNA != len(ligne2) - 1:
            raise Exception("Le nombre d'ingrédients non aimés du client {noClient} ne correspond pas au nombre d'ingredients donnés".format(
                noClient=noClient))

        global clients

        # Enregistrement du client et de ces ingredients
        client = Client()
        index = self.ajouterIngredients(list(ligne1[1:]))
        client.addIngredientsAimes(index)
        client.addIngredientsAimes(index)
        index = self.ajouterIngredients(ligne2[1:])
        client.addIngredientsNonAimes(index)

        clients.append(client)

    def getDonnees(self, nomFichier: str) -> None:
        global clients
        global ingredients

        clients = list()
        ingredients = list()
        with open(nomFichier, "r") as fichier:
            # Lecture de l'entête (nombre de clients)
            ligne = fichier.readline().strip('\n')
            nbClients = self.getInt(ligne,
                                    "Le ficher n'est pas valide, la première ligne doit être le nombre de client (entier)")
            # Récupération des clients et enregistrement de leurs infos
            for i in range(nbClients):
                ligne1 = fichier.readline().strip('\n')
                ligne2 = fichier.readline().strip('\n')
                self.ajouterClient(i, ligne1, ligne2)

    def ecrireResultat(self, nomFichier: str) -> None:
        """
        Ecrit les résultats du programme dans le fichier spécifié

        Parameters
        ----------
        nomFichier: str
            Le chemin du fichier dans lequel ecrire
        """
        global solution
        text = str(len(solution))
        for s in solution:
            text += " " + s
        with open(nomFichier, "w") as fichier:
            fichier.write(text)


class Genetique:

    nbIndividus: int
    nbEnfants: int
    scoreCible: int
    tempsMax: float

    meilleurIndividu: str
    meilleurScore: int

    individus: dict[str, int]
    enfants: dict[str, int]
    selectionParents: list[tuple[str, str]]
    selectionEnfants: list[str]

    def __init__(self, nbIndividus, nbEnfants, scoreCible, tempsMax) -> None:
        global ingredients
        self.nbIndividus = min(
            2 ** len(ingredients) - 1, nbIndividus)
        self.nbEnfants = min(
            2 ** len(ingredients) - 1, nbEnfants)
        self.scoreCible = scoreCible
        self.tempsMax = tempsMax
        self.selectionParents = list()
        self.selectionEnfants = list()

    def fitness(self, individu: str) -> int:
        global clients
        fitness = 0
        for client in clients:
            if client.recetteAcceptable(individu):
                fitness += 1
        return fitness


def genererPopulation():
    global ingredients, individus, enfants, nbIndividus, meilleurScore, meilleurIndividu
    nbIngredients = len(ingredients)
    individus = dict()
    enfants = dict()
    random.seed()
    # Genere la population
    while len(individus) < nbIndividus:
        valeurAleatoire = random.randint(0, 2**nbIngredients - 1)
        recette = format(valeurAleatoire, 'b').rjust(nbIngredients, '0')
        individus[recette] = -1
    meilleurScore = -1
    meilleurIndividu = ""


def evaluerIndividus():
    global individus, meilleurScore, meilleurIndividu
    for cle in individus.keys():
        if not cle in individus or individus[cle] == -1:
            fitness = 0
            for client in clients:
                if client.recetteAcceptable(cle):
                    fitness += 1
            individus[cle] = fitness
        if individus[cle] > meilleurScore:
            meilleurScore = individus[cle]
            meilleurIndividu = cle


def selectionReproduction(puissance: int = 3):
    global selectionParents, nbIndividus, individus
    probabilites = []
    keys = []
    selectionParents = list()
    nbIndividus = nbIndividus
    for (i, key) in enumerate(sorted(individus, key=individus.get, reverse=True)):
        probabilite = ((1 - (i + 1)/nbIndividus) ** puissance)
        probabilites.append(probabilite)
        keys.append(key)

    random.seed()
    while len(selectionParents) < nbIndividus:
        selectionParents.append(random.choices(
            keys, weights=probabilites, k=2))


def croisement():
    global selectionEnfants, nbEnfants, selectionParents
    selectionEnfants = list()
    continuer = True
    while len(selectionEnfants) < nbEnfants and continuer:
        for couple in selectionParents:
            random.seed()
            bits = random.choices([True, False], weights=[
                                  1.0, 1.0], k=len(couple[0]))
            enfant = ""
            for (i, bit) in enumerate(bits):
                if bit:
                    enfant += couple[0][i]
                else:
                    enfant += couple[1][i]
            selectionEnfants.append(enfant)
            if len(selectionEnfants) >= nbEnfants:
                continuer = False
                break


def mutation(probabilite=1/100):
    global selectionEnfants
    for (i, enfant) in enumerate(selectionEnfants):
        mutation = ""
        random.seed()
        for bit in enfant:
            if random.uniform(0.0, 1.0) <= probabilite:
                if bit == "0":
                    mutation += "1"
                else:
                    mutation += "0"
            else:
                mutation += bit
        selectionEnfants[i] = mutation


def evaluerEnfants():
    global meilleurIndividu, meilleurScore, enfants, individus, selectionEnfants
    for cle in selectionEnfants:
        if not cle in individus or not cle in enfants:
            fitness = 0
            for client in clients:
                if client.recetteAcceptable(cle):
                    fitness += 1
            enfants[cle] = fitness
        if enfants[cle] > meilleurScore:
            meilleurScore = enfants[cle]
            meilleurIndividu = cle


def selectionRemplacement():
    global enfants, nbEnfants, individus, nbIndividus
    meilleurs = dict()
    for enfant in sorted(enfants, key=enfants.get, reverse=True):
        if len(meilleurs) < nbEnfants:
            meilleurs[enfant] = enfants[enfant]
        else:
            break
    for i in sorted(individus, key=individus.get, reverse=True):
        if len(meilleurs) < nbIndividus:
            meilleurs[i] = individus[i]
        else:
            break
    individus = meilleurs


def recherche():
    global meilleurIndividu, meilleurScore, scoreCible
    genererPopulation()
    evaluerIndividus()

    continuer = True
    ancienMeilleur = meilleurIndividu

    while continuer:
        selectionReproduction(4)
        croisement()
        mutation()
        evaluerEnfants()
        selectionRemplacement()
        evaluerIndividus()

        if meilleurScore >= scoreCible:
            continuer = False
        print(f"{meilleurScore}")


if __name__ == "__main__":
    main()

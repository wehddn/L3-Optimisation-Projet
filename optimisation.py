from abc import ABC, abstractclassmethod


class Programme:
    pass


class Recette:
    pass


class GestionnaireFichier:
    pass


class AlgorithmeResolution:
    pass


class Client:
    pass


class BranchAndBound:
    pass


class ExplorationTotale:
    pass


class Genetique:
    pass


class Recette:
    """
    Classe représentant une recette

    Attributes
    ----------
    __indexIngredients : list[int]
        La liste des index(dans la liste des ingredients du programme) des ingrédients
        de la recette
    """
    __indexIngredients: list[int]
    __programme: Programme

    def __init__(self, p: Programme, *args) -> None:
        """
        Constructeur

        Parameters
        ----------
        p : Programme
            Le programme de recherche de solution

        """
        if isinstance(args[0], list):
            self.__indexIngredients = args[0]
        elif isinstance(args[0], str):
            self.__indexIngredients = []
            codeIngredients = args[0]
            for i in range(len(codeIngredients)):
                if codeIngredients[i] == '1':
                    self.__indexIngredients.append(i)
        self.__programme = p

    def __repr__(self) -> str:
        ingredients = []
        for i in self.__indexIngredients:
            ingredients.append(self.__programme.getIngredient(i))
        return ingredients.__repr__()

    def getIndexIngredients(self) -> list[int]:
        """
        Donne la liste des ingredients (index) la composant

        Parameters
        ----------
        """
        return self.__indexIngredients.copy()


class Client:
    """
    Classe représentant un client

    Attributes
    ----------
    __numero : int
        Le numéro du client
    __ingredientsAimes : list[int]
        La liste des ingrédients que le client aime (index)
    __ingredientsNonAimes : list[int]
        La liste des ingrédients que le client n'aime pas (index)
    __programme : Programme
        Le programme de recherche
    """
    __numero: int
    __ingredientsAimes: list[int]
    __ingredientsNonAimes: list[int]
    __programme: Programme

    def __init__(self, p: Programme, numero: int) -> None:
        """
        Constructeur

        Parameters
        ----------
        p : Programme
            Le programme de recherche de solution
        numero : int
            Le numéro du client
        """
        self.__numero = numero
        self.__ingredientsAimes = []
        self.__ingredientsNonAimes = []
        self.__programme = p

    def __repr__(self) -> str:
        ingredientsA = []
        ingredientsNA = []
        for i in self.__ingredientsAimes:
            ingredientsA.append(self.__programme.getIngredient(i))

        for i in self.__ingredientsNonAimes:
            ingredientsNA.append(self.__programme.getIngredient(i))

        return "{{ Client {noclient} : Aime {ingredientsA}, N'aime Pas {ingredientsNA} }}".format(noclient=self.__numero, ingredientsA=ingredientsA, ingredientsNA=ingredientsNA)

    def addIngredientAime(self, indexIngredient: int) -> None:
        """
        Ajoute l'ingredient à la liste des ingredients que le client aime

        Parameters
        ----------
        indexIngredient : int
            L'index de l'ingrédient
        """
        self.__ingredientsAimes.append(indexIngredient)

    def addIngredientNonAime(self, indexIngredient: int) -> None:
        """
        Ajoute l'ingredient à la liste des ingredients que le client n'aime pas

        Parameters
        ----------
        indexIngredient : int
            L'index de l'ingrédient
        """
        self.__ingredientsNonAimes.append(indexIngredient)

    def aime(self, indexIngredient: int) -> bool:
        """
        Dit si le client aime l'ingrédient

        Parameters
        ----------
        indexIngredient : int
            L'index de l'ingrédient
        """
        if indexIngredient in self.__ingredientsAimes:
            return True
        return False

    def aimePas(self, indexIngredient: int) -> bool:
        """
        Dit si le client n'aime pas l'ingrédient

        Parameters
        ----------
        indexIngredient : int
            L'index de l'ingrédient
        """
        if indexIngredient in self.__ingredientsNonAimes:
            return True
        return False

    def recetteAcceptable(self, r: Recette) -> bool:
        """
        Dit si le client peut manger une pizza contenant certains ingredients

        Parameters
        ----------
        r : Recette
            la Recette de la pizza
        """
        ingredientsASet = set(self.__ingredientsAimes)
        ingredientsNASet = set(self.__ingredientsNonAimes)
        recetteSet = set(r.getIndexIngredients())
        contientAimes = ingredientsASet.issubset(
            recetteSet)
        neContientNonAimes = len(ingredientsNASet.intersection(
            recetteSet)) == 0
        return (contientAimes and neContientNonAimes)


class GestionnaireFichier:
    """
    Classe responsable de la recupération et de l'écriture des données dans
    des fichiers

    Attributes
    ----------
    __programme : Programme
        Le programme de recherche
    """
    __programme: Programme

    def __init__(self, p: Programme) -> None:
        self.__programme = p

    def getDonnees(self, nomFichier: str) -> None:
        """
        Récupére les données à partir d'un fichier et les transmet au programme

        Parameters
        ----------
        nomFichier: str
            Le chemin du fichier
        """
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
        solution = self.__programme.getIngredientsSolution()
        text = str(len(solution))
        for s in solution:
            text += " " + s
        with open(nomFichier, "w") as fichier:
            fichier.write(text)


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

        # Enregistrement du client et de ces ingredients dans le programme
        client = Client(self.__programme, noClient)
        for ingredient in ligne1[1:]:
            client.addIngredientAime(
                self.__programme.ajouterIngredient(ingredient))
        for ingredient in ligne2[1:]:
            client.addIngredientNonAime(
                self.__programme.ajouterIngredient(ingredient))

        self.__programme.ajouterClient(client)


class AlgorithmeResolution(ABC):
    _programme: Programme

    def __init__(self, p: Programme) -> None:
        super().__init__()
        self._programme = p

    @abstractclassmethod
    def trouverSolution(self) -> Recette:
        pass


class BranchAndBound(AlgorithmeResolution):
    def __init__(self, p: Programme) -> None:
        super().__init__(p)

    def trouverSolution(self) -> Recette:
        pass


class ExplorationTotale(AlgorithmeResolution):
    def __init__(self, p: Programme) -> None:
        super().__init__(p)

    def trouverSolution(self) -> Recette:
        noBit = 0  # le no du bit qu'il faut changer
        # on obtient le code pour representer les ingredients
        nbIngredients = self._programme.getNbIngredients()
        meilleurSolution = ("1", 0)
        avisite = ["0", "1"]

        while avisite:  # On utilise la boucle while et la pile pour simuler une recursivité
            next = avisite.pop(0)
            score = self.calculerScore(next)
            if score > meilleurSolution[1]:
                meilleurSolution = (next, score)

            if len(next) < nbIngredients:
                avisite.append(next + "0")
                avisite.append(next + "1")
        return Recette(self._programme, meilleurSolution[0])

    def calculerScore(self, codeRecette: str) -> int:
        score = 0
        r = Recette(self._programme, codeRecette)
        for i in self._programme.getClients():
            if i.recetteAcceptable(r):
                score += 1
        return score


class Programme:
    """Classe représentant le programme de recherche de solution"""
    __cheminEntree: str
    __cheminSortie: str
    __ingredients: list[str]
    __ingredientsSolution: list[str]
    __clients: list[Client]
    __gestionFichier: GestionnaireFichier
    __resolveur: AlgorithmeResolution

    def __init__(self, entree:str, sortie:str) -> None:
        self.__cheminEntree = entree
        self.__cheminSortie = sortie
        self.__ingredients = []
        self.__ingredientsSolution = []
        self.__clients = []
        self.__gestionFichier = GestionnaireFichier(self)
        self.__resolveur = ExplorationTotale(self)

    def __repr__(self) -> str:
        retour = "Ingredients : " + self.__ingredients.__repr__() + "\nClients :"
        for client in self.__clients:
            retour += "\n" + client.__repr__()
        retour += "\nIngredients solution : " + self.__ingredientsSolution.__repr__()
        return retour

    def setAlgorithmeResolution(self, ar: AlgorithmeResolution) -> None:
        self.__resolveur = ar

    def ajouterIngredient(self, ingredient: str) -> None:
        # Si l'ingrédient existe déjà on renvoie son index
        if ingredient in self.__ingredients:
            return self.__ingredients.index(ingredient)
        # Sinon on le rajoute et on renvoie son nouvel index
        self.__ingredients.append(ingredient)
        return len(self.__ingredients) - 1

    def getIngredient(self, indexIngredient: int) -> str:
        return self.__ingredients[indexIngredient]

    def ajouterClient(self, c: Client) -> None:
        self.__clients.append(c)

    def trouverSolution(self) -> None:
        # Recupération des données
        self.__gestionFichier.getDonnees(self.__cheminEntree)
        meilleurRecette = self.__resolveur.trouverSolution()
        # Recherche de solution
        solution = []
        for i in meilleurRecette.getIndexIngredients():
            solution.append(self.getIngredient(i))
        self.__ingredientsSolution = solution
        # Ecriture du résultat
        self.__gestionFichier.ecrireResultat(self.__cheminSortie)

    def getNbIngredients(self) -> int:
        return len(self.__ingredients)

    def getClients(self) -> list[Client]:
        return self.__clients

    def getIngredientsSolution(self) -> list[str]:
        return self.__ingredientsSolution

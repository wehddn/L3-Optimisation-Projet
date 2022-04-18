from itertools import count


def main():
    clients = lireDonnees("DonneesCodePizza/a_exemple.txt")
    print(clients)

class Client:
    def __init__(self, numero, ingredientsA:list[str], ingredientsNA:list[str]):
        self.numero = numero
        self.ingredientsA = ingredientsA
        self.ingredientsNA = ingredientsNA

    def __repr__(self):
     return "Client " + str(self.numero) + " aime : " + self.ingredientsA.__str__() + ", n'aime pas : " + self.ingredientsNA.__str__()


def lireDonnees(chemin:str) -> list[Client]:
    with open(chemin) as fichier:
        #Recupere le nombre des clients
        nombre = fichier.readline().strip('\n')
        #Le nombre des clients doit etre un entier 
        checkInt(nombre)

        nombre = int(nombre)

        clients = []

        for i in range(nombre):
            ligneA = lireLigneClient(fichier.readline())
            ligneNA = lireLigneClient(fichier.readline())
            clients.append(Client(i, ligneA[1:len(ligneA)], ligneNA[1:len(ligneA)]))
            
        return clients


def checkInt(valeur:str):
    if (not valeur.isdecimal()):
            raise TypeError("\"" + valeur + "\" doit etre un entier")

def lireLigneClient(ligne):
    ligne = ligne.strip('\n').split(" ")
    checkInt(ligne[0])
    if (int(ligne[0]) != len(ligne)-1):
        raise Exception("Le nombre d'ingredients ne correspond pas")
    return ligne

if __name__ == "__main__":
    main()
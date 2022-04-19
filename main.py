aimeList = []
clients = None

def main():
    global clients
    clients = lireDonnees("c_grossier.txt")

    bb("Branch_and_bound.txt")

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


def bb(nom):
    global aimeList
    global aimePasList
    #liste des tout ingredients qu'on aime
    for c in clients:
        for i in c.ingredientsA:
            aimeList.append(i)
    aimeList = list(set(aimeList))

    lst = []
    for i in range (len(aimeList)):
        lst.append(1)

    result = bbAlgo(lst, 0)
    resultWrite = ""
    count = 0
    for i in range(len(aimeList)):
        if result[i]==1:
            resultWrite=resultWrite + " " + aimeList[i]
            count+=1
    resultWrite=str(count) + resultWrite
    with open(nom, 'w') as f:
        f.write(resultWrite)


def bbAlgo(state, i):
    if i<len(state)-1:
        leftState = state.copy()
        rightState = state.copy()
        leftState[i] = 1
        rightState[i] = 0
        resultL = numberWhoLike(leftState)
        resultR = numberWhoLike(rightState)
        if resultL >= resultR:
            return bbAlgo(leftState, i+1)
        else:
            return bbAlgo(rightState, i+1)
    return state

def numberWhoLike(state):
    global aimeList
    global clients
    result = 0
    for c in clients:
        like = True
        for i in c.ingredientsA:
            if state[aimeList.index(i)]!=1 :
                like = False
        for i in c.ingredientsNA:
            try:
                if state[aimeList.index(i)]!=0 :
                    like = False
            except ValueError: 
                None
        if like:
            result+=1
    return result

if __name__ == "__main__":
    main()
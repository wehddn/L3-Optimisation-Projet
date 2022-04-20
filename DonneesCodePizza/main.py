import random
#TODO resultat de writeToFile ne correspond pas au resultat d'evaluation

aimeList = []
clients = None

def main():
    global clients
    global aimeList
    clients = lireDonnees("d_inf.txt")

    for c in clients:
        for i in c.ingredientsA:
            aimeList.append(i)
    aimeList = list(set(aimeList))

    #bb("Branch_and_bound.txt")
    gen("Algorithme_Genetique.txt", 5)

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
    
    lst = []
    for i in range (len(aimeList)): #11111
        lst.append(1)

    result = bbAlgo(lst, 0)
    writeToFile(result, nom)

def writeToFile(result, nom):
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

def gen(nom, arret):
    global aimeList

    taillePopulation = 20

    population = []
    p = 0
    while p < taillePopulation:
        lst = []
        for i in range (len(aimeList)):
            lst.append(random.randint(0,1))
        if not lst in population:
            population.append(lst)
        else:
            p-=1
        p+=1
    like = []
    for i in range (len(population)):
        like.append(numberWhoLike(population[i]))

    selection = []
    selection.append(population)
    selection.append(like)
    result = croisement(selection, 0, arret)
    print(numberWhoLike(result))
    writeToFile(result, nom)

def croisement(selection, k, arret):
    selection = getParents(selection)
    result = []
    if selection[1][0] < arret:
        for i in range (len(selection[0])):
            buff = selection[0].copy()
            point = random.randint(0, len(selection[0][i]))
            p1 = buff.pop(random.randint(0,len(buff)-1))
            p2 = buff.pop(random.randint(0,len(buff)-1))
            child1 = []
            child2 = []
            for j in range (point):
                child1.append(p1[j])
                child2.append(p2[j])
            for j in range (point, len(selection[0][i])):
                child1.append(p2[j])
                child2.append(p1[j])
            result.append(child1)
            result.append(child2)

        result = mutation(result)

        like = []
        for i in range (len(result)):
            like.append(numberWhoLike(result[i]))

        selection = []
        selection.append(result)
        selection.append(like)
        return (croisement(selection, k+1, arret))

    else:
        return selection[0][0]

def getParents(lst):
    resultp = []
    resultv = []
    
    lst_len = int(len(lst[1])/2)
    if lst_len % 2 == 1:
        lst_len+=1

    for i in range (lst_len):
        idmax = lst[1].index(max(lst[1]))
        resultp.append(lst[0].pop(idmax))
        resultv.append(lst[1].pop(idmax))
    
    result = []
    result.append(resultp)
    result.append(resultv)

    return result

def mutation(lst):
    for i in range (len(lst)):
        lst[i][random.randint(1, len(lst[i]))-1]=random.randint(0, 1)
    return lst

if __name__ == "__main__":
    main()
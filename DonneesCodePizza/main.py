import random

listIngredients = []
clients = None

def main():
    global clients
    global listIngredients
    clients = lireDonnees("d_difficile.txt")

    for c in clients:
        for i in c.ingredientsA:
            listIngredients.append(i)
        for j in c.ingredientsNA:
            listIngredients.append(j)
    listIngredients = list(set(listIngredients))

    #bb("Branch_and_bound.txt")
    gen("Algorithme_Genetique.txt", 1750)

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
            clients.append(Client(i, ligneA[1:len(ligneA)], ligneNA[1:len(ligneNA)]))
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
    global listIngredients
    
    lst = []
    for _ in range (len(listIngredients)): #11111
        lst.append(1)

    resultat = bbAlgo(lst, 0)
    ecrireDonnees(resultat, nom)

def ecrireDonnees(resultat, nom):
    resultatEcrire = ""
    count = 0
    for i in range(len(resultat)):
        if resultat[i]==1:
            resultatEcrire=resultatEcrire + " " + listIngredients[i]
            count+=1
    resultatEcrire=str(count) + resultatEcrire
    with open(nom, 'w') as f:
        f.write(resultatEcrire)

def bbAlgo(seq, i):
    if i<len(seq)-1:
        brancheGauche = seq.copy()
        brancheDroite = seq.copy()
        brancheGauche[i] = 1
        brancheDroite[i] = 0
        resultatL = nombreQuiAime(brancheGauche)
        resultatR = nombreQuiAime(brancheDroite)
        if resultatL >= resultatR:
            return bbAlgo(brancheGauche, i+1)
        else:
            return bbAlgo(brancheDroite, i+1)
    return seq

def nombreQuiAime(seq):
    global listIngredients
    global clients
    solution_list = []
    for i in range(len(seq)):
        if seq[i] == 1:
            solution_list.append(listIngredients[i])
    solution_set = set(solution_list)
    resultat = 0
    for c in clients:
        if set(c.ingredientsA).issubset(solution_set) and len(set(c.ingredientsNA).intersection(solution_set))==0:
            resultat+=1
    return resultat

def gen(nom, arret):
    global listIngredients

    taillePopulation = 50

    population = []
    p = 0
    while p < taillePopulation:
        lst = []
        for i in range (len(listIngredients)):
            lst.append(random.randint(0,1))
        if not lst in population:
            population.append(lst)
        else:
            p-=1
        p+=1
    aime = []
    for i in range (len(population)):
        aime.append(nombreQuiAime(population[i]))

    selection = []
    selection.append(population)
    selection.append(aime)
    resultat = croisementNew(selection, arret)
    ecrireDonnees(resultat, nom)

def croisement(selection, k, arret):
    selection = getParents(selection)
    resultat = []
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
            resultat.append(child1)
            resultat.append(child2)

        resultat = mutation(resultat)

        aime = []
        for i in range (len(resultat)):
            aime.append(nombreQuiAime(resultat[i]))

        selection = []
        selection.append(resultat)
        selection.append(aime)
        return (croisement(selection, k+1, arret))

    else:
        return selection[0][0]

def croisementNew(selection, arret):
    while selection[1][0] < arret:
        print(selection[1][0])
        selection = getParents(selection)
        resultat = []
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
            resultat.append(child1)
            resultat.append(child2)

        resultat = mutation(resultat)

        aime = []
        for i in range (len(resultat)):
            aime.append(nombreQuiAime(resultat[i]))
    
        selection = []
        selection.append(resultat)
        selection.append(aime)

    return selection[0][0]

def getParents(lst):
    resultat1 = []
    resultat2 = []
    
    lst_len = int(len(lst[1])/2)
    if lst_len % 2 == 1:
        lst_len+=1

    for i in range (lst_len):
        idmax = lst[1].index(max(lst[1]))
        resultat1.append(lst[0].pop(idmax))
        resultat2.append(lst[1].pop(idmax))
    
    resultat = []
    resultat.append(resultat1)
    resultat.append(resultat2)

    return resultat

def mutation(lst):
    for i in range (len(lst)):
        lst[i][random.randint(1, len(lst[i]))-1]=random.randint(0, 1)
    return lst

if __name__ == "__main__":
    main()
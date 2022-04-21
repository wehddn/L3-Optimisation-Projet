from optimisation import *


def main():
    p = Programme()
    a = p.ajouterIngredient("a")
    b = p.ajouterIngredient("b")
    c = p.ajouterIngredient("c")
    p.ajouterIngredient("d")
    e = p.ajouterIngredient("e")
    client = Client(p, 1)
    client.addIngredientAime(a)
    client.addIngredientAime(b)
    client.addIngredientAime(c)
    client.addIngredientNonAime(e)
    print(client)


if __name__ == "__main__":
    main()

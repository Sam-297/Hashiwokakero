# HASHIWOKAKERO (BRIDGES) 

###### Projet par Jad FAWAZ, Mohamad EL CHAMAA, Anthony TAHA, Sam HAJJ ASSAF

---

## Introduction

Ce programme est conçu pour résoudre les puzzles Hashiwokakero de manière efficace. Il fonctionne en convertissant d'abord la disposition de la grille et les règles concernant les ponts en une formule logique conjonctive puis en format DIMACS. Ensuite, en utilisant un solveur SAT (satisfiability), il cherche une solution qui satisfait toutes ces contraintes. Si une solution existe, le programme la trouve et la présente à l'utilisateur.

## Logiciels et langages utilisés

Logiciels :

- BDDC  ( utilisé pour transformer les formules en FNC )
- MiniSat ( utilisé pour trouver une solution de la formule )

Languages :

- Python ( Langage principal du programme )
- Shell Script ( Utilisé pour executer les commandes BDDC et Minisat )

## Installation et configuration (Linux)

Pour exécuter le programme, il faut d'abord vérifier que les bibliothèques Python et les logiciels utilisés sont téléchargés:

- **BDDC**

    Exécuter cette commande pour vérifier que BDDC a le droit d'exécution:
    ```bash
    chmod u+x bddc
    ```

    Vérifiez que l'exécutable BDDC est dans le répertoire du programme initial.
    

- **MiniSat**

    Exécuter cette commande dans le terminal:

    ```bash
    sudo apt install minisat 
    ```

- *Bibliothèque* **Tkinter**

    Exécuter cette commande dans le terminal:

    ```bash
    sudo apt install python3-tk 
    ```

- *Bibliothèque* **Pillow**

    Exécuter ces commandes dans le terminal:

    ```bash
    sudo apt install python3-pil 
    sudo apt install python3-pil.imagetk
    ```

Après les installations il suffit d'exécuter le fichier `main.py` pour utiliser le programme.

## Description du programme (Fonctions initiales)

- **ponts_possibles_croisement**
    
    Donne les combinaisons possibles en tenant compte des croisements des ponts.

- **func_combinaisons**

    Donne toutes les combinaisons possibles de ponts pour chaque île.

- **chemin**

    Donne toutes les combinaisons de ponts possibles garantissant que la configuration finale reste connectée.

- **solve**

    Regroupe les trois formules précédentes pour générer une seule formule en les transformant en forme normale conjonctive (FNC), puis convertis cette formule en format DIMACS afin que MiniSat puisse trouver la solution.

###### NB : Le nombre maximal d'îles est de 26.

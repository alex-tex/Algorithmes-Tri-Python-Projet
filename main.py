import pyxel
import random
from time import time, sleep

### Variables ###
Size = [250, 150]
bar_width = 5

status = "menu" # c'est pour le menu
tab = []
algoChoisi = None
#slow_mode = False # Mode lent pour le tri (utilise time.sleep() pour ralentir le code)
tab_original = [] 
temps_écoulé, etapes_tri = 0,0 # le temps écoulé entre les étapes et le nombre des étapes pour benchmark
display_mode = "colonne" # Mode d'affichage par défaut

### Fonctions ###

# Fonction pour générer un tableau avec des valeurs aléatoires
def get_random_tab(n):
    tableau = []   # un tableau de n valeur aléatoire allant de 0 jusqu'à hauteur écran
    for _ in range(min(n, Size[0])):
        tableau.append(random.randint(0, Size[1]))
    return tableau




def insertion(tableau):
    for i in range(1, len(tableau)):
        cle = tableau[i]
        j = i-1
    
        while j >= 0 and tableau[j] > cle:
            tableau[j+1] = tableau[j]
            j-=1

            draw()
            
            pyxel.flip()
        tableau[j+1] = cle
        
        draw()
        pyxel.flip()

def selection(tableau):
    for i in range(0, len(tableau)):
        min_index = i
        cle = tableau[i]
        for j in range(i+1, len(tableau)):
            if tableau[j] < tableau[min_index]:
                min_index = j
        tableau[min_index], tableau[i] = tableau[i], tableau[min_index]
        draw()
        pyxel.flip() 
    draw()
    pyxel.flip()   

def tri_bulle(tableau):
    n = len(tableau)
    echange = True
    while echange == True:
        echange = False
        for i in range(0, n-1):
            if tableau[i] > tableau[i + 1]:
                tableau[i],tableau[i+1] = tableau[i + 1],tableau[i]
                echange = True
                draw()
                pyxel.flip()

    draw()
    pyxel.flip()


# Fonction pour changer le mode
def ToggleMode(mode):
    if mode == "colonne":
        return "nuage"
    else:
        return "colonne"

# Fonction principale "update"
def update():
    global status, tab, algoChoisi, tab_original, etapes_tri, temps_écoulé, display_mode

    if pyxel.btnp(pyxel.KEY_SPACE):
        if status != "attente":
            nouveauMode = ToggleMode(display_mode)
            display_mode = nouveauMode
    
    if status == "menu":

        # Afficher le menu
        if pyxel.btnp(pyxel.KEY_1):
            tab = get_random_tab(Size[0]//bar_width)
      
            algoChoisi = "1"
            status = "attente"
        elif pyxel.btnp(pyxel.KEY_2):
            tab = get_random_tab(Size[0]//bar_width)
      
            algoChoisi = "2"
            status = "attente"
        elif pyxel.btnp(pyxel.KEY_3):
            tab = get_random_tab(Size[0]//bar_width)
            algoChoisi = "3"
            status = "attente"
    
    elif status == "attente":

        if pyxel.btnp(pyxel.KEY_SPACE):
            status = "tri"
            temps_écoulé = time() 
            if algoChoisi in algoritmes:
                algoritmes[algoChoisi](tab)  # c'est modulaire (+1 pnt pour ca 😎)  
                status = "done"
                temps_écoulé = time() - temps_écoulé
   
    elif status == "tri":
        print("triii")
    
    elif status == "done" and pyxel.btnp(pyxel.KEY_R):
        status = "menu"
        etape_actuelle = 0

# Fonction principale pour dessiner "draw"
def draw():
    global tab, status
    pyxel.cls(0)
    
    if status == "menu":
        x_pos = Size[0] // 2 - 30
        y_pos = Size[1] // 3
        pyxel.text(x_pos, 15, "Choisir le tri", 7)
        pyxel.text(x_pos, y_pos,      "1: Insertion", 6)
        pyxel.text(x_pos, y_pos + 10, "2: Selection", 5)
        pyxel.text(x_pos, y_pos + 20, "3: Bulles", 4)
        pyxel.text(10, Size[1] - 10, f"Mode: {display_mode}", 7)

        # Afficher le mode d'affichage courant
        pyxel.text(10, Size[1]-10, f"Mode: {display_mode}", 7)
    else:
        
        # Dessiner le tableau selon le mode d'affichage choisi
        if display_mode == "colonne":
            for i in range(len(tab)):
                v = tab[i]
                pyxel.rect(i * bar_width, Size[1] - v, bar_width - 1, v, 11)

        else:  # mode "point"
            for i in range(len(tab)):
                v = tab[i]
                # Dessiner un point au milieu de la "colonne"

                pyxel.circ(i * bar_width , Size[1] - v, 3,11) # affiche le ressource sur l'écran dépuis sa donné

        if status == "attente":
            pyxel.text(10, 10, "Appuyer sur ESPACE", 7)
            
        elif status == "done":
            pyxel.text(10, 20, "Appuyer R pour reset", 8)
            pyxel.text(10, 10, f"Temps : {temps_écoulé:.2f} s", 8)

        
    
### Initialisation ###  
pyxel.init(Size[0], Size[1], title="Tri Visualisation")
algoritmes = {"1": insertion, "2": selection, "3": tri_bulle } 
pyxel.run(update, draw)

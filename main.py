import tkinter as tk

# --- Fonctions principales ---

def creation_matrice_transition(nb_pieces, portes):
    # je crée une matrice nb_pieces x nb_pieces avec que des zéros
    T = []
    for i in range(nb_pieces):
        ligne = []
        for j in range(nb_pieces):
            ligne.append(0)  # remplir avec des zéros
        T.append(ligne)

    # je remplis avec les largeurs des portes
    for (i,j) in portes:
        largeur = portes[(i,j)]
        T[i][j] = largeur
        T[j][i] = largeur  # symétrie

    # normalisation pour que chaque ligne fasse 1
    for i in range(nb_pieces):
        s = 0
        for j in range(nb_pieces):
            s = s + T[i][j]
        if s>0:
            for j in range(nb_pieces):
                T[i][j] = T[i][j]/s
        else:
            T[i][i] = 1  # si pas de porte, on reste sur place
    return T

def evolution_presence(T, V0, k=None, precision=1e-6, max_iter=1000):
    """
    T = matrice de transition
    V0 = état initial
    k = nombre d’itérations (None pour vecteur stationnaire)
    Retourne : le vecteur final et le nombre d'itérations effectuées
    """
    n = len(T)
    V = []
    for v in V0:
        V.append(float(v))

    if k is not None:
        # --- mode itérations fixes ---
        for iter_count in range(k):
            V_new = []
            for i in range(n):
                s = 0
                for j in range(n):
                    s = s + V[j]*T[j][i]
                V_new.append(s)
            V = V_new
        return V, k
    else:
        # --- mode méthode de la puissance ---
        q_old = 0
        for iter_count in range(max_iter):
            # produit matrice * vecteur
            Y = []
            for i in range(n):
                s = 0
                for j in range(n):
                    s = s + V[j]*T[j][i]
                Y.append(s)
            # normalisation
            total = 0
            for val in Y:
                total = total + val
            if total == 0:
                total = 1
            for i in range(n):
                V[i] = Y[i]/total
            # calcul valeur propre
            TV = []
            for i in range(n):
                s = 0
                for j in range(n):
                    s = s + T[i][j]*V[j]
                TV.append(s)
            q = 0
            for i in range(n):
                q = q + V[i]*TV[i]
            # critère de Cauchy
            if abs(q - q_old) < precision and iter_count > 0:
                return V, iter_count
            q_old = q
        return V, iter_count, q

# --- Données ---
nb_pieces = 5
portes_base = { (0,1):100, (0,3):70, (1,2):120, (3,4):70, (4,2):50 }
portes_oscillation = { (0,1):1, (1,2):1, (2,3):1, (3,0):1 }
portes_rupture = {(0,1):1,
                   (1,2):1,
                   (2,3):1,
                   (3,0):1,
                   (0,2):1,
                   (3,4):1 }


# création des matrices
T_base = creation_matrice_transition(nb_pieces, portes_base)
T_oscillation = creation_matrice_transition(4, portes_oscillation)
T_rupture = creation_matrice_transition(5, portes_rupture)

V0_base = [1,0,0,0,0]
V0_oscillation = [1,0,0,0]

print("\nMatrice de transition du probleme initial :\n")#on ne print que la matrice du probleme
for ligne in T_base:
    print(ligne)

print("\nMatrice de transition (rupture): \n")
for ligne in T_oscillation:
    print(ligne)

print("\nMatrice de transition (oscillation) : \n")
for ligne in T_rupture:
    print(ligne)

evolution_base_cauchy = evolution_presence(T_base, V0_base, k=None, precision=1e-6, max_iter=1000)
evolution_base_iteration = evolution_presence(T_base, V0_base, k=50, precision=1e-6, max_iter=1000)
evolution_rupture_cauchy = evolution_presence(T_rupture, V0_base, k=None, precision=1e-6, max_iter=1000)
evolution_oscillation_cauchy = evolution_presence(T_oscillation, V0_base, k=None, precision=1e-6, max_iter=1000)

print("\n vecteur propre de la situation de base par cauchy et le nombre d'iteration necessaire : ")
print(evolution_base_cauchy)
print("\nvecteur propre de la situation de base par iteration et le nombre d'iteration : ")
print(evolution_base_iteration)
print("\nvecteur propre de la situation (rupture) par cauchy et le nombre d'iteration necessaire: ")
print(evolution_rupture_cauchy)
print("\nvecteur propre de la situation (oscillation) par cauchy et le nombre d'iteration necessaire: ")
print(evolution_oscillation_cauchy)
print("\n")


# --- Interface graphique simple ---
root = tk.Tk()
root.title("Répartition de probabilité")

canvas = tk.Canvas(root, width=500, height=250)
canvas.pack()

# positions simples pour les cercles
positions_base = [(50,100),(150,100),(250,100),(350,100),(450,100)]
positions_osc = [(50,100),(150,100),(250,100),(350,100)]

V_current = list(V0_base)
T_current = T_base
positions_current = positions_base

def dessiner():
    canvas.delete("all")
    # dessiner les cercles
    for i in range(len(V_current)):
        x, y = positions_current[i]
        rayon = int(V_current[i]*50)+10
        canvas.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, fill="blue")
        canvas.create_text(x, y, text=f"{V_current[i]:.2f}", fill="white")
    # légende simple
    canvas.create_text(250, 220, text="Flèche → : itération | 1 : base | 2 : rupture | 3 : oscillation | 0 : vecteur stationnaire", fill="black")

def iteration(k=None):
    global V_current
    V_current, k_effectif = evolution_presence(T_current, V_current, k)
    dessiner()
    print(f"Répartition après {k_effectif} itérations :", V_current)

def changer_mode(mode):
    global T_current, V_current, positions_current
    if mode=="base":
        T_current = T_base
        V_current = list(V0_base)
        positions_current = positions_base
    elif mode=="rupture":
        T_current = T_rupture
        V_current = list(V0_base)
        positions_current = positions_base
    elif mode=="oscillation":
        T_current = T_oscillation
        V_current = list(V0_oscillation)
        positions_current = positions_osc
    dessiner()

# --- Contrôles clavier ---
def key_press(event):
    if event.keysym=="Right":
        iteration(k=1)  # avance d'une itération
    elif event.keysym=="1":
        changer_mode("base")
    elif event.keysym=="2":
        changer_mode("rupture")
    elif event.keysym=="3":
        changer_mode("oscillation")
    elif event.keysym=="0":
        iteration(k=None)  # méthode de la puissance

root.bind("<Key>", key_press)

# dessin initial
dessiner()

root.mainloop()

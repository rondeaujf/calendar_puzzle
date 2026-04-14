import sys
import random

# Empêche PyCSP3 de lire les arguments de Gunicorn au démarrage
sys.argv = ['app.py']

from flask import Flask, render_template, request, redirect
from pycsp3 import *

app = Flask(__name__)

# Couleurs pour les 8 pièces
COLORS = {
    'A': 'bg-red-400', 'B': 'bg-blue-400', 'C': 'bg-green-400', 'D': 'bg-yellow-400',
    'E': 'bg-purple-400', 'F': 'bg-orange-400', 'G': 'bg-pink-400', 'H': 'bg-teal-400',
    'TARGET': 'bg-gray-800 text-white font-bold',
    'EMPTY': 'bg-transparent border-none'
}

def solve_calendar(mois_cible, jour_cible):
    clear()  # Réinitialise l'instance PyCSP3 [cite: 5880]

    # Disposition du plateau Genius Crafts
    month_map = {
        "JAN": (0, 0), "FEB": (0, 1), "MAR": (0, 2), "APR": (0, 3), "MAY": (0, 4), "JUN": (0, 5),
        "JUL": (1, 0), "AUG": (1, 1), "SEP": (1, 2), "OCT": (1, 3), "NOV": (1, 4), "DEC": (1, 5)
    }
    day_map = {str(d): (2 + (d - 1) // 7, (d - 1) % 7) for d in range(1, 32)}

    board_coords = list(month_map.values()) + list(day_map.values())
    target_cells = {month_map[mois_cible], day_map[jour_cible]}
    active_cells = [cell for cell in board_coords if cell not in target_cells]
    
    # Définition des pièces en respectant vos formes
    pieces = [
        [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)], # A: La grosse pièce (Hexomino 2x3)
        [(0,0), (0,1), (0,2), (1,0), (1,2)],        # B: Pièce en U
        [(0,0), (1,0), (2,0), (3,0), (3,1)],        # C: Pièce en L (long)
        [(0,0), (1,0), (2,0), (2,1), (2,2)],        # D: Pièce en V (coin 3x3)
        [(0,0), (1,0), (1,1), (1,2), (2,2)],        # E: Pièce en Z (escalier)
        [(0,0), (0,1), (0,2), (0,3), (1,1)],        # F: LA PIÈCE F
        [(0,0), (0,1), (1,0), (1,1), (1,2)],        # G: Pièce en P (bloc compact)
        [(0,0), (0,1), (0,2), (1,2), (1,3)]         # H: Pièce en Y (ou T allongé)
    ]

    def get_orientations(piece):
        orientations = set()
        for flip in [False, True]:
            p = [(r, c) for r, c in piece]
            if flip: p = [(r, -c) for r, c in p]
            for _ in range(4):
                p = [(c, -r) for r, c in p]
                min_r, min_c = min(r for r, c in p), min(c for r, c in p)
                norm_p = tuple(sorted((r - min_r, c - min_c) for r, c in p))
                orientations.add(norm_p)
        return list(orientations)

    # Calcul des placements possibles
    T = [[] for _ in range(len(pieces))]
    for i, piece in enumerate(pieces):
        for orient in get_orientations(piece):
            for r in range(7):
                for c in range(7):
                    placement = [(r + dr, c + dc) for dr, dc in orient]
                    if all(cell in active_cells for cell in placement):
                        bool_tuple = tuple(1 if cell in placement else 0 for cell in active_cells)
                        T[i].append(bool_tuple)

    if any(not t for t in T): 
        return None 

    # Mélange des domaines pour la diversification de la recherche [cite: 4148, 4775]
    for i in range(len(pieces)):
        random.shuffle(T[i])

    # Modélisation CSP [cite: 5374, 5951]
    B = VarArray(size=[len(pieces), len(active_cells)], dom={0, 1})
    for i in range(len(pieces)): 
        satisfy(B[i] in T[i]) # Contrainte d'extension [cite: 5487, 5707]
    
    for j in range(len(active_cells)): 
        satisfy(Sum(B[i][j] for i in range(len(pieces))) == 1) # Contrainte de somme [cite: 5667, 7120]

    # On définit une graine aléatoire pour Python et le solveur
    graine = random.randint(0, 1000000)

    # Résolution avec options de diversification :
    # 1. -seed : définit la graine du solveur Java
    # 2. -valh=Rand : force le choix aléatoire des valeurs (placements de pièces)
    if solve(options=f"-seed={graine} -valh=Rand") is SAT:
        grid = [[{'color': COLORS['EMPTY'], 'text': ''} for _ in range(7)] for _ in range(7)]
        r_m, c_m = month_map[mois_cible]
        r_d, c_d = day_map[jour_cible]
        grid[r_m][c_m] = {'color': COLORS['TARGET'], 'text': mois_cible}
        grid[r_d][c_d] = {'color': COLORS['TARGET'], 'text': jour_cible}

        chars = "ABCDEFGH"
        for i in range(len(pieces)):
            for j in range(len(active_cells)):
                if value(B[i][j]) == 1:
                    r, c = active_cells[j]
                    grid[r][c] = {'color': COLORS[chars[i]], 'text': chars[i]}
        return grid
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    grid = None
    error = None
    selected_month = "JAN"
    selected_day = "1"
    if request.method == 'POST':
        selected_month = request.form.get('month')
        selected_day = request.form.get('day')
        grid = solve_calendar(selected_month, selected_day)
        if not grid:
            error = "Désolé, aucune solution n'a été trouvée pour cette date."

    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    days = [str(i) for i in range(1, 32)]
    return render_template('index.html', grid=grid, error=error, months=months, days=days, 
                           selected_month=selected_month, selected_day=selected_day)

@app.route('/reset')
def reset():
    return redirect('/')

if __name__ == '__main__':
    # Configuration pour Render
    app.run(host='0.0.0.0', port=10000)

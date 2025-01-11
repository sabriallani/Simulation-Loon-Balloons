import streamlit as st
import math

# ================================
# Étape 1: Interface utilisateur pour le chargement des données
# ================================
st.title("Simulation Loon Balloons")
st.write("Planifiez les trajectoires des ballons pour maximiser la couverture Internet !")

uploaded_file = st.file_uploader("Téléchargez le fichier d'entrée", type=["txt"])

if uploaded_file:
    # Lire et afficher le contenu du fichier
    input_data = uploaded_file.read().decode("utf-8").splitlines()
    st.text("Fichier chargé avec succès !")

    # Parsez les données d'entrée
    # Première ligne : R, C, A
    R, C, A = map(int, input_data[0].split())
    st.write(f"Grille : {R}x{C}, Altitudes : {A}")

    # Deuxième ligne : L, V, B, T
    L, V, B, T = map(int, input_data[1].split())
    st.write(f"Cibles : {L}, Rayon de couverture : {V}, Ballons : {B}, Tours : {T}")

    # Troisième ligne : Position de départ des ballons
    start_row, start_col = map(int, input_data[2].split())
    st.write(f"Position de départ : ({start_row}, {start_col})")

    # Lignes suivantes : Positions des cibles
    target_cells = []
    for i in range(3, 3 + L):
        try:
            line = input_data[i].split()
            if len(line) != 2:
                raise ValueError(f"Ligne incorrecte pour une cible : {line}")
            r, c = map(int, line)
            target_cells.append((r, c))
        except ValueError as e:
            st.error(f"Erreur de format dans la ligne des cibles : {e}")
            st.stop()

    st.write(f"Cibles : {target_cells}")

    # Grilles de vent
    wind_grids = []
    for altitude in range(A):
        wind_grid = []
        start_idx = 3 + L + altitude * R
        for row in range(R):
            if start_idx + row >= len(input_data):
                st.error(f"Les données de vent sont incomplètes pour l'altitude {altitude + 1}.")
                st.stop()
            line = input_data[start_idx + row].split()
            if len(line) % 2 != 0:
                st.error(f"Ligne incorrecte dans les grilles de vent : {line}")
                st.stop()
            wind_row = []
            for j in range(0, len(line), 2):
                delta_r, delta_c = map(int, line[j:j+2])
                wind_row.append((delta_r, delta_c))
            wind_grid.append(wind_row)
        wind_grids.append(wind_grid)
    st.write(f"Grilles de vent chargées pour {A} altitudes.")

    # ================================
    # Étape 2: Initialisation de la simulation
    # ================================
    balloons = [{"row": start_row, "col": start_col, "altitude": 0, "lost": False} for _ in range(B)]

    def display_grid(balloons, target_cells, R, C):
        """Affichage textuel de la grille."""
        grid = [["." for _ in range(C)] for _ in range(R)]
        for r, c in target_cells:
            grid[r][c] = "T"  # Marquer les cibles
        for b in balloons:
            if not b["lost"]:
                grid[b["row"]][b["col"]] = "B"  # Marquer les ballons
        return "\n".join("".join(row) for row in grid)

    def calculate_coverage(balloons):
        """Calculer les cibles couvertes par les ballons."""
        covered = set()
        for balloon in balloons:
            if balloon["lost"] or balloon["altitude"] == 0:
                continue
            r, c = balloon["row"], balloon["col"]
            for target in target_cells:
                tr, tc = target
                col_dist = min(abs(tc - c), C - abs(tc - c))  # Grille cyclique pour les colonnes
                if math.sqrt((tr - r) ** 2 + col_dist ** 2) <= V:
                    covered.add(target)
        return len(covered)

    def best_move(balloons, target_cells, wind_grids, R, C, A):
        """Trouver le meilleur mouvement pour maximiser la couverture."""
        for b in balloons:
            if b["lost"]:
                continue
            best_score = -1
            best_adjustment = 0

            for adjustment in [-1, 0, 1]:
                new_altitude = b["altitude"] + adjustment
                if new_altitude < 1 or new_altitude > A:
                    continue

                wind = wind_grids[new_altitude - 1][b["row"]][b["col"]]
                new_row = b["row"] + wind[0]
                new_col = (b["col"] + wind[1]) % C

                if new_row < 0 or new_row >= R:
                    continue

                score = sum(
                    1 for tr, tc in target_cells
                    if abs(tr - new_row) + min(abs(tc - new_col), C - abs(tc - new_col)) <= V
                )
                if score > best_score:
                    best_score = score
                    best_adjustment = adjustment

            b["altitude"] += best_adjustment

    for t in range(T):
        st.write(f"#### Tour {t+1}")
        best_move(balloons, target_cells, wind_grids, R, C, A)
        st.write(display_grid(balloons, target_cells, R, C))
        score = calculate_coverage(balloons)
        st.write(f"Score pour ce tour : {score}")

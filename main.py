import streamlit as st
import math
import matplotlib.pyplot as plt

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
    simulation_data = []

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

    def move_balloons(balloons, adjustments):
        """Déplacer les ballons en fonction des ajustements d'altitude."""
        for i, adjustment in enumerate(adjustments):
            if balloons[i]["lost"]:
                continue

            # Ajuster l'altitude
            new_altitude = balloons[i]["altitude"] + adjustment
            if new_altitude < 1 or new_altitude > A:
                balloons[i]["lost"] = True
                continue

            balloons[i]["altitude"] = new_altitude

            # Calculer la nouvelle position en fonction du vent
            current_altitude = new_altitude - 1  # Index 0-based
            delta_r, delta_c = wind_grids[current_altitude][balloons[i]["row"]][balloons[i]["col"]]
            new_row = balloons[i]["row"] + delta_r
            new_col = (balloons[i]["col"] + delta_c) % C

            # Vérifier si le ballon est perdu
            if new_row < 0 or new_row >= R:
                balloons[i]["lost"] = True
            else:
                balloons[i]["row"] = new_row
                balloons[i]["col"] = new_col

    # ================================
    # Étape 3: Simulation
    # ================================
    st.write("### Simulation")
    total_score = 0

    for t in range(T):
        st.write(f"#### Tour {t+1}")

        # Récupérer les ajustements de l'utilisateur
        adjustments = []
        for b in range(B):
            adjustment = st.number_input(f"Ajustement d'altitude pour le ballon {b+1} au tour {t+1}", -1, 1, 0)
            adjustments.append(adjustment)

        # Déplacer les ballons
        move_balloons(balloons, adjustments)

        # Calculer la couverture
        score = calculate_coverage(balloons)
        total_score += score

        # Enregistrer les données de simulation
        simulation_data.append({
            "tour": t + 1,
            "positions": [(b["row"], b["col"]) for b in balloons],
            "score": score,
            "total_score": total_score
        })

        st.write(f"Score pour ce tour : {score}")
        st.write(f"Score total : {total_score}")

    # Afficher les résultats sous forme de tableau
    st.write("### Résultats de la simulation")
    results_table = ""
    results_table += "| Tour | Positions | Score | Total Score |\n"
    results_table += "|------|-----------|-------|-------------|\n"
    for data in simulation_data:
        positions_str = ", ".join([f"({r}, {c})" for r, c in data["positions"]])
        results_table += f"| {data['tour']} | {positions_str} | {data['score']} | {data['total_score']} |\n"

    st.markdown(f"```{results_table}```")

    # Visualisation des positions des ballons
    st.write("### Visualisation des positions des ballons")
    for t, data in enumerate(simulation_data):
        fig, ax = plt.subplots()
        grid = [[0 for _ in range(C)] for _ in range(R)]
        for target in target_cells:
            grid[target[0]][target[1]] = -1  # Indiquer les cibles
        for pos in data["positions"]:
            grid[pos[0]][pos[1]] = 1  # Position des ballons
        ax.imshow(grid, cmap="coolwarm", interpolation="none")
        ax.set_title(f"Tour {t+1}")
        st.pyplot(fig)

    st.write(f"### Score final : {total_score}")

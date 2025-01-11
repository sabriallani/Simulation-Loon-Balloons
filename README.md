# Simulation Loon Balloons

This repository contains a Streamlit application that simulates the coordination of balloons to maximize internet coverage in specified areas. The project is inspired by the idea of using high-altitude balloons for providing internet access in remote regions.

## Features

- **Interactive Simulation**: Adjust the altitude of balloons in real-time and observe their movements.
- **Dynamic Visualizations**: Visualize balloon positions and target coverage on a grid.
- **Simulation Metrics**: View scores and results for each simulation step.
- **Error Validation**: Ensures the input file is correctly formatted before starting the simulation.

---

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.8 or later
- Required Python libraries:
  - `streamlit`
  - `matplotlib`

Install dependencies with:

```bash
pip install streamlit matplotlib
```

### Running the Application

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Launch the Streamlit application:

   ```bash
   streamlit run app.py
   ```

3. Open the application in your browser and upload a properly formatted input file.

---

## Input File Format

The input file must be a plain text file with the following structure:

1. **Grid Dimensions and Altitudes**:
   ```
   R C A
   ```
   - `R`: Number of rows in the grid.
   - `C`: Number of columns in the grid.
   - `A`: Number of altitudes.

2. **Simulation Parameters**:
   ```
   L V B T
   ```
   - `L`: Number of target cells.
   - `V`: Coverage radius.
   - `B`: Number of balloons.
   - `T`: Number of simulation turns.

3. **Starting Position**:
   ```
   rs cs
   ```
   - `rs`, `cs`: Row and column of the starting position for the balloons.

4. **Target Cells**:
   Each target cell is described by its row and column:
   ```
   r1 c1
   r2 c2
   ...
   ```

5. **Wind Grids**:
   Each altitude has `R` rows, and each row has `C` pairs of wind vectors `(Δr, Δc)`:
   ```
   Δr1 Δc1 Δr2 Δc2 ... ΔrC ΔcC
   ```

### Example Input File

```txt
3 5 3
2 1 1 5
1 2
0 2
0 4
0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1
-1 0 -1 0 -1 0 -1 0 -1 0
-1 0 -1 0 -1 0 -1 0 -1 0
-1 0 -1 0 -1 0 -1 0 -1 0
0 1 0 1 0 1 0 2 0 1
0 2 0 1 0 2 0 3 0 2
0 1 0 1 0 1 0 2 0 1
```

---

## How It Works

1. **Upload Input File**:
   Upload the input file to initialize the simulation.

2. **Interactive Control**:
   Adjust the altitude of each balloon at every turn.

3. **Visualization**:
   - Balloon positions and target coverage are displayed on a grid.
   - Real-time updates for scores and simulation data.

4. **Results**:
   - Final score and detailed results are shown at the end of the simulation.

---

## Example Output

- **Simulation Steps**:
  - View scores for each step and the total score dynamically.

- **Grid Visualization**:
  - Balloons (indicated by positions) and targets are clearly marked.

---

## Contributing

If you'd like to contribute, feel free to fork the repository and submit a pull request.

---

## License

This project is licensed under the MIT License.

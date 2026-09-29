# Warburg Effect Tumor Metabolism Simulator

A small Python simulation that compares the energy production and lactate secretion of a normal healthy cell with those of a malignant tumor cell. The model illustrates the **Warburg effect**: the tendency of many tumor cells to favor glycolysis and produce lactate even when oxygen is available.

> **Important:** This is an educational, simplified model—not a clinical, diagnostic, or quantitatively validated biological simulator.

## Relevance to Tumors

Healthy cells generally use oxygen-dependent oxidative phosphorylation when oxygen is available. In this simulation, that pathway produces **36 ATP per unit of glucose** and only a small amount of lactate.

The tumor-cell model represents aerobic glycolysis, commonly associated with the Warburg effect. It uses glucose at a higher default rate, produces **2 ATP per unit of glucose**, and secretes more lactate. This demonstrates two important ideas:

- **High glucose consumption:** Tumor cells may consume substantial amounts of glucose to support rapid growth and biosynthetic activity.
- **Lactate production despite oxygen:** Tumor cells can convert glucose to lactate even in an oxygenated environment, contributing to an acidic tumor microenvironment.
- **Different energy strategy:** Glycolysis generates less ATP per glucose molecule, but it can provide metabolic intermediates and support rapid energy production under conditions relevant to tumor growth.

The simulation does not claim that every tumor behaves identically. Tumor metabolism varies according to tumor type, genetics, oxygen availability, nutrient supply, and the surrounding microenvironment.

## What the Program Does

When run, the program:

1. Displays the simulator title.
2. Requests three values from the user:
   - Baseline glucose intake for a healthy cell.
   - Elevated glucose intake for a tumor cell.
   - Simulation duration in hours.
3. Uses defaults when the user submits an empty response:
   - Healthy-cell glucose intake: `1.0` unit/hour.
   - Tumor-cell glucose intake: `10.0` units/hour.
   - Duration: `24` hours.
4. Validates the values and restores safe defaults if the input is invalid.
5. Creates one `NormalCell` and one `TumorCell` object.
6. Simulates an oxygenated tissue environment.
7. Runs metabolism once for each cell during every simulated hour.
8. Prints cumulative ATP production and lactate secretion for both cells.

## Model Assumptions and Equations

### Shared cell state

Every cell stores:

- `cell_type`: A human-readable cell name.
- `glucose_intake`: Glucose consumed per hour.
- `total_atp_produced`: Cumulative ATP generated during the simulation.
- `total_lactate_produced`: Cumulative lactate secreted during the simulation.

### Normal cell with oxygen

For each hour:

```text
ATP per hour = glucose intake × 36
Lactate per hour = glucose intake × 0.1
```

### Normal cell without oxygen

For each hour:

```text
ATP per hour = glucose intake × 2
Lactate per hour = glucose intake × 2
```

### Tumor cell

The tumor-cell model uses glycolysis regardless of the `oxygen_available` value:

```text
ATP per hour = glucose intake × 2
Lactate per hour = glucose intake × 2.5
```

### Cumulative totals

For a constant glucose-intake rate and a simulation lasting `H` hours:

```text
Total ATP = ATP per hour × H
Total lactate = Lactate per hour × H
```

## Example Run

Running the program with all default values gives the following expected totals after 24 hours:

| Cell | Glucose rate | ATP/hour | Total ATP | Lactate/hour | Total lactate |
|---|---:|---:|---:|---:|---:|
| Normal healthy cell | 1.0 | 36.0 | 864.0 | 0.1 | 2.4 |
| Malignant tumor cell | 10.0 | 20.0 | 480.0 | 25.0 | 600.0 |

The tumor cell produces less ATP in this simplified model, but consumes much more glucose and secretes dramatically more lactate. That contrast is the main educational result of the program.

## Program Structure

### `Cell`

The base class contains shared properties and the `display_status()` method used to print a summary.

### `NormalCell`

A subclass representing a healthy cell. Its `metabolize()` method changes its ATP and lactate output depending on whether oxygen is available.

### `TumorCell`

A subclass representing a malignant tumor cell. Its `metabolize()` method models preferential glycolysis and ignores oxygen availability in the current simplified implementation.

### Main execution block

The code under `if __name__ == "__main__":` makes the file executable as a command-line program while preventing the interactive simulation from running automatically when the classes are imported into another Python file.

## Steps Used to Create the Simulation

1. **Define a shared abstraction:** A `Cell` base class was created to hold data common to all cell types.
2. **Add measurable outputs:** ATP and lactate totals were initialized to zero so that results could accumulate over time.
3. **Model healthy metabolism:** `NormalCell` was given separate aerobic and anaerobic behaviors.
4. **Model tumor metabolism:** `TumorCell` was configured to favor glycolysis and produce additional lactate.
5. **Add user-controlled parameters:** The program accepts glucose rates and simulation duration at runtime.
6. **Add input validation:** Negative glucose values and non-positive durations are rejected; malformed entries are caught with `ValueError`.
7. **Provide biological defaults:** Default values make the program easy to run without requiring the user to enter every value.
8. **Create a time loop:** The simulation calls each cell's metabolism method once per hour.
9. **Accumulate and report results:** Each cell records its totals and prints a formatted summary at the end.
10. **Make the script reusable:** The main execution guard allows the cell classes to be imported into tests or future simulations.

## Running the Program

From the repository root, run:

```bash
python WarbugFlux-sim/main.py
```

Depending on your system, you may need to use:

```bash
python3 WarbugFlux-sim/main.py
```

Press **Enter** at any prompt to use its default value. For example:

```text
Enter baseline glucose intake for Healthy Cell (default is 1.0):
Enter elevated glucose intake for Tumor Cell (default is 10.0):
Enter the duration of the simulation in hours (e.g., 24):
```

You can also provide custom values, such as `2`, `8`, and `12`, to compare the cells over 12 hours.

## Input Handling

The program accepts:

- Non-negative floating-point glucose rates, such as `1`, `2.5`, or `10.0`.
- A positive integer number of hours.

If the user enters text that cannot be converted to the expected numeric type, a negative glucose value, or zero/negative hours, the program prints an error and resets all values to the defaults.

One limitation is that the validation currently allows special floating-point values such as `nan` or `inf` in some Python environments. A production-quality scientific model should explicitly reject non-finite values with `math.isfinite()`.

## Limitations

This simulation is intentionally simple. It does not model:

- Individual glycolysis reactions or mitochondrial pathways.
- ATP use, cell division, biomass production, or cell death.
- Oxygen depletion over time.
- Glucose availability or competition between cells.
- Acid buffering, lactate transport, or blood-vessel supply.
- Differences among tumor types or individual patient tumors.
- Dynamic changes in metabolism in response to hypoxia or treatment.
- Experimentally calibrated units or clinical measurements.

The numerical values are illustrative assumptions chosen to make the contrast visible. They should not be interpreted as universal biological constants.

## Possible Extensions

Future versions could add:

- A changing oxygen level and hypoxia threshold.
- Glucose and oxygen resource pools shared by multiple cells.
- A population of cells rather than one cell of each type.
- Cell growth based on ATP and available nutrients.
- Graphs showing ATP and lactate over time.
- CSV or JSON export for analysis.
- Unit tests for metabolism, validation, and cumulative totals.
- Configurable metabolic rates instead of hard-coded coefficients.
- A comparison of treatment scenarios, such as glycolysis inhibitors or oxygen therapy.

## Educational Takeaway

The program demonstrates that metabolic efficiency and metabolic behavior are not the same thing. In the model, the healthy cell generates more ATP per glucose molecule in oxygenated conditions, while the tumor cell consumes more glucose and releases much more lactate through glycolysis. This simplified trade-off helps explain why altered glucose metabolism and lactate accumulation are important features when studying tumor biology.

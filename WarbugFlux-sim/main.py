class Cell:
    def __init__(self, cell_type: str, glucose_intake_rate: float):
        self.cell_type = cell_type
        self.glucose_intake = glucose_intake_rate  # units per hour
        self.total_atp_produced = 0.0
        self.total_lactate_produced = 0.0

    def display_status(self, hours: int):
        print(f"\n--- {self.cell_type.upper()} SUMMARY ({hours} Hours) ---")
        print(f"Glucose Intake Rate: {self.glucose_intake} units/hr")
        print(f"Total ATP (Energy) Generated: {self.total_atp_produced:,.2f} units")
        print(f"Total Lactate (Acid) Secreted: {self.total_lactate_produced:,.2f} units")


class NormalCell(Cell):
    def __init__(self, glucose_rate: float):
        # Normal cells initialized with user-defined or default glucose rate
        super().__init__(cell_type="Normal Healthy Cell", glucose_intake_rate=glucose_rate)

    def metabolize(self, oxygen_available: bool):
        if oxygen_available:
            # Efficient: Oxidative Phosphorylation (36 ATP per 1 glucose)
            atp_per_hr = self.glucose_intake * 36
            lactate_per_hr = self.glucose_intake * 0.1
        else:
            # Anaerobic Glycolysis due to lack of oxygen (2 ATP per 1 glucose)
            atp_per_hr = self.glucose_intake * 2
            lactate_per_hr = self.glucose_intake * 2
        
        # Accumulate metrics
        self.total_atp_produced += atp_per_hr
        self.total_lactate_produced += lactate_per_hr


class TumorCell(Cell):
    def __init__(self, glucose_rate: float):
        # Tumor cells initialized with user-defined elevated glucose rate
        super().__init__(cell_type="Malignant Tumor Cell", glucose_intake_rate=glucose_rate)

    def metabolize(self, oxygen_available: bool):
        # THE WARBURG EFFECT: Regardless of oxygen availability, 
        # tumor cells predominantly perform glycolysis (2 ATP per glucose)
        atp_per_hr = self.glucose_intake * 2
        lactate_per_hr = self.glucose_intake * 2.5
        
        # Accumulate metrics
        self.total_atp_produced += atp_per_hr
        self.total_lactate_produced += lactate_per_hr


# ==========================================
# ADVANCED SIMULATION EXECUTION
# ==========================================
if __name__ == "__main__":
    print("--- Tumor Metabolism & Warburg Effect Simulator ---\n")

    # 1. Error Handling for Dynamic Runtime User Inputs
    try:
        healthy_glucose = float(input("Enter baseline glucose intake for Healthy Cell (default is 1.0): ") or 1.0)
        tumor_glucose = float(input("Enter elevated glucose intake for Tumor Cell (default is 10.0): ") or 10.0)
        simulation_hours = int(input("Enter the duration of the simulation in hours (e.g., 24): ") or 24)
        
        # Validate against mathematically or biologically impossible values
        if healthy_glucose < 0 or tumor_glucose < 0 or simulation_hours <= 0:
            raise ValueError("Values cannot be negative, and simulation hours must be greater than zero.")
            
    except ValueError as e:
        print(f"\n[Input Error]: Invalid entry. Details: {e}")
        print("Resetting to safe biological defaults: Healthy=1.0, Tumor=10.0, Hours=24.")
        healthy_glucose = 1.0
        tumor_glucose = 10.0
        simulation_hours = 24

    # 2. Instantiate cells with validated parameters
    healthy_cell = NormalCell(glucose_rate=healthy_glucose)
    cancer_cell = TumorCell(glucose_rate=tumor_glucose)

    # 3. Simulate oxygenated environment state
    oxygen_present = True
    print(f"\nTissue Environment Status: Oxygen is Available -> Yes")
    print(f"Running simulation timeline loop for {simulation_hours} hours...")

    # 4. Multi-Hour Growth Loop
    for hour in range(1, simulation_hours + 1):
        healthy_cell.metabolize(oxygen_available=oxygen_present)
        cancer_cell.metabolize(oxygen_available=oxygen_present)

    # 5. Display cumulative metabolic impact
    healthy_cell.display_status(hours=simulation_hours)
    cancer_cell.display_status(hours=simulation_hours)

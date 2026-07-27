import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configure the modern theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
plt.style.use("dark_background")  # Make matplotlib match the dark theme


class ModernDiceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dice Probability Simulations")
        self.geometry("1100x700")  # Widened to fit the right sidebar

        # Configure grid layout (3 columns: Left Sidebar, Main Plot, Right Info)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # ==========================================
        # LEFT SIDEBAR: CONTROLS
        # ==========================================
        self.left_sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.left_sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.left_sidebar.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.left_sidebar, text="Simulations", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.scenario_label = ctk.CTkLabel(self.left_sidebar, text="Select Scenario:", font=ctk.CTkFont(size=14))
        self.scenario_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

        self.scenarios = [
            "1. Fair 6-Sided Dice",
            "2. Sum of Two Fair 6-Sided",
            "3. Sum of Two Fair 4-Sided",
            "4. Sum of Two Loaded 4-Sided",
            "5. Loaded 6-Sided (CDF)",
            "6. Condition: 2nd throw if <= 3",
            "7. Condition: 2nd throw if >= 3"
        ]

        self.scenario_dropdown = ctk.CTkOptionMenu(self.left_sidebar, values=self.scenarios, width=210)
        self.scenario_dropdown.grid(row=2, column=0, padx=20, pady=(10, 20))

        self.run_button = ctk.CTkButton(self.left_sidebar, text="Run Simulation", command=self.run_simulation,
                                        height=40)
        self.run_button.grid(row=3, column=0, padx=20, pady=10)

        # ==========================================
        # CENTER PANEL: PLOT & RESULTS
        # ==========================================
        self.plot_frame = ctk.CTkFrame(self, corner_radius=10)
        self.plot_frame.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="nsew")

        bg_color = "#2b2b2b"  # Seamless dark hex color
        self.fig, self.ax = plt.subplots(figsize=(6, 4), facecolor=bg_color)
        self.ax.set_facecolor(bg_color)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        self.results_frame = ctk.CTkFrame(self, corner_radius=10, height=120)
        self.results_frame.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="nsew")
        self.results_frame.grid_propagate(False)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)

        self.results_text = ctk.CTkTextbox(self.results_frame, font=ctk.CTkFont("Consolas", size=14), state="disabled")
        self.results_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # ==========================================
        # RIGHT SIDEBAR: PARAMETERS & NOTES
        # ==========================================
        self.right_sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.right_sidebar.grid(row=0, column=2, rowspan=2, sticky="nsew")
        self.right_sidebar.grid_rowconfigure(5, weight=1)

        self.param_label = ctk.CTkLabel(self.right_sidebar, text="Parameters & Notes",
                                        font=ctk.CTkFont(size=18, weight="bold"))
        self.param_label.grid(row=0, column=0, padx=20, pady=(30, 20))

        self.iter_label = ctk.CTkLabel(self.right_sidebar, text="Number of Iterations:", font=ctk.CTkFont(size=14))
        self.iter_label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")

        # Entry box allowing user to dynamically change array size
        self.iter_entry = ctk.CTkEntry(self.right_sidebar, width=210)
        self.iter_entry.insert(0, "10000")
        self.iter_entry.grid(row=2, column=0, padx=20, pady=(0, 20))

        self.notes_label = ctk.CTkLabel(self.right_sidebar, text="Logic Notes:", font=ctk.CTkFont(size=14))
        self.notes_label.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="w")

        self.notes_text = ctk.CTkTextbox(self.right_sidebar, width=210, height=350, font=ctk.CTkFont("Arial", size=13),
                                         wrap="word", state="disabled")
        self.notes_text.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")

        # Dictionary holding explanations for each scenario
        self.logic_notes = {
            "1. Fair 6-Sided Dice": "Uses np.random.choice() to generate uniform random throws.\n\nDemonstrates the baseline mean (~3.5) and variance (~2.9) of a fair 6-sided die over a large sample size.",
            "2. Sum of Two Fair 6-Sided": "Generates two independent arrays of throws and sums them.\n\nNotice how the distribution shifts from uniform to a triangular/bell-shape, illustrating the Central Limit Theorem.",
            "3. Sum of Two Fair 4-Sided": "Calculates the Covariance Matrix using np.cov(throw1, throw2).\n\nBecause the two dice throws are completely independent events, the covariance approaches 0.",
            "4. Sum of Two Loaded 4-Sided": "Injects bias using the 'p' parameter in np.random.choice().\n\nProbabilities are set to [0.2, 0.4, 0.2, 0.2], making the die twice as likely to land on '2'.",
            "5. Loaded 6-Sided (CDF)": "Plots the Cumulative Distribution Function (CDF) using matplotlib's ecdf().\n\nThe slope indicates probability density. Notice the steeper jump at heavily weighted values.",
            "6. Condition: 2nd throw if <= 3": "Uses Vectorization for performance.\n\nInstead of a slow Python for-loop, it uses np.where(throw1 <= 3, throw2, 0) to apply conditional logic instantly across the entire array.",
            "7. Condition: 2nd throw if >= 3": "Uses Vectorization for performance.\n\nApplies np.where(throw1 >= 3, throw2, 0). Changing the condition dramatically alters the probability mass function (PMF) distribution."
        }

    def display_results(self, text):
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("end", text)
        self.results_text.configure(state="disabled")

    def update_notes(self, scenario):
        self.notes_text.configure(state="normal")
        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("end", self.logic_notes.get(scenario, ""))
        self.notes_text.configure(state="disabled")

    def get_iterations(self):
        try:
            iters = int(self.iter_entry.get())
            return max(1, iters)  # Ensure at least 1 iteration
        except ValueError:
            self.iter_entry.delete(0, "end")
            self.iter_entry.insert(0, "10000")
            return 10000

    def run_simulation(self):
        selection = self.scenario_dropdown.get()
        self.update_notes(selection)
        iters = self.get_iterations()

        self.ax.clear()
        self.ax.grid(color='#444444', linestyle='--', linewidth=0.5, alpha=0.7)
        self.ax.set_axisbelow(True)

        if "1." in selection:
            self.simulate_fair_6_sided(iters)
        elif "2." in selection:
            self.simulate_two_fair_6_sided(iters)
        elif "3." in selection:
            self.simulate_two_fair_4_sided(iters)
        elif "4." in selection:
            self.simulate_loaded_4_sided(iters)
        elif "5." in selection:
            self.simulate_loaded_6_sided_cdf(iters)
        elif "6." in selection:
            self.simulate_conditional_throw_less_equal(iters)
        elif "7." in selection:
            self.simulate_conditional_throw_greater_equal(iters)

        self.canvas.draw()

    # ==========================================
    # SIMULATION LOGIC
    # ==========================================
    def simulate_fair_6_sided(self, iters):
        dice = [1, 2, 3, 4, 5, 6]
        throws = np.random.choice(dice, size=iters)
        mean, var = np.mean(throws), np.var(throws)

        self.ax.hist(throws, bins=np.arange(0.5, 7.5, 1), density=True, rwidth=0.8, edgecolor="white", color="#1f538d")
        self.ax.set_xticks(range(1, 7))
        self.ax.set_title(f"Probability Distribution ({iters:,} throws)", pad=15)
        self.display_results(f"Scenario: Single Fair 6-Sided Dice\nMean: {mean:.3f}\nVariance: {var:.3f}")

    def simulate_two_fair_6_sided(self, iters):
        dice = [1, 2, 3, 4, 5, 6]
        sums = np.random.choice(dice, size=iters) + np.random.choice(dice, size=iters)

        self.ax.hist(sums, bins=np.arange(1.5, 13.5), density=True, rwidth=0.8, edgecolor="white", color="#2ca02c")
        self.ax.set_xticks(range(2, 13))
        self.ax.set_title(f"Sum of Two 6-Sided Dice ({iters:,} throws)", pad=15)
        self.display_results(
            f"Scenario: Sum of Two Fair 6-Sided Dice\nMean of Sums: {np.mean(sums):.3f}\nVariance of Sums: {np.var(sums):.3f}")

    def simulate_two_fair_4_sided(self, iters):
        dice = [1, 2, 3, 4]
        throw1 = np.random.choice(dice, size=iters)
        throw2 = np.random.choice(dice, size=iters)
        sums = throw1 + throw2
        cov_matrix = np.cov(throw1, throw2)

        self.ax.hist(sums, bins=np.arange(1.5, 9.5), density=True, rwidth=0.8, edgecolor="white", color="#ff7f0e")
        self.ax.set_xticks(range(2, 9))
        self.ax.set_title(f"Sum of Two 4-Sided Dice ({iters:,} throws)", pad=15)
        self.display_results(
            f"Scenario: Sum of Two Fair 4-Sided Dice\nMean: {np.mean(sums):.3f} | Variance: {np.var(sums):.3f}\nCovariance [Throw 1, Throw 2]: {cov_matrix[0][1]:.5f}")

    def simulate_loaded_4_sided(self, iters):
        dice, probs = [1, 2, 3, 4], [0.2, 0.4, 0.2, 0.2]
        sums = np.random.choice(dice, p=probs, size=iters) + np.random.choice(dice, p=probs, size=iters)

        self.ax.hist(sums, bins=np.arange(1.5, 9.5), density=True, rwidth=0.8, edgecolor="white", color="#9467bd")
        self.ax.set_xticks(range(2, 9))
        self.ax.set_title(f"Sum of Two Loaded 4-Sided Dice ({iters:,} throws)", pad=15)
        self.display_results(
            f"Scenario: Loaded 4-Sided (P(2)=0.4)\nMean of Sums: {np.mean(sums):.3f}\nVariance of Sums: {np.var(sums):.3f}")

    def simulate_loaded_6_sided_cdf(self, iters):
        dice, probs = [1, 2, 3, 4, 5, 6], np.array([1 / 7, 1 / 7, 2 / 7, 1 / 7, 1 / 7, 1 / 7])
        sums = np.random.choice(dice, p=probs, size=iters) + np.random.choice(dice, p=probs, size=iters)

        self.ax.ecdf(sums, color="#17becf", linewidth=2)
        self.ax.set_title(f"CDF of Loaded 6-Sided Dice Sums ({iters:,} throws)", pad=15)
        self.ax.set_ylabel("Cumulative Probability")
        self.display_results(
            f"Scenario: Cumulative Distribution Function (Loaded 6-Sided)\nMean of Sums: {np.mean(sums):.3f}\nCurve reflects the heavy weighting on face '3'.")

    def simulate_conditional_throw_less_equal(self, iters):
        dice = [1, 2, 3, 4, 5, 6]
        throw1 = np.random.choice(dice, size=iters)
        throw2 = np.where(throw1 <= 3, np.random.choice(dice, size=iters), 0)
        sums = throw1 + throw2

        self.ax.hist(sums, bins=np.arange(0.5, 10.5, 1), density=True, rwidth=0.8, edgecolor="white", color="#bcbd22")
        self.ax.set_xticks(range(1, 10))
        self.ax.set_title(f"Conditional: 2nd throw if 1st <= 3 ({iters:,} throws)", pad=15)
        self.display_results(
            f"Scenario: Conditional Throw (First <= 3)\nMean of Sums: {np.mean(sums):.3f}\nVariance of Sums: {np.var(sums):.3f}")

    def simulate_conditional_throw_greater_equal(self, iters):
        dice = [1, 2, 3, 4, 5, 6]
        throw1 = np.random.choice(dice, size=iters)
        throw2 = np.where(throw1 >= 3, np.random.choice(dice, size=iters), 0)
        sums = throw1 + throw2

        self.ax.hist(sums, bins=np.arange(0.5, 13.5, 1), density=True, rwidth=0.8, edgecolor="white", color="#d62728")
        self.ax.set_xticks(range(1, 13))
        self.ax.set_title(f"Conditional: 2nd throw if 1st >= 3 ({iters:,} throws)", pad=15)
        self.display_results(
            f"Scenario: Conditional Throw (First >= 3)\nMean of Sums: {np.mean(sums):.3f}\nVariance of Sums: {np.var(sums):.3f}")


if __name__ == "__main__":
    app = ModernDiceApp()
    app.mainloop()
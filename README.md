# Dice Probability Simulations 🎲

An interactive Python dashboard built to visualize core probability and statistics concepts, highlighting the Law of Large Numbers, Central Limit Theorem, and conditional probability.

### Features
* **Modern UI:** Built using `customtkinter` for a clean, dark-mode interface.
* **Vectorized Logic:** Utilizes `numpy` arrays and `np.where()` for instant, loop-free mathematical simulations of tens of thousands of dice throws.
* **Data Visualization:** Integrates `matplotlib` directly into the GUI to render empirical histograms, covariance matrices, and Cumulative Distribution Functions (CDFs).

### Scenarios Simulated
1. Single Fair 6-Sided Dice (Mean & Variance)
2. Sum of Two Fair 6-Sided Dice (Central Limit Theorem)
3. Sum of Two Fair 4-Sided Dice (Covariance)
4. Sum of Two Loaded 4-Sided Dice (Weighted Probabilities)
5. Loaded 6-Sided Dice (CDF Plotting)
6. Conditional Throw: 2nd throw only if 1st <= 3
7. Conditional Throw: 2nd throw only if 1st >= 3

### How to Run
Ensure you have the required libraries installed:
`pip install numpy matplotlib customtkinter`

Run the application:
`python dice_simulation.py`
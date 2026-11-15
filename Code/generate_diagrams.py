"""
Generate high-resolution Methodology Block Diagram and Algorithm Flowchart
for inclusion in the Mini Project Report and Presentation.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_block_diagram(output_path: str):
    """Creates a professional block diagram of the system methodology."""
    fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
    ax.axis('off')
    
    blocks = [
        (0.03, 0.65, 0.16, 0.22, "1. Data Collection\n& Generation\n(1,500 Orders,\n7 Features)", "#DBEAFE", "#1D4ED8"),
        (0.23, 0.65, 0.16, 0.22, "2. Preprocessing\n& Scaling\n(StandardScaler\nScratch: z=(x-μ)/σ)", "#FEF3C7", "#D97706"),
        (0.43, 0.65, 0.16, 0.22, "3. Train-Test Split\n(80% Train: 1200\n20% Test: 300)", "#E0E7FF", "#4338CA"),
        (0.64, 0.76, 0.18, 0.18, "4A. Custom Scratch\nModel (NumPy)\n• Gradient Descent\n• Normal Equation", "#DCFCE7", "#15803D"),
        (0.64, 0.52, 0.18, 0.18, "4B. Benchmark\nModel (Sklearn)\n• LinearRegression\n• SGDRegressor", "#FCE7F3", "#BE185D"),
        (0.86, 0.64, 0.12, 0.25, "5. Evaluation\n& Analysis\n• All Parameters\n• Metrics (R², RMSE)\n• Diagnostics", "#F3E8FF", "#7E22CE"),
        (0.43, 0.12, 0.39, 0.22, "6. Interactive Web Frontend (Streamlit)\n• Live Predictor (Custom vs Sklearn)\n• Parameter & Metric Comparison Tables\n• Real-Time Diagnostic Visualizations", "#CCFBF1", "#0F766E")
    ]
    
    for x, y, w, h, text, bg, border in blocks:
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.015,rounding_size=0.02",
            facecolor=bg, edgecolor=border, linewidth=2.0
        )
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1E293B')

    arrow_props = dict(facecolor='#475569', edgecolor='#334155', width=1.5, headwidth=7, shrink=0.05)
    
    ax.annotate('', xy=(0.23, 0.76), xytext=(0.19, 0.76), arrowprops=arrow_props)
    ax.annotate('', xy=(0.43, 0.76), xytext=(0.39, 0.76), arrowprops=arrow_props)
    ax.annotate('', xy=(0.64, 0.85), xytext=(0.59, 0.78), arrowprops=arrow_props)
    ax.annotate('', xy=(0.64, 0.61), xytext=(0.59, 0.74), arrowprops=arrow_props)
    ax.annotate('', xy=(0.86, 0.79), xytext=(0.82, 0.83), arrowprops=arrow_props)
    ax.annotate('', xy=(0.86, 0.73), xytext=(0.82, 0.63), arrowprops=arrow_props)
    ax.annotate('', xy=(0.82, 0.23), xytext=(0.92, 0.64), arrowprops=arrow_props)

    plt.title("System Methodology & Architectural Block Diagram", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=250, bbox_inches='tight')
    plt.close()
    print(f"Generated Block Diagram at: {output_path}")

def generate_flowchart(output_path: str):
    """Creates a detailed flowchart of the Batch Gradient Descent optimization process."""
    fig, ax = plt.subplots(figsize=(8.5, 10.5), dpi=200)
    ax.axis('off')
    
    nodes = [
        (0.5, 0.94, "START", "oval", "#E2E8F0", "#475569"),
        (0.5, 0.83, "Initialize Parameters:\nWeights w = 0, Bias b = y_mean\nHyperparameters: α = 0.05, tol = 1e-8, max_iter = 3000", "box", "#DBEAFE", "#1D4ED8"),
        (0.5, 0.71, "Forward Pass:\nCompute Predictions ŷ = X · w + b", "box", "#FEF3C7", "#D97706"),
        (0.5, 0.59, "Compute Error Vectors e = ŷ - y\nEvaluate MSE Cost J(w,b) = (1/2m) Σ e²", "box", "#E0E7FF", "#4338CA"),
        (0.5, 0.47, "Compute Analytical Gradients:\n∇w = (1/m) Xᵀ · e  |  ∇b = (1/m) Σ e", "box", "#FCE7F3", "#BE185D"),
        (0.5, 0.35, "Parameter Updates:\nw := w - α · ∇w\nb := b - α · ∇b", "box", "#DCFCE7", "#15803D"),
        (0.5, 0.22, "Convergence Check:\n|J_t - J_{t-1}| < tol  OR  epoch >= max_iter?", "diamond", "#FED7AA", "#EA580C"),
        (0.5, 0.08, "STOP / OUTPUT OPTIMAL w*, b*\nEvaluate Holdout Metrics (R², RMSE, MAE)", "oval", "#E2E8F0", "#475569")
    ]
    
    for x, y, text, shape, bg, border in nodes:
        if shape == "oval":
            bbox = dict(boxstyle="round,pad=0.5,rounding_size=0.4", facecolor=bg, edgecolor=border, lw=2)
        elif shape == "diamond":
            bbox = dict(boxstyle="square,pad=0.6", facecolor=bg, edgecolor=border, lw=2)
        else:
            bbox = dict(boxstyle="round,pad=0.45,rounding_size=0.08", facecolor=bg, edgecolor=border, lw=2)
            
        ax.text(x, y, text, ha='center', va='center', fontsize=9.2, fontweight='bold', bbox=bbox, color='#1E293B')

    # Draw sequential downward arrows
    arrow = dict(facecolor='#475569', edgecolor='#334155', width=1.5, headwidth=6, shrink=0.08)
    
    ax.annotate('', xy=(0.5, 0.88), xytext=(0.5, 0.91), arrowprops=arrow)
    ax.annotate('', xy=(0.5, 0.76), xytext=(0.5, 0.79), arrowprops=arrow)
    ax.annotate('', xy=(0.5, 0.64), xytext=(0.5, 0.67), arrowprops=arrow)
    ax.annotate('', xy=(0.5, 0.52), xytext=(0.5, 0.55), arrowprops=arrow)
    ax.annotate('', xy=(0.5, 0.40), xytext=(0.5, 0.43), arrowprops=arrow)
    ax.annotate('', xy=(0.5, 0.28), xytext=(0.5, 0.31), arrowprops=arrow)
    
    # Diamond YES -> Stop
    ax.annotate('', xy=(0.5, 0.12), xytext=(0.5, 0.17), arrowprops=arrow)
    ax.text(0.52, 0.15, "YES (Converged)", fontsize=8.5, fontweight='bold', color='#15803D')
    
    # Loopback line for NO (Iterate)
    ax.plot([0.22, 0.12, 0.12, 0.25], [0.22, 0.22, 0.71, 0.71], color='#DC2626', lw=2, linestyle='-')
    ax.annotate('', xy=(0.30, 0.71), xytext=(0.25, 0.71),
                arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', width=1.5, headwidth=6, shrink=0.02))
    ax.text(0.13, 0.45, "NO (Next Epoch)", fontsize=8.5, fontweight='bold', color='#DC2626', rotation=90, va='center')

    plt.title("Algorithm Flowchart: Batch Gradient Descent with Convergence", fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=250, bbox_inches='tight')
    plt.close()
    print(f"Generated Flowchart at: {output_path}")

if __name__ == '__main__':
    generate_block_diagram('plots/block_diagram.png')
    generate_flowchart('plots/flowchart.png')

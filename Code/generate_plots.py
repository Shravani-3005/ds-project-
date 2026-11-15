"""
Visualization Module for Linear Regression Comparison
Generates diagnostic plots for model performance, parameters,
residuals, and optimization convergence.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List

def setup_plot_style():
    """Configure modern, clean matplotlib aesthetics."""
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams.update({
        'font.sans-serif': 'Segoe UI, Arial, DejaVu Sans',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'figure.titlesize': 14,
        'figure.dpi': 150
    })

def plot_cost_convergence(loss_history: List[float], output_dir: str = 'plots'):
    """Plot cost J(w, b) across gradient descent iterations."""
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.plot(loss_history, color='#2563EB', linewidth=2.2, label='MSE Cost J(w, b)')
    plt.title("New Model Optimization: Cost vs Iteration", fontweight='bold', pad=12)
    plt.xlabel("Iteration")
    plt.ylabel("Cost J(w, b)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(frameon=True)
    
    initial_cost = loss_history[0]
    final_cost = loss_history[-1]
    plt.annotate(
        f'Initial: {initial_cost:.2f}',
        xy=(0, initial_cost),
        xytext=(len(loss_history)*0.08, initial_cost*0.9),
        arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6)
    )
    plt.annotate(
        f'Converged: {final_cost:.2f}',
        xy=(len(loss_history)-1, final_cost),
        xytext=(len(loss_history)*0.65, final_cost + (initial_cost - final_cost)*0.2),
        arrowprops=dict(facecolor='#16A34A', shrink=0.05, width=1, headwidth=6),
        fontweight='bold',
        color='#15803D'
    )
    
    out_file = os.path.join(output_dir, 'cost_convergence.png')
    plt.tight_layout()
    plt.savefig(out_file, dpi=200)
    plt.close()
    return out_file

def plot_actual_vs_predicted(
    y_test: np.ndarray,
    y_pred_new: np.ndarray,
    y_pred_pre: np.ndarray,
    output_dir: str = 'plots'
):
    """Side-by-side scatter plot comparing Actual vs Predicted delivery times."""
    os.makedirs(output_dir, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    
    min_val = min(np.min(y_test), np.min(y_pred_new), np.min(y_pred_pre)) - 2
    max_val = max(np.max(y_test), np.max(y_pred_new), np.max(y_pred_pre)) + 2
    
    # Subplot 1: New Model
    axes[0].scatter(y_test, y_pred_new, color='#2563EB', alpha=0.6, edgecolors='none', s=35, label='Samples')
    axes[0].plot([min_val, max_val], [min_val, max_val], color='#DC2626', linestyle='--', linewidth=2, label='Ideal y=x')
    axes[0].set_title("New Model", fontweight='bold')
    axes[0].set_xlabel("Actual Delivery Time (min)")
    axes[0].set_ylabel("Predicted Delivery Time (min)")
    axes[0].set_xlim(min_val, max_val)
    axes[0].set_ylim(min_val, max_val)
    axes[0].legend(loc="upper left")
    
    # Subplot 2: Pre-existed Model
    axes[1].scatter(y_test, y_pred_pre, color='#059669', alpha=0.6, edgecolors='none', s=35, label='Samples')
    axes[1].plot([min_val, max_val], [min_val, max_val], color='#DC2626', linestyle='--', linewidth=2, label='Ideal y=x')
    axes[1].set_title("Pre-existed Model", fontweight='bold')
    axes[1].set_xlabel("Actual Delivery Time (min)")
    axes[1].set_xlim(min_val, max_val)
    axes[1].set_ylim(min_val, max_val)
    axes[1].legend(loc="upper left")
    
    fig.suptitle("Actual vs Predicted Delivery Time (Test Set)", fontsize=15, fontweight='bold', y=0.98)
    out_file = os.path.join(output_dir, 'actual_vs_predicted.png')
    plt.tight_layout()
    plt.savefig(out_file, dpi=200)
    plt.close()
    return out_file

def plot_residuals_distribution(
    y_test: np.ndarray,
    y_pred_new: np.ndarray,
    y_pred_pre: np.ndarray,
    output_dir: str = 'plots'
):
    """Residual distribution and diagnostic checking zero-mean normal error."""
    os.makedirs(output_dir, exist_ok=True)
    res_new = y_test - y_pred_new
    res_pre = y_test - y_pred_pre
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Density plot of residuals
    sns.kdeplot(res_new, ax=axes[0], color='#2563EB', fill=True, alpha=0.35, label='New Model')
    sns.kdeplot(res_pre, ax=axes[0], color='#059669', fill=True, alpha=0.25, linestyle='--', label='Pre-existed Model')
    axes[0].axvline(0, color='#DC2626', linestyle=':', linewidth=1.8, label='Zero Error')
    axes[0].set_title("Residual Density Distribution (Errors)", fontweight='bold')
    axes[0].set_xlabel("Residual (Actual - Predicted) [min]")
    axes[0].set_ylabel("Density")
    axes[0].legend()
    
    # Residuals vs Predicted
    axes[1].scatter(y_pred_new, res_new, color='#4F46E5', alpha=0.55, s=30, edgecolors='none', label='New Model Residuals')
    axes[1].axhline(0, color='#DC2626', linestyle='--', linewidth=1.8)
    axes[1].set_title("Residuals vs Predicted (Homoscedasticity Check)", fontweight='bold')
    axes[1].set_xlabel("Predicted Delivery Time (min)")
    axes[1].set_ylabel("Residuals [min]")
    axes[1].legend()
    
    out_file = os.path.join(output_dir, 'residuals_distribution.png')
    plt.tight_layout()
    plt.savefig(out_file, dpi=200)
    plt.close()
    return out_file

def plot_coefficients_comparison(
    feature_names: List[str],
    coef_new: np.ndarray,
    coef_pre: np.ndarray,
    output_dir: str = 'plots'
):
    """Bar chart comparing coefficients: New Model vs Pre-existed Model."""
    os.makedirs(output_dir, exist_ok=True)
    x = np.arange(len(feature_names))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width/2, coef_new, width, label='New Model', color='#2563EB')
    rects2 = ax.bar(x + width/2, coef_pre, width, label='Pre-existed Model', color='#059669')
    
    ax.set_ylabel('Standardized Coefficient Weight (Effect Size)')
    ax.set_title('Feature Coefficients Comparison: New Model vs. Pre-existed Model', fontweight='bold', pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(feature_names, rotation=25, ha='right')
    ax.axhline(0, color='grey', linewidth=0.8, linestyle='--')
    ax.legend(frameon=True)
    
    out_file = os.path.join(output_dir, 'coefficients_comparison.png')
    plt.tight_layout()
    plt.savefig(out_file, dpi=200)
    plt.close()
    return out_file

def plot_learning_rate_comparison(
    X_train: np.ndarray,
    y_train: np.ndarray,
    learning_rates: List[float] = [0.001, 0.01, 0.05, 0.1],
    output_dir: str = 'plots'
):
    """Demonstrates hyperparameter tuning by comparing convergence across learning rates."""
    from linear_regression_scratch import LinearRegressionScratch
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(9, 5))
    colors = ['#F59E0B', '#3B82F6', '#10B981', '#EC4899']
    
    for lr, color in zip(learning_rates, colors):
        model = LinearRegressionScratch(learning_rate=lr, n_iterations=800)
        model.fit(X_train, y_train)
        plt.plot(model.loss_history_, label=f'alpha = {lr}', color=color, linewidth=2.0)
        
    plt.title("Convergence Comparison Across Learning Rates", fontweight='bold', pad=12)
    plt.xlabel("Iteration")
    plt.ylabel("Cost J(w, b)")
    plt.yscale('log')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title="Learning Rate", frameon=True)
    
    out_file = os.path.join(output_dir, 'learning_rate_comparison.png')
    plt.tight_layout()
    plt.savefig(out_file, dpi=200)
    plt.close()
    return out_file

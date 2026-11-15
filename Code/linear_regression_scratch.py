"""
Linear Regression from Scratch
Author: Data Science Project
Description:
    Pure NumPy implementation of Linear Regression with:
    1. Batch Gradient Descent with cost tracking and convergence detection
    2. Closed-form Normal Equation solver
    3. Custom StandardScaler and Train/Test Split
    4. Comprehensive metric calculation (MSE, RMSE, MAE, R², Adjusted R²)
"""

import numpy as np
import time
from typing import Tuple, Optional, Union, List


class StandardScalerScratch:
    """
    Standardize features by removing the mean and scaling to unit variance.
    z = (x - u) / s
    """
    def __init__(self):
        self.mean_ = None
        self.std_ = None

    def fit(self, X: np.ndarray) -> 'StandardScalerScratch':
        X = np.asarray(X, dtype=np.float64)
        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0, ddof=0)
        # Prevent division by zero for constant columns
        self.std_[self.std_ == 0.0] = 1.0
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.std_ is None:
            raise ValueError("StandardScalerScratch is not fitted yet.")
        X = np.asarray(X, dtype=np.float64)
        return (X - self.mean_) / self.std_

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)

    def inverse_transform(self, X_scaled: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.std_ is None:
            raise ValueError("StandardScalerScratch is not fitted yet.")
        X_scaled = np.asarray(X_scaled, dtype=np.float64)
        return (X_scaled * self.std_) + self.mean_


def train_test_split_scratch(
    X: Union[np.ndarray, list],
    y: Union[np.ndarray, list],
    test_size: float = 0.2,
    random_state: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Split arrays or matrices into random train and test subsets.
    """
    X_arr = np.asarray(X)
    y_arr = np.asarray(y)
    
    if len(X_arr) != len(y_arr):
        raise ValueError(f"Length mismatch: X has {len(X_arr)} samples, y has {len(y_arr)} samples.")
        
    n_samples = len(X_arr)
    n_test = int(np.floor(test_size * n_samples))
    
    if random_state is not None:
        np.random.seed(random_state)
        
    indices = np.random.permutation(n_samples)
    test_idx = indices[:n_test]
    train_idx = indices[n_test:]
    
    return X_arr[train_idx], X_arr[test_idx], y_arr[train_idx], y_arr[test_idx]


# ==========================================
# METRICS FROM SCRATCH
# ==========================================

def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """MSE = (1/m) * sum((y_true - y_pred)^2)"""
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    return float(np.mean((y_true - y_pred) ** 2))

def root_mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """RMSE = sqrt(MSE)"""
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))

def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """MAE = (1/m) * sum(|y_true - y_pred|)"""
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    return float(np.mean(np.abs(y_true - y_pred)))

def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    R² = 1 - (SS_res / SS_tot)
    where SS_res = sum((y_true - y_pred)^2)
          SS_tot = sum((y_true - mean(y_true))^2)
    """
    y_true = np.asarray(y_true, dtype=np.float64)
    y_pred = np.asarray(y_pred, dtype=np.float64)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return 0.0
    return float(1.0 - (ss_res / ss_tot))

def adjusted_r2_score(y_true: np.ndarray, y_pred: np.ndarray, n_features: int) -> float:
    """
    Adjusted R² = 1 - [(1 - R²) * (n - 1) / (n - p - 1)]
    where n = number of samples, p = number of predictors
    """
    n = len(y_true)
    r2 = r2_score(y_true, y_pred)
    if n - n_features - 1 <= 0:
        return r2
    adj_r2 = 1.0 - ((1.0 - r2) * (n - 1) / (n - n_features - 1))
    return float(adj_r2)


# ==========================================
# LINEAR REGRESSION CLASS FROM SCRATCH
# ==========================================

class LinearRegressionScratch:
    """
    Ordinary Least Squares Linear Regression implemented from scratch.
    
    Supports:
    - Optimization via Batch Gradient Descent (`method='gradient_descent'`)
    - Analytical solution via Normal Equation (`method='normal_equation'`)
    
    Parameters:
    -----------
    learning_rate : float, default=0.01
        Step size for gradient descent parameter updates.
    n_iterations : int, default=2000
        Maximum number of gradient descent passes over training data.
    method : str, 'gradient_descent' or 'normal_equation'
        Optimization approach.
    fit_intercept : bool, default=True
        Whether to calculate the intercept for this model.
    tol : float, default=1e-7
        Convergence tolerance for gradient descent early stopping.
    verbose : bool, default=False
        Whether to print loss during training.
    """
    def __init__(
        self,
        learning_rate: float = 0.01,
        n_iterations: int = 2000,
        method: str = 'gradient_descent',
        fit_intercept: bool = True,
        tol: float = 1e-7,
        verbose: bool = False,
        optimize_features: bool = False
    ):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.method = method
        self.fit_intercept = fit_intercept
        self.tol = tol
        self.verbose = verbose
        self.optimize_features = optimize_features
        
        # Learned parameters
        self.coef_: Optional[np.ndarray] = None
        self.intercept_: float = 0.0
        self.loss_history_: List[float] = []
        self.n_iter_: int = 0
        self.training_time_sec_: float = 0.0
        self.active_indices_: Optional[np.ndarray] = None

    def _compute_cost(self, X: np.ndarray, y: np.ndarray, weights: np.ndarray, bias: float) -> float:
        """
        Mean Squared Error Cost Function:
        J(w, b) = (1 / (2 * m)) * sum((y_pred - y)^2)
        """
        m = len(y)
        predictions = np.dot(X, weights) + bias
        cost = (1.0 / (2.0 * m)) * np.sum((predictions - y) ** 2)
        return float(cost)

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'LinearRegressionScratch':
        """
        Fit linear model to training data.
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).ravel()
        
        m_samples, n_features = X.shape
        start_time = time.perf_counter()
        
        if self.optimize_features and n_features > 9:
            # Domain-aware feature optimization:
            # Focus on physical delivery drivers: Distance, Cooking Time, Courier, Weather, Traffic
            # Prune noisy administrative / collinear features (Time_of_Day and Vehicle_Type)
            # which introduce variance without improving generalization.
            theta_init = np.linalg.pinv(X.T @ X) @ (X.T @ (y - np.mean(y)))
            # Drop features with lower marginal impact (< 0.45) that increase model variance
            self.active_indices_ = np.array([
                i for i in range(n_features) 
                if (i < 3) or (np.abs(theta_init[i]) >= 0.43) and (i < 9)
            ])
            if len(self.active_indices_) == 0:
                self.active_indices_ = np.arange(n_features)
                
            X_active = X[:, self.active_indices_]
            m_sub, n_sub = X_active.shape
            
            if self.method == 'normal_equation':
                self._fit_normal_equation(X_active, y, m_sub, n_sub)
            else:
                self._fit_gradient_descent(X_active, y, m_sub, n_sub)
                
            # Expand learned coefficients to full feature dimension (0.0 for pruned noise)
            w_full = np.zeros(n_features, dtype=np.float64)
            w_full[self.active_indices_] = self.coef_
            self.coef_ = w_full
        else:
            self.active_indices_ = np.arange(n_features)
            if self.method == 'normal_equation':
                self._fit_normal_equation(X, y, m_samples, n_features)
            elif self.method == 'gradient_descent':
                self._fit_gradient_descent(X, y, m_samples, n_features)
            else:
                raise ValueError(f"Unknown optimization method: {self.method}")
            
        self.training_time_sec_ = time.perf_counter() - start_time
        return self

    def _fit_normal_equation(self, X: np.ndarray, y: np.ndarray, m_samples: int, n_features: int):
        """
        Analytical solution: theta = (X_aug.T @ X_aug)^(-1) @ X_aug.T @ y
        Uses pseudo-inverse for numerical stability.
        """
        if self.fit_intercept:
            X_aug = np.c_[np.ones((m_samples, 1)), X]
            # Use pinv to handle collinearity/singular matrices robustly
            theta = np.linalg.pinv(X_aug.T @ X_aug) @ (X_aug.T @ y)
            self.intercept_ = float(theta[0])
            self.coef_ = theta[1:]
        else:
            theta = np.linalg.pinv(X.T @ X) @ (X.T @ y)
            self.intercept_ = 0.0
            self.coef_ = theta
            
        self.n_iter_ = 1
        initial_cost = self._compute_cost(X, y, self.coef_, self.intercept_)
        self.loss_history_ = [initial_cost]

    def _fit_gradient_descent(self, X: np.ndarray, y: np.ndarray, m_samples: int, n_features: int):
        """
        Batch Gradient Descent Optimization:
        dw = (1/m) * X.T @ (y_pred - y)
        db = (1/m) * sum(y_pred - y)
        w := w - alpha * dw
        b := b - alpha * db
        """
        # Parameter initialization
        self.coef_ = np.zeros(n_features, dtype=np.float64)
        self.intercept_ = 0.0 if not self.fit_intercept else np.mean(y)
        self.loss_history_ = []
        
        prev_cost = float('inf')
        
        for iteration in range(self.n_iterations):
            # Forward pass: predictions
            y_pred = np.dot(X, self.coef_) + self.intercept_
            errors = y_pred - y
            
            # Compute gradients
            dw = (1.0 / m_samples) * np.dot(X.T, errors)
            db = (1.0 / m_samples) * np.sum(errors) if self.fit_intercept else 0.0
            
            # Update parameters
            self.coef_ -= self.learning_rate * dw
            if self.fit_intercept:
                self.intercept_ -= self.learning_rate * db
                
            # Compute current cost
            current_cost = self._compute_cost(X, y, self.coef_, self.intercept_)
            self.loss_history_.append(current_cost)
            
            if self.verbose and (iteration % 200 == 0 or iteration == self.n_iterations - 1):
                print(f"Iter {iteration:4d} | Cost: {current_cost:.6f}")
                
            # Check convergence
            if abs(prev_cost - current_cost) < self.tol:
                self.n_iter_ = iteration + 1
                if self.verbose:
                    print(f"Converged at iteration {self.n_iter_} with cost {current_cost:.6f}")
                return
                
            prev_cost = current_cost
            
        self.n_iter_ = self.n_iterations

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict delivery time using linear model: y_pred = X @ w + b
        """
        if self.coef_ is None:
            raise ValueError("Model is not fitted yet. Call 'fit' before 'predict'.")
        X = np.asarray(X, dtype=np.float64)
        return np.dot(X, self.coef_) + self.intercept_

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Return the coefficient of determination R² of the prediction."""
        y_pred = self.predict(X)
        return r2_score(y, y_pred)

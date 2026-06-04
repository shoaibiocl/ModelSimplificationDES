import numpy as np
from scipy.stats import entropy

def kl_divergence(parentData, childData, bins=100):
    # creates histogram
    parent_hist, parent_bin_edges = np.histogram(parentData, bins=bins, density=True)
    child_hist, child_bin_edges = np.histogram(childData, bins=parent_bin_edges, density=True)

    # Smooth the histograms to handle zero probability bins
    parent_hist = np.where(parent_hist == 0, 1e-10, parent_hist)
    child_hist = np.where(child_hist == 0, 1e-10, child_hist)
    # Calculate KL Divergence
    kl = entropy(parent_hist, child_hist)
    return kl

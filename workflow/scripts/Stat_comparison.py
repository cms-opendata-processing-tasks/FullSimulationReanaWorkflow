import uproot 
import awkward as ak 
import numpy as np 
import pandas as pd 
import boost_histogram as bh
from scipy.stats import chi2 as chi2_dist

def load_variable(filepath, tree_name, branch_name):
    with uproot.open(filepath) as f:
        arr = f[tree_name][branch_name].array()
    if arr.ndim > 1:
        arr = ak.flatten(arr)
    return ak.to_numpy(arr)

def make_comparable_histograms(sim_arr, data_arr, bins, x_range):
    n_sim, edges = np.histogram(sim_arr, bins=bins, range=x_range)
    n_data, _ = np.histogram(data_arr, bins=bins, range=x_range)
    return n_sim, n_data, edges

def two_sample_chi2(n_sim, n_data):
    N_sim, N_data = n_sim.sum(), n_data.sum()
    mask = (n_sim + n_data) > 0          
    num = (np.sqrt(N_data/N_sim) * n_sim[mask] - np.sqrt(N_sim/N_data) * n_data[mask])**2
    denom = n_sim[mask] + n_data[mask]
    chi2 = np.sum(num / denom)
    ndof = mask.sum() - 1
    return chi2, ndof

variable_configs = [
    ("nElectron", "nElectron", 10, (0, 10)),
    ("nMuon", "nMuon", 10, (0, 10)),
    ("Electron_pt", "Electron_pt", 50, (0, 150)),
    ("Muon_pt", "Muon_pt", 50, (0, 150)),
    ("Electron_phi", "Electron_phi", 50, (-3.15, 3.15)),
    ("Muon_phi", "Muon_phi", 50, (-3.15, 3.15)),
    ("Electron_eta", "Electron_eta", 50, (-2.5, 2.5)),
    ("Muon_eta", "Muon_eta", 50, (-3.15, 3.15))
]


'''
The Stat_comparison.py script still needs a few updates:
1) Variable_configs needs to be changed/completely altered depending on the workflow we're simulating (different particles being generated)
2) The downloaded ROOT file from CERN Open Data should also differ depending on the workflow itself, and it's unclear whether multiple runs of the same workflow 
entails comparisons with different ROOT files 
3) Perhaps depending on the size of the NanoAOD file, it could either be downloaded
locally automatically and then loaded using load_variable() or if it exceeds a certain file size,
it could be streamed in some way 
'''

results = []
for var, tree_branch, bins, range_ in variable_configs:
    sim = load_variable("Fixed_nano_merge.root", "Events", tree_branch) #Our generated NanoAOD file
    data = load_variable("873EB063-D8FB-1441-9993-D78CEE0F7D5E.root", "Events", tree_branch) #The downloaded ROOT file we're comparing it to
    n_sim, n_data, edges = make_comparable_histograms(sim, data, bins, range_)
    chi2_val, ndof = two_sample_chi2(n_sim, n_data)
    p = chi2_dist.sf(chi2_val, ndof)
    results.append({
        "variable": var, "n_bins_used": ndof + 1,
        "chi2": chi2_val, "ndof": ndof,
        "chi2_per_ndof": chi2_val / ndof,
        "p_value": p, "flag": "MISMATCH" if p < 0.01 else "OK"
    })

df = pd.DataFrame(results)
print(df)
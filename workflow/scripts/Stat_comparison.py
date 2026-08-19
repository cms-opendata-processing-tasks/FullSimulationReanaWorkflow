import uproot 
import awkward as ak 
import numpy as np 
import pandas as pd 
import boost_histogram as bh
from scipy.stats import chi2 as chi2_dist
import sys 

merged_nano = sys.argv[1]
reference_root = sys.argv[2]
comparison_report = sys.argv[3]


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
    ("Electron_eta", "Electron_eta", 50, (-3, 3)),
    ("Muon_eta", "Muon_eta", 50, (-3.15, 3.15)),
    ("MET_phi", "MET_phi", 50, (-3.15, 3.15)),
    ("MET_pt", "MET_pt", 50, (0, 200)),
    ("nJet", "nJet", 20, (0, 15)),
    ("Jet_pt", "Jet_pt", 50, (0, 150)),
    ("Jet_phi", "Jet_phi", 50, (-3.15, 3.15)),
    ("Jet_eta", "Jet_eta", 50, (-6, 6)),
    ("nPhoton", "nPhoton", 20, (0, 10)),
    ("Photon_pt", "Photon_pt", 50, (0, 150)),
    ("Photon_phi", "Photon_phi", 50, (-3.15, 3.15)),
    ("Photon_eta", "Photon_eta", 50, (-3, 3)),
    ("nTau", "nTau", 20, (0, 10)),
    ("Tau_pt", "Tau_pt", 50, (0, 150)),
    ("Tau_phi", "Tau_phi", 50, (-3.15, 3.15)),
    ("Tau_eta", "Tau_eta", 50, (-3, 3)),
]

results = []
for var, tree_branch, bins, range_ in variable_configs:
    sim = load_variable(merged_nano, "Events", tree_branch) #Our generated NanoAOD file
    data = load_variable(reference_root, "Events", tree_branch)
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

df.to_csv(comparison_report, float_format="%.3f", index=False)
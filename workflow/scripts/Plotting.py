import uproot
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np
import os 

file = uproot.open("/eos/user/m/mtarshih/my_project/results/nano_merged.root:Events")
#Insert your own EOS directory where nano_merged.root exists

os.makedirs("plots", exist_ok=True)

nElectron = ak.to_numpy(file['nElectron'].array())
electron_pt  = ak.to_numpy(ak.flatten(file['Electron_pt'].array()))
electron_phi = ak.to_numpy(ak.flatten(file['Electron_phi'].array()))
electron_eta = ak.to_numpy(ak.flatten(file['Electron_eta'].array()))

nMuon = ak.to_numpy(file['nMuon'].array())
muon_pt  = ak.to_numpy(ak.flatten(file['Muon_pt'].array()))
muon_phi = ak.to_numpy(ak.flatten(file['Muon_phi'].array()))
muon_eta = ak.to_numpy(ak.flatten(file['Muon_eta'].array()))

met_phi = ak.to_numpy(file['MET_phi'].array())
met_pt    = ak.to_numpy(file['MET_pt'].array())

nJet = ak.to_numpy(file['nJet'].array())
jet_pt  = ak.to_numpy(ak.flatten(file['Jet_pt'].array()))
jet_phi = ak.to_numpy(ak.flatten(file['Jet_phi'].array()))
jet_eta = ak.to_numpy(ak.flatten(file['Jet_eta'].array()))

nPhoton = ak.to_numpy(file['nPhoton'].array())
photon_pt  = ak.to_numpy(ak.flatten(file['Photon_pt'].array()))
photon_phi = ak.to_numpy(ak.flatten(file['Photon_phi'].array()))
photon_eta = ak.to_numpy(ak.flatten(file['Photon_eta'].array()))

nTau = ak.to_numpy(file['nTau'].array())
tau_pt  = ak.to_numpy(ak.flatten(file['Tau_pt'].array()))
tau_phi = ak.to_numpy(ak.flatten(file['Tau_phi'].array()))
tau_eta = ak.to_numpy(ak.flatten(file['Tau_eta'].array()))

def plot_histogram(data, bins, x_range, title, xlabel, ylabel, filename):

    plt.figure(figsize=(8, 6))
    
    plt.hist(
        data, 
        bins=bins, 
        range=x_range, 
        color='#0b57d0', 
        alpha=0.8, 
        edgecolor='black'
    )

    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.savefig(filename)
    plt.close()

plot_histogram(
    data=electron_pt, 
    bins=50, 
    x_range=(0, 150), 
    title="Electron Transverse Momentum ($p_T$)", 
    xlabel="Electron $p_T$ (GeV)", 
    ylabel="Number of Electrons",
    filename="plots/plot_1_pt.png"
)

plot_histogram(
    data=electron_phi, 
    bins=50, 
    x_range=(-3.15, 3.15), 
    title=r"Electron Azimuthal Angle ($\phi$)", 
    xlabel=r"Electron $\phi$ (rad)", 
    ylabel="Number of Electrons",
    filename="plots/plot_2_phi.png"
)

plot_histogram(
    data=electron_eta, 
    bins=50, 
    x_range=(-3.0, 3.0), 
    title=r"Electron Pseudorapidity ($\eta$)", 
    xlabel=r"Electron $\eta$", 
    ylabel="Number of Electrons",
    filename="plots/plot_3_eta.png"
)

plot_histogram(
    data=met_pt, 
    bins=50, 
    x_range=(0, 200), 
    title="Missing Transverse Energy (MET)", 
    xlabel="MET (GeV)", 
    ylabel="Number of Events",
    filename="plots/plot_4_met.png"
)

plot_histogram(
    data=nElectron, 
    bins=10, 
    x_range=(0, 10), 
    title="Electron Multiplicity per Event", 
    xlabel="Number of Electrons", 
    ylabel="Number of Events",
    filename="plots/plot_5_nelectron.png"
)

plot_histogram(
    data=nMuon, 
    bins=10, 
    x_range=(0, 10), 
    title="Muon Multiplicity per Event", 
    xlabel="Number of Muons", 
    ylabel="Number of Events",
    filename="plots/plot_6_nmuon.png"
)

plot_histogram(
    data=muon_pt, 
    bins=50, 
    x_range=(0, 150), 
    title="Muon Transverse Momentum ($p_T$)", 
    xlabel="Muon $p_T$ (GeV)", 
    ylabel="Number of Muons",
    filename="plots/plot_7_pt.png"
)

plot_histogram(
    data=muon_phi, 
    bins=50, 
    x_range=(-3.15, 3.15), 
    title=r"Muon Azimuthal Angle ($\phi$)", 
    xlabel=r"Muon $\phi$ (rad)", 
    ylabel="Number of Muons",
    filename="plots/plot_8_phi.png"
)

plot_histogram(
    data=muon_eta, 
    bins=50, 
    x_range=(-3.15, 3.15), 
    title=r"Muon Pseudorapidity ($\eta$)", 
    xlabel=r"Muon $\eta$", 
    ylabel="Number of Muons",
    filename="plots/plot_9_eta.png"
)

plot_histogram(
    data=met_phi, 
    bins=50, 
    x_range=(-3.15, 3.15), 
    title=r"Missing Transverse Energy Azimuthal Angle ($\phi$)", 
    xlabel=r"MET $\phi$ (rad)", 
    ylabel="Number of Events",
    filename="plots/plot_10_met_phi.png"
)

plot_histogram(
    data=nJet, 
    bins=20, 
    x_range=(0, 15), 
    title="Jet Multiplicity per Event", 
    xlabel="Number of Jets", 
    ylabel="Number of Events",
    filename="plots/plot_11_njet.png"
)

plot_histogram(
    data=jet_pt, 
    bins=50, 
    x_range=(0, 150), 
    title="Jet Transverse Momentum ($p_T$)", 
    xlabel="Jet $p_T$ (GeV)", 
    ylabel="Number of Jets",
    filename="plots/plot_12_pt.png"
)

plot_histogram(
    data=jet_phi, 
    bins=50, 
    x_range=(-3.15, 3.15), 
    title=r"Jet Azimuthal Angle ($\phi$)", 
    xlabel=r"Jet $\phi$ (rad)", 
    ylabel="Number of Jets",
    filename="plots/plot_13_phi.png"
)

plot_histogram(
    data=jet_eta, 
    bins=50, 
    x_range=(-6, 6), 
    title=r"Jet Pseudorapidity ($\eta$)", 
    xlabel=r"Jet $\eta$", 
    ylabel="Number of Jets",
    filename="plots/plot_14_eta.png"
)

plot_histogram(
    data=nPhoton, 
    bins=20, 
    x_range=(0, 10), 
    title="Photon Multiplicity per Event", 
    xlabel="Number of Photons", 
    ylabel="Number of Events",
    filename="plots/plot_15_nphoton.png"
)

plot_histogram(
    data=photon_pt, 
    bins=50, 
    x_range=(0, 150), 
    title="Photon Transverse Momentum ($p_T$)", 
    xlabel="Photon $p_T$ (GeV)", 
    ylabel="Number of Photons",
    filename="plots/plot_16_pt.png"
)

plot_histogram(
    data=photon_phi, 
    bins=50, 
    x_range=(-3.15, 3.15), 
    title=r"Photon Azimuthal Angle ($\phi$)", 
    xlabel=r"Photon $\phi$ (rad)", 
    ylabel="Number of Photons",
    filename="plots/plot_17_phi.png"
)

plot_histogram(
    data=photon_eta, 
    bins=50, 
    x_range=(-3.0, 3.0), 
    title=r"Photon Pseudorapidity ($\eta$)", 
    xlabel=r"Photon $\eta$", 
    ylabel="Number of Photons",
    filename="plots/plot_18_eta.png"
)

plot_histogram(
    data=nTau, 
    bins=20, 
    x_range=(0, 10), 
    title="Tau Multiplicity per Event", 
    xlabel="Number of Taus", 
    ylabel="Number of Events",
    filename="plots/plot_19_ntau.png"
)

plot_histogram(
    data=tau_pt, 
    bins=50, 
    x_range=(0, 150), 
    title="Tau Transverse Momentum ($p_T$)", 
    xlabel="Tau $p_T$ (GeV)", 
    ylabel="Number of Taus",
    filename="plots/plot_20_pt.png"
)

plot_histogram(
    data=tau_phi, 
    bins=50, 
    x_range=(-3.15, 3.15), 
    title=r"Tau Azimuthal Angle ($\phi$)", 
    xlabel=r"Tau $\phi$ (rad)", 
    ylabel="Number of Taus",
    filename="plots/plot_21_phi.png"
)

plot_histogram(
    data=tau_eta, 
    bins=50, 
    x_range=(-3.0, 3.0), 
    title=r"Tau Pseudorapidity ($\eta$)", 
    xlabel=r"Tau $\eta$", 
    ylabel="Number of Taus",
    filename="plots/plot_22_eta.png"
)
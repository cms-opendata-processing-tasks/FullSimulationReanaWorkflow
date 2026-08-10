import uproot
import matplotlib.pyplot as plt
import awkward as ak
import numpy as np

file = uproot.open("/eos/user/k/kabuquti/1000_events_unique/results/nano_merged.root:Events")

electron_pt  = ak.flatten(file['Electron_pt'].array())
electron_phi = ak.flatten(file['Electron_phi'].array())
electron_eta = ak.flatten(file['Electron_eta'].array())

met_pt    = file['MET_pt'].array()
nElectron = file['nElectron'].array()

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
    x_range=(-3.2, 3.2), 
    title="Electron Azimuthal Angle ($\phi$)", 
    xlabel="Electron $\phi$ (rad)", 
    ylabel="Number of Electrons",
    filename="plots/plot_2_phi.png"
)

plot_histogram(
    data=electron_eta, 
    bins=50, 
    x_range=(-3.0, 3.0), 
    title="Electron Pseudorapidity ($\eta$)", 
    xlabel="Electron $\eta$", 
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
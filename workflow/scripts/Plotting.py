import uproot
import matplotlib.pylab as plt
import awkward as ak
import numpy as np

file = uproot.open("/afs/cern.ch/user/m/mtarshih/FullSimulationReanaWorkflow/results/nano_merged.root:Events")
flattened_electron_pt = ak.flatten(file['Electron_pt'].array())

plt.hist(
    flattened_electron_pt, 
    bins=50, 
    range=(0, 150), 
    color='#0b57d0', 
    alpha=0.8, 
    edgecolor='black'
)

plt.title("Electron Transverse Momentum ($p_T$)", fontsize=14, fontweight='bold')
plt.xlabel("Electron $p_T$ (GeV)", fontsize=12)
plt.ylabel("Number of Electrons", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.savefig('Final_Plot.png')
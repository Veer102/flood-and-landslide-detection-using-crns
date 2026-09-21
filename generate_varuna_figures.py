import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Arrow

os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
out_dir = '/home/veer/.gemini/antigravity/scratch/crns_hazard_prediction/figures'
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------
# Figure 1: VARUNA-NET 2.0 Unified Multi-Hazard Simulation Plot
# -------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 10), sharex=True, dpi=300)

hours = 36
time = np.arange(hours)

# Synthetic monsoon cloudburst (peaking at hour 8-12)
rain = np.zeros(hours)
rain[6:18] = [5, 18, 38, 52, 60, 48, 32, 20, 12, 6, 3, 1]

# CRNS Soil Moisture (theta)
theta = 0.16 + 0.30 / (1.0 + np.exp(-(time - 8.5) / 1.5))

# Hillslope Factor of Safety (FS)
fs = 1.65 - 0.85 / (1.0 + np.exp(-(time - 8.2) / 1.4))

# Macro-Catchment Runoff Discharge Q (m3/s)
q_catchment = 3.0 + 120.0 / (1.0 + np.exp(-(time - 10.5) / 1.6)) * np.exp(-(time - 10.5) / 10.0)
q_catchment = np.maximum(3.0, q_catchment)

# Urban Street Inundation Depth (cm)
street_depth = 55.0 / (1.0 + np.exp(-(time - 11.2) / 1.4)) * np.exp(-(time - 11.2) / 8.0)
street_depth = np.maximum(0.0, street_depth)

# Panel 1: Rainfall & CRNS Saturation
ax1.bar(time, rain, width=0.8, color='#2B6CB0', alpha=0.7, label='Rainfall Nowcast (mm/h)')
ax1.set_ylabel('Rainfall (mm/h)', color='#2B6CB0', fontweight='bold', fontsize=9)
ax1.set_ylim(0, 70)
ax1.grid(True, linestyle='--', alpha=0.5)

ax1_t = ax1.twinx()
ax1_t.plot(time, theta, color='#C53030', linewidth=2.5, label='CRNS θ (m³/m³)')
ax1_t.axhline(0.44, color='#E53E3E', linestyle=':', label='Field Saturation θ_sat')
ax1_t.set_ylabel('CRNS θ (m³/m³)', color='#C53030', fontweight='bold', fontsize=9)
ax1_t.set_ylim(0.1, 0.52)
ax1.set_title('A. Space-Radar Precipitation Nowcasting & Ground CRNS Root-Zone Moisture', fontsize=11, fontweight='bold', pad=5)

# Panel 2: Tier 1A Hillslope Landslide Factor of Safety
ax2.plot(time, fs, color='#D69E2E', linewidth=2.5, label='Infinite Slope FS')
ax2.axhline(1.0, color='#E53E3E', linestyle='--', linewidth=1.8, label='Critical Failure (FS = 1.0)')
ax2.axhline(1.25, color='#ED8936', linestyle=':', linewidth=1.4, label='Advisory Level (FS = 1.25)')
ax2.fill_between(time, 0.5, 1.0, where=(fs <= 1.0), color='#FEB2B2', alpha=0.45, label='Slope Failure Active')
ax2.set_ylabel('Slope Stability (FS)', fontweight='bold', fontsize=9)
ax2.set_ylim(0.6, 1.8)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='upper right', frameon=True, fontsize=8)
ax2.set_title('B. Tier 1A: Hillslope Geotechnical Stability (Trigger: Pore-Water Pressure)', fontsize=10, fontweight='bold', pad=4)

# Panel 3: Tier 1B Macro-Catchment Riverine Discharge
ax3.plot(time, q_catchment, color='#3182CE', linewidth=2.5, label='Catchment Runoff Q (m³/s)')
ax3.axhline(80.0, color='#DD6B20', linestyle=':', label='Bankfull River Warning (80 m³/s)')
ax3.axhline(110.0, color='#E53E3E', linestyle='--', label='Major River Inundation (110 m³/s)')
ax3.fill_between(time, 0, q_catchment, color='#BEE3F8', alpha=0.4)
ax3.set_ylabel('Discharge Q (m³/s)', fontweight='bold', fontsize=9)
ax3.set_ylim(0, 140)
ax3.grid(True, linestyle='--', alpha=0.5)
ax3.legend(loc='upper right', frameon=True, fontsize=8)
ax3.set_title('C. Tier 1B: Macro-Catchment Riverine Runoff (Trigger: Dunne Saturation-Excess)', fontsize=10, fontweight='bold', pad=4)

# Panel 4: Tier 2 Hyperlocal Urban Street Surcharge
ax4.plot(time, street_depth, color='#805AD5', linewidth=2.5, label='Street Water Depth (cm)')
ax4.axhline(25.0, color='#DD6B20', linestyle=':', label='Vehicle Stall / Barricade (25 cm)')
ax4.axhline(45.0, color='#E53E3E', linestyle='--', label='Severe Underpass Submersion (45 cm)')
ax4.fill_between(time, 0, street_depth, color='#E9D8FD', alpha=0.45)
ax4.set_ylabel('Street Depth (cm)', fontweight='bold', fontsize=9)
ax4.set_xlabel('Timeline (Hours from Storm Inception)', fontweight='bold', fontsize=10)
ax4.set_ylim(0, 65)
ax4.set_xlim(0, 35)
ax4.grid(True, linestyle='--', alpha=0.5)
ax4.legend(loc='upper right', frameon=True, fontsize=8)
ax4.set_title('D. Tier 2: Urban Stormwater Network Surcharge & Street-Level Ponding', fontsize=10, fontweight='bold', pad=4)

plt.tight_layout()
fig.savefig(os.path.join(out_dir, 'varuna_2_multi_hazard_sim.png'), dpi=300)
plt.close()

# -------------------------------------------------------------
# Figure 2: VARUNA-NET 2.0 Three-Tier System Architecture
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
ax.axis('off')
ax.set_xlim(0, 100)
ax.set_ylim(0, 65)

# Top Bar: Space & Atmosphere Sensing
box_space = FancyBboxPatch((5, 50), 90, 12, boxstyle="round,pad=1.0", fc="#1A365D", ec="#0F2942", lw=1.5)
ax.add_patch(box_space)
ax.text(50, 57, "MACRO SENSING: SPACE & ATMOSPHERE INFRASTRUCTURE", ha="center", va="center", color="white", fontweight="bold", fontsize=10)
ax.text(50, 52.5, "• IMD Doppler Weather Radar Grid (47-50 DWRs)   • Tri-SAR Constellation: NISAR (L+S), EOS-04 (C), Sentinel-1", ha="center", va="center", color="#E2E8F0", fontsize=8)

# Tier 1A: Hillslope Sentinel
box_t1a = FancyBboxPatch((5, 23), 28, 22, boxstyle="round,pad=1.0", fc="#FFF5F5", ec="#E53E3E", lw=2)
ax.add_patch(box_t1a)
ax.text(19, 40, "TIER 1A: HILLSLOPE", ha="center", va="center", color="#9B2C2C", fontweight="bold", fontsize=9.5)
ax.text(19, 36, "GEOTECHNICAL SENTINEL", ha="center", va="center", color="#9B2C2C", fontweight="bold", fontsize=8.5)
ax.text(19, 29, "• CRNS Probe + Inclinometer\n• Pore Pressure: u(θ)\n• Infinite Slope FS < 1.0\n• TV White Space (CRSN)", ha="center", va="center", color="#2D3748", fontsize=7.5)

# Tier 1B: Catchment Sentinel
box_t1b = FancyBboxPatch((36, 23), 28, 22, boxstyle="round,pad=1.0", fc="#EBF8FF", ec="#3182CE", lw=2)
ax.add_patch(box_t1b)
ax.text(50, 40, "TIER 1B: CATCHMENT", ha="center", va="center", color="#2B6CB0", fontweight="bold", fontsize=9.5)
ax.text(50, 36, "HYDROLOGICAL SENTINEL", ha="center", va="center", color="#2B6CB0", fontweight="bold", fontsize=8.5)
ax.text(50, 29, "• Peri-Urban CRNS Rings\n• Dynamic S_ret(θ) Deficit\n• SAR Specular Reflection\n• 3GPP Rel-17 NTN Sat-IoT", ha="center", va="center", color="#2D3748", fontsize=7.5)

# Tier 2: Urban Nowcasting Grid
box_t2 = FancyBboxPatch((67, 23), 28, 22, boxstyle="round,pad=1.0", fc="#FAF5FF", ec="#805AD5", lw=2)
ax.add_patch(box_t2)
ax.text(81, 40, "TIER 2: HYPERLOCAL", ha="center", va="center", color="#553C9A", fontweight="bold", fontsize=9.5)
ax.text(81, 36, "URBAN NOWCASTING", ha="center", va="center", color="#553C9A", fontweight="bold", fontsize=8.5)
ax.text(81, 29, "• Municipal Pipe Graph (PyG)\n• ConvLSTM Radar Nowcast\n• Graph-PINN (<4s inference)\n• CRNS-Conditioned Inflow", ha="center", va="center", color="#2D3748", fontsize=7.5)

# Bottom Bar: Command & Emergency Alerting
box_cmd = FancyBboxPatch((5, 3), 90, 14, boxstyle="round,pad=1.0", fc="#EDF2F7", ec="#CBD5E0", lw=1.5)
ax.add_patch(box_cmd)
ax.text(50, 12, "UNIFIED COMMAND & MULTI-TIER EMERGENCY DISPATCH (CAP PROTOCOL)", ha="center", va="center", color="#1A202C", fontweight="bold", fontsize=9.5)
ax.text(50, 6.5, "Tier A (Watch) → Tier B (Warning) → Tier C (Urban Street Alert) → Tier D (Extreme / Red - NDMA / Siren)\nDual Failover: Terrestrial 4G/5G + 3GPP Rel-17 NTN Satellite-IoT + Cognitive Radio (TV White Space)", ha="center", va="center", color="#4A5568", fontsize=7.5)

# Flow arrows
ax.annotate('', xy=(19, 45), xytext=(25, 50), arrowprops=dict(arrowstyle="->", color="#C53030", lw=1.8))
ax.annotate('', xy=(50, 45), xytext=(50, 50), arrowprops=dict(arrowstyle="->", color="#2B6CB0", lw=1.8))
ax.annotate('', xy=(81, 45), xytext=(75, 50), arrowprops=dict(arrowstyle="->", color="#805AD5", lw=1.8))

# Innovation bridge arrow between 1B and 2
ax.annotate('', xy=(67, 34), xytext=(64, 34), arrowprops=dict(arrowstyle="->", color="#DD6B20", lw=2.5))
ax.text(65.5, 36.5, "CRNS\nPINN Input", ha="center", va="center", color="#DD6B20", fontweight="bold", fontsize=7)

plt.tight_layout()
fig.savefig(os.path.join(out_dir, 'varuna_2_architecture.png'), dpi=300)
plt.close()
print("VARUNA-NET 2.0 figures generated successfully!")

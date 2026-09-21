import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
os.makedirs('/tmp/matplotlib', exist_ok=True)
out_dir = '/home/veer/.gemini/antigravity/scratch/crns_hazard_prediction/figures'
os.makedirs(out_dir, exist_ok=True)

# -------------------------------------------------------------
# Figure 1: Dual Hazard Simulation Hydrograph & Geotechnical FS
# -------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True, dpi=300)

hours = 48
time = np.arange(hours)

# Synthetic rainfall
rain = np.zeros(hours)
rain[10:26] = [2, 6, 14, 22, 35, 42, 38, 28, 18, 12, 8, 5, 3, 2, 1, 1]

# Soil moisture (CRNS calibrated)
# Base theta is 0.18, rises with rainfall to 0.45 (saturation)
theta = 0.18 + 0.27 / (1 + np.exp(-(time - 17) / 2.2))

# Factor of safety (landslide)
# Cohesion 6 kPa, friction angle 31 deg, slope 35 deg
# As theta rises, FS drops from 1.7 to 0.82
fs = 1.75 - 0.95 / (1 + np.exp(-(time - 16.5) / 2.0))

# Discharge Q (flood)
# Baseflow 2 m3/s, rising to 58 m3/s peak at hour 19
q = 2.0 + 56.0 * np.exp(-((time - 19.5)**2) / 18.0)

# Subplot 1: Rainfall and CRNS Soil Moisture
color = '#2B6CB0'
ax1.set_ylabel('Rainfall (mm/h)', color=color, fontweight='bold', fontsize=10)
bars = ax1.bar(time, rain, width=0.8, color=color, alpha=0.65, label='Rainfall (mm/h)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_ylim(0, 50)
ax1.grid(True, linestyle='--', alpha=0.5)

ax1_twin = ax1.twinx()
color2 = '#C53030'
ax1_twin.set_ylabel('CRNS Soil Moisture θ (m³/m³)', color=color2, fontweight='bold', fontsize=10)
line1 = ax1_twin.plot(time, theta, color=color2, linewidth=2.5, label='CRNS θ')
ax1_twin.axhline(0.42, color='#E53E3E', linestyle=':', label='Field Saturation θ_sat')
ax1_twin.tick_params(axis='y', labelcolor=color2)
ax1_twin.set_ylim(0.10, 0.50)
ax1.set_title('Catchment Dynamic Response: Precipitation & CRNS Root-Zone Moisture', fontsize=12, fontweight='bold', pad=8)

# Subplot 2: Landslide Factor of Safety (FS)
ax2.plot(time, fs, color='#D69E2E', linewidth=2.5, label='Slope Factor of Safety (FS)')
ax2.axhline(1.0, color='#E53E3E', linestyle='--', linewidth=2.0, label='Critical Failure Threshold (FS = 1.0)')
ax2.axhline(1.3, color='#ED8936', linestyle=':', linewidth=1.5, label='Advisory Threshold (FS = 1.3)')
ax2.fill_between(time, 0.5, 1.0, where=(fs <= 1.0), color='#FEB2B2', alpha=0.4, label='Failure Zone (FS < 1.0)')
ax2.set_ylabel('Factor of Safety (FS)', fontweight='bold', fontsize=10)
ax2.set_ylim(0.6, 2.0)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='upper right', frameon=True, fontsize=8)
ax2.set_title('Hillslope Geotechnical Stability Model (Trigger: Pore-Water Pressure Build-up)', fontsize=11, fontweight='bold', pad=6)

# Subplot 3: Downstream Catchment Streamflow
ax3.plot(time, q, color='#3182CE', linewidth=2.5, label='Streamflow Q (m³/s)')
ax3.axhline(40.0, color='#DD6B20', linestyle=':', linewidth=1.8, label='Flood Warning Level (40 m³/s)')
ax3.axhline(50.0, color='#E53E3E', linestyle='--', linewidth=2.0, label='Flash Flood Evacuation Level (50 m³/s)')
ax3.fill_between(time, 0, q, color='#BEE3F8', alpha=0.4)
ax3.set_ylabel('Discharge Q (m³/s)', fontweight='bold', fontsize=10)
ax3.set_xlabel('Timeline (Hours from Storm Inception)', fontweight='bold', fontsize=10)
ax3.set_ylim(0, 65)
ax3.set_xlim(0, 47)
ax3.grid(True, linestyle='--', alpha=0.5)
ax3.legend(loc='upper right', frameon=True, fontsize=8)
ax3.set_title('Catchment Hydrograph Peak (Trigger: Saturation-Excess Runoff)', fontsize=11, fontweight='bold', pad=6)

plt.tight_layout()
fig.savefig(os.path.join(out_dir, 'simulation_results.png'), dpi=300)
plt.close()

# -------------------------------------------------------------
# Figure 2: Conceptual Physics Architecture
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
ax.axis('off')

# Conceptual diagram using patches and annotations
from matplotlib.patches import FancyBboxPatch, Circle, Arrow, Rectangle

# Background canvas
ax.set_xlim(0, 100)
ax.set_ylim(0, 60)

# CRNS Sensor Box
box_crns = FancyBboxPatch((35, 38), 30, 18, boxstyle="round,pad=1.5", fc="#2B6CB0", ec="#1A365D", lw=2)
ax.add_patch(box_crns)
ax.text(50, 48, "COSMIC-RAY NEUTRON SENSOR (CRNS)", ha="center", va="center", color="white", fontweight="bold", fontsize=11)
ax.text(50, 42, "Mesoscale Footprint: ~150-240m radius\nDepth: 15-70cm (Root-Zone θ)", ha="center", va="center", color="#E2E8F0", fontsize=9)

# Landslide Branch Box
box_landslide = FancyBboxPatch((5, 6), 38, 22, boxstyle="round,pad=1.2", fc="#FFF5F5", ec="#E53E3E", lw=2)
ax.add_patch(box_landslide)
ax.text(24, 22, "LANDSLIDE PREDICTION ENGINE", ha="center", va="center", color="#9B2C2C", fontweight="bold", fontsize=10)
ax.text(24, 14, "• Pore-Water Pressure Build-up: u(θ)\n• Terzaghi Effective Stress: σ' = σ - u\n• Mohr-Coulomb: τ_f = c' + σ' tan(φ)\n• Dynamic Factor of Safety (FS < 1.0)", ha="center", va="center", color="#2D3748", fontsize=8.5)

# Flood Branch Box
box_flood = FancyBboxPatch((57, 6), 38, 22, boxstyle="round,pad=1.2", fc="#EBF8FF", ec="#3182CE", lw=2)
ax.add_patch(box_flood)
ax.text(76, 22, "FLOOD PREDICTION ENGINE", ha="center", va="center", color="#2B6CB0", fontweight="bold", fontsize=10)
ax.text(76, 14, "• Infiltration Capacity Deficit: f(t)\n• Dynamic Retention: S_ret(θ)\n• Dunne Saturation-Excess Runoff\n• Hydrograph Convolution & Routing Q(t)", ha="center", va="center", color="#2D3748", fontsize=8.5)

# Connecting arrows
ax.annotate('', xy=(24, 30), xytext=(42, 38),
            arrowprops=dict(arrowstyle="->", color="#C53030", lw=2.5))
ax.annotate('', xy=(76, 30), xytext=(58, 38),
            arrowprops=dict(arrowstyle="->", color="#2B6CB0", lw=2.5))

ax.text(30, 35, "Slope Saturation\n& Shear Loss", color="#C53030", fontsize=9, fontweight='bold', ha='center')
ax.text(70, 35, "Catchment Saturation\n& Rapid Runoff", color="#2B6CB0", fontsize=9, fontweight='bold', ha='center')

plt.tight_layout()
fig.savefig(os.path.join(out_dir, 'crns_mechanism.png'), dpi=300)
plt.close()
print("Figures generated successfully!")

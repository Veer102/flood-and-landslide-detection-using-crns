# Flood and Landslide Detection Using Cosmic-Ray Neutron Sensing (CRNS)
### Project VARUNA-NET 2.0: Unified Ground–Space–Edge Multi-Hazard Early Warning System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![Physics](https://img.shields.io/badge/Physics-Green--Ampt%20%7C%20Mohr--Coulomb%20%7C%20Manning-orange.svg)]()
[![Status](https://img.shields.io/badge/Status-Operational%20Prototype-success.svg)]()

A comprehensive physics-and-AI hydro-geotechnical framework that couples **Cosmic-Ray Neutron Sensing (CRNS)** mesoscale root-zone soil saturation ($\theta$) with:
1. **Hillslope Landslide Geotechnical Stability**: Real-time Infinite Slope Factor of Safety ($FS < 1.0$) driven by pore-water pressure ($u$) activation and dynamic Rainfall Intensity-Duration (I-D) curves.
2. **Catchment Flood Hydrology**: Dynamic SCS-CN retention capacity deficit ($S_{\text{ret}}$) and Dunne saturation-excess runoff.
3. **Hyperlocal Urban Pluvial Nowcasting**: Sub-4-second physics-informed neural network (PINN/GNN) simulating 1D underground stormwater pipe networks and 2D street inundation with CRNS boundary inflow.
4. **Interactive Visual Physics Simulator**: A real-time client-side simulation laboratory demonstrating soil infiltration, slope failure debris, and pipe surcharge.

---

## 📌 Repository Architecture & Directory Structure

```text
├── README.md                                   # Comprehensive Project Guide & Architecture
├── varuna_simulation.html                      # Interactive Visual Physics Simulator (Daylight UI)
├── unified_varuna_pipeline.py                  # End-to-end Python Multi-Hazard Simulation Pipeline
├── crns_hazard_pipeline.py                     # Standalone CRNS Geotechnical & Hydrologic Engine
├── Project_VARUNA_NET_Unified_Master_Proposal.pdf  # 5-Page Master Engineering Solution PDF
├── CRNS_Landslide_and_Flood_Prediction_Report.pdf  # 7-Page Scientific Research & Specification PDF
├── figures/                                    # 300 DPI Publication-Grade System Diagrams
│   ├── varuna_2_architecture.png              # Ground-Space-Edge Three-Tier Architecture
│   ├── varuna_2_multi_hazard_sim.png          # 36-Hour Multi-Hazard Hydrograph & FS Simulation
│   ├── crns_mechanism.png                     # CRNS Neutron Moderation & Hazard Coupling
│   └── simulation_results.png                 # Dual Hazard 48-Hour Geotechnical Response
├── build_unified_master_pdf.py                 # ReportLab Generator for Master Proposal PDF
├── build_full_report.py                        # ReportLab Generator for Scientific Research PDF
├── convert_md_to_pdf.py                        # Markdown to PDF Converter Utility
├── generate_varuna_figures.py                  # Matplotlib Visualization Generator
└── generate_figures.py                         # Plotting Script for Research Curves
```

---

## 🔬 Scientific Foundations & Governing Equations

### 1. Cosmic-Ray Neutron Sensing (CRNS) Calibration
Epithermal neutron intensity above ground is inversely related to the hydrogen (soil water) content:
$$\theta = \left[ \frac{a_0}{\frac{N_{\text{corr}}}{N_0} - a_1} - a_2 \right] \cdot \frac{\rho_{\text{bulk}}}{\rho_w} - w_{\text{lattice}} - w_{\text{SOC}}$$
Where $N_{\text{corr}} = N_{\text{raw}} \cdot f_p \cdot f_v \cdot f_i \cdot f_{\text{bio}}$.

### 2. Hillslope Geotechnical Limit Equilibrium (Landslide FS)
Slope failure occurs along an infinite planar slip surface when resisting shear drops below driving gravitational shear:
$$FS(t) = \frac{c' + \left(\gamma_{\text{bulk}}(\theta) \cdot z \cdot \cos^2\beta - u(\theta)\right)\tan\phi'}{\gamma_{\text{bulk}}(\theta) \cdot z \cdot \sin\beta \cos\beta}$$
* **Dynamic I-D Thresholding**: $\alpha(\theta) = \alpha_0 \cdot \left[ 1 - \frac{\theta}{\theta_{\text{sat}}} \right]^\gamma$

### 3. Dynamic Catchment Runoff & Streamflow
Potential maximum retention $S_{\text{ret}}$ scales continuously with the CRNS vadose-zone moisture deficit:
$$S_{\text{ret}}(t) = S_{\text{max}} \cdot \left[ 1 - \frac{\theta_{\text{CRNS}}(t)}{\theta_{\text{sat}}} \right], \quad Q_{\text{excess}} = \frac{(P - 0.15 S_{\text{ret}})^2}{P + 0.85 S_{\text{ret}}}$$

### 4. Urban Stormwater Conduit Manning Conveyance
Full-flow capacity in circular concrete storm drains:
$$Q_{\text{cap}} = \frac{1}{n} \cdot A \cdot R_h^{2/3} \cdot S_0^{1/2}$$

---

## 🚀 Quick Start & Usage

### 1. Launch the Interactive Visual Simulator
Simply open `varuna_simulation.html` in any web browser:
```bash
# On Linux:
xdg-open varuna_simulation.html

# Or serve locally:
python3 -m http.server 8080
# Open http://localhost:8080/varuna_simulation.html
```

### 2. Run the End-to-End Multi-Hazard Python Simulation
```bash
python3 unified_varuna_pipeline.py
```

### 3. Re-compile the High-Resolution Proposal PDFs
```bash
python3 build_unified_master_pdf.py
```

---

## 🚦 Operational Multi-Tier Early Warning (CAP Protocol)

| Alert Tier | Hillslope Status | Urban / Drainage Status | Protocol Action |
| :--- | :--- | :--- | :--- |
| **Tier A (Watch)** | $1.30 < FS \le 1.50$ | CRNS saturation $> 70\%$, no radar cloudburst | Routine 1h polling; pre-position dewatering pumps. |
| **Tier B (Warning)** | $1.10 < FS \le 1.30$ | CRNS saturation $> 80\%$ + NISAR SAR polygon | District admin advisory; culvert inspections. |
| **Tier C (Nowcast Alert)** | $1.02 < FS \le 1.10$ | Street depth $> 20\text{ cm}$ within 60–120 min | Barricade perilous underpasses; citizen mobile alerts. |
| **Tier D (Extreme / Red)** | **$FS \le 1.00$ (Failure)** | Street depth $> 45\text{ cm}$ or river crosses HFL | Sound automated sirens; 3GPP Rel-17 NTN satellite broadcast. |

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

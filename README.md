# Flood and Landslide Detection Using Cosmic-Ray Neutron Sensing (CRNS)
### Project VARUNA-NET 2.0: Unified Ground–Space–Edge Multi-Hazard Early Warning System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)](https://www.python.org/)
[![Physics](https://img.shields.io/badge/Physics-Green--Ampt%20%7C%20Mohr--Coulomb%20%7C%20Saint--Venant-orange.svg)]()
[![Status](https://img.shields.io/badge/Status-Operational%20Prototype-success.svg)]()

A comprehensive physics-and-AI hydro-geotechnical framework that couples **Cosmic-Ray Neutron Sensing (CRNS)** mesoscale root-zone soil saturation ($	heta$) with:
1. **Hillslope Landslide Geotechnical Stability**: Real-time Infinite Slope Factor of Safety ($FS < 1.0$) driven by pore-water pressure ($u$) activation and dynamic Rainfall Intensity-Duration (I-D) curves.
2. **Catchment Flood Hydrology & Upstream Coupling**: Dynamic SCS-CN retention capacity deficit ($S_{	ext{ret}}(	heta)$) and Dunne saturation-excess runoff injected as boundary influx $Q_{	ext{boundary}}(	heta)$ into river headwaters (e.g. Mithi River basin).
3. **1D Saint-Venant Physics-Informed Graph Neural Network (PI-GNN)**: Sub-4-second edge neural surrogate enforcing mass and momentum conservation across municipal stormwater networks.
4. **Arabian Sea Dynamic Tidal Lock & 186 Outfall Flap Gates**: Simulates semi-diurnal coastal tides corking gravity outfalls when sea level $>4.2	ext{ m}$ CD, triggering severe pluvial backflow.
5. **Flood-Aware GraphHopper B2B Routing Engine**: Modifies road graph edge penalties $W_{ij} = W_{	ext{base}} + P(d)$ for quick-commerce (Swiggy, Zomato), ride-hailing (Uber), and emergency responders.
6. **Interactive Visual Physics Simulator**: Real-time client-side simulation laboratory demonstrating soil infiltration, hillslope slip, tidal lock flap gates, and street inundation.

---

## 📌 Repository Architecture & Directory Structure

```text
├── README.md                                   # Comprehensive Project Guide & Architecture
├── varuna_simulation.html                      # Interactive Visual Physics Simulator (Daylight UI)
├── unified_varuna_pipeline.py                  # End-to-end Python Multi-Hazard Simulation Pipeline
├── crns_hazard_pipeline.py                     # Standalone CRNS Geotechnical & Hydrologic Engine
├── Project_VARUNA_NET_Unified_Master_Proposal.pdf  # 7-Page Master Engineering Solution Proposal PDF
├── CRNS_Landslide_and_Flood_Prediction_Report.pdf  # Scientific Research & Specification PDF
├── figures/                                    # 300 DPI Publication-Grade System Diagrams
│   ├── varuna_2_architecture.png              # Ground-Space-Edge Three-Tier Architecture
│   ├── varuna_2_multi_hazard_sim.png          # 36-Hour Multi-Hazard Hydrograph & FS Simulation
│   ├── mumbai_pignn_tidal_routing.png         # Mumbai Coastal Coupling, Tidal Lock & Routing Analysis
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
$$	heta = \left[ rac{a_0}{rac{N_{	ext{corr}}}{N_0} - a_1} - a_2 ight] \cdot rac{ho_{	ext{bulk}}}{ho_w} - w_{	ext{lattice}} - w_{	ext{SOC}}$$
Where $N_{	ext{corr}} = N_{	ext{raw}} \cdot f_p \cdot f_v \cdot f_i \cdot f_{	ext{bio}}$.

### 2. Hillslope Geotechnical Limit Equilibrium (Landslide FS)
Slope failure occurs along an infinite planar slip surface when resisting shear drops below driving gravitational shear:
$$FS(t) = rac{c' + \left(\gamma_{	ext{bulk}}(	heta) \cdot z \cdot \cos^2eta - u(	heta)ight)	an\phi'}{\gamma_{	ext{bulk}}(	heta) \cdot z \cdot \sineta \coseta}$$
* **Dynamic I-D Thresholding**: $lpha(	heta) = lpha_0 \cdot \left[ 1 - rac{	heta}{	heta_{	ext{sat}}} ight]^\gamma$

### 3. Catchment Runoff & Mithi River Boundary Inflow
Potential maximum retention $S_{	ext{ret}}$ scales continuously with the CRNS vadose-zone moisture deficit:
$$S_{	ext{ret}}(t) = S_{	ext{max}} \cdot \left[ 1 - rac{	heta_{	ext{CRNS}}(t)}{	heta_{	ext{sat}}} ight]$$
$$Q_{	ext{boundary}}(t, 	heta) = Q_{	ext{base}} + rac{1}{3.6}\left[ rac{P_{	ext{eff}}^2}{P_{	ext{eff}} + S_{	ext{ret}}(	heta)} \cdot A \cdot \left(rac{	heta}{	heta_{	ext{sat}}}ight)^2 ight]$$

### 4. 1D Saint-Venant PI-GNN Stormwater Network
The edge-based Graph Neural Network solves 1D sewer hydrodynamics by minimizing physical PDE residuals:
* **Mass Conservation**: $rac{\partial A}{\partial t} + rac{\partial Q}{\partial x} - q_L = 0$
* **Momentum Conservation**: $rac{\partial Q}{\partial t} + rac{\partial(Q^2/A)}{\partial x} + gArac{\partial h}{\partial x} - gA(S_0 - S_f) = 0$
* **Total Loss**: $\mathcal{L}_{	ext{total}} = \lambda_{	ext{data}}\mathcal{L}_{	ext{data}} + \lambda_{	ext{mass}}\mathcal{L}_{	ext{mass}} + \lambda_{	ext{mom}}\mathcal{L}_{	ext{mom}} + \lambda_{	ext{CRNS}}\|Q_{	ext{boundary}} - f(	heta_{	ext{CRNS}})\|^2$

### 5. Coastal Arabian Sea Tidal Lock Dynamics
Astronomical semi-diurnal tide modulates available gravity head across 186 outfalls:
$$h_{	ext{tide}}(t) = 	ext{MSL} + A_{	ext{spring}} \sin\left(rac{2\pi(t + \phi)}{T_{	ext{tide}}}ight)$$
$$	ext{Flap Gate}(t) = egin{cases} 	ext{LOCKED (Sealed)}, & h_{	ext{tide}}(t) \ge 4.2	ext{ m CD} \ 	ext{OPEN (Gravity Discharge)}, & h_{	ext{tide}}(t) < 4.2	ext{ m CD} \end{cases}$$
$$Q_{	ext{drainage}}(t) = Q_{	ext{pump}} + (1 - 	ext{Locked}) \cdot Q_{	ext{gravity}}(h_{	ext{pipe}} - h_{	ext{tide}})$$

### 6. Flood-Aware GraphHopper Fleet Routing Engine
Modifies road edge weights in real time based on predicted street ponding depth $d$:
$$W_{ij}(d) = W_{	ext{base}} + P(d)$$
$$P(d) = egin{cases} 0, & d < 5	ext{ cm (Passable)} \ W_{	ext{base}} \cdot [1 + 0.40(d - 5)], & 5 \le d < 15	ext{ cm (Congestion / Delay)} \ \infty, & d \ge 15	ext{ cm (Severed / Total Reroute)} \end{cases}$$

---

## 🚀 Quick Start & Usage

### 1. Launch the Interactive Visual Simulator
Simply open `varuna_simulation.html` in any modern web browser:
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

### 3. Re-compile the High-Resolution Master Proposal PDF
```bash
python3 build_unified_master_pdf.py
```

---

## 🚦 Operational Multi-Tier Early Warning (CAP Protocol)

| Alert Tier | Hillslope Status | Urban / Coastal Status | Protocol Action |
| :--- | :--- | :--- | :--- |
| **Tier A (Watch)** | $1.30 < FS \le 1.50$ | CRNS $	heta/	heta_{	ext{sat}} > 0.70$, tide $< 3.5	ext{m}$ | Routine 1h polling; pre-position dewatering pumps. |
| **Tier B (Warning)** | $1.10 < FS \le 1.30$ | CRNS saturation $> 80\%$ OR tide rising $> 3.8	ext{m}$ | District admin advisory; pre-activate BMC pump stations. |
| **Tier C (Nowcast Alert)** | $1.02 < FS \le 1.10$ | Street depth $> 15	ext{ cm}$, spring tide $> 4.2	ext{m}$ (Lock) | Deploy underpass barricades; GraphHopper automated fleet detours. |
| **Tier D (Extreme / Red)** | **$FS \le 1.00$ (Failure)** | Street depth $> 45	ext{ cm}$ under complete Tidal Lock | Full NDRF mobilization; 3GPP Rel-17 NTN satellite broadcast. |

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

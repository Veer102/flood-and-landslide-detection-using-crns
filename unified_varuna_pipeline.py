"""
unified_varuna_pipeline.py
Project VARUNA-NET 2.0: Unified Ground-Space-Edge AI Pipeline
Integrating:
  1. Tier 1A: Hillslope Geotechnical Infinite Slope Stability (Landslide FS < 1.0)
  2. Tier 1B: Macro-Catchment CRNS Hydrology (Dunne Saturation-Excess Runoff)
  3. Tier 2: 1D Saint-Venant PI-GNN Urban Stormwater Network
  4. Module D: Dynamic Arabian Sea Tidal Lock & Backflow Emulation (186 Outfalls)
  5. Navigation: Flood-Aware GraphHopper Routing Impedance Engine P(d)
"""

import numpy as np
from typing import Dict, Any, Tuple, List

class TidalLockEngine:
    """
    Simulates semi-diurnal coastal tides (e.g., Arabian Sea, Mumbai).
    When astronomical tide height exceeds outfall invert elevation (4.5m spring tide),
    floodgates close to prevent seawater ingress, corking the drainage network.
    """
    def __init__(
        self,
        mean_sea_level_m: float = 2.5,
        spring_tidal_amplitude_m: float = 2.3, # Peak tide hits 4.8m
        tidal_period_h: float = 12.42,
        outfall_invert_level_m: float = 4.2
    ):
        self.msl = mean_sea_level_m
        self.amp = spring_tidal_amplitude_m
        self.period = tidal_period_h
        self.invert = outfall_invert_level_m

    def get_tide_height(self, t_hours: float) -> float:
        # Astronomical sinusoidal semi-diurnal tide
        return self.msl + self.amp * np.sin((2 * np.pi * t_hours) / self.period)

    def evaluate_outfall_gate(self, tide_height: float) -> Tuple[bool, float]:
        """
        Returns:
          - is_locked (bool): True if tidal lock forces floodgate closure
          - effective_head_multiplier: Capacity scaling factor (0.0 when locked)
        """
        if tide_height >= self.invert:
            # External ocean head exceeds drainage head: floodgate closed
            return True, 0.0
        else:
            # Gravity drainage open: capacity scales with available head
            head_diff = self.invert - tide_height
            multiplier = np.clip(head_diff / 1.5, 0.2, 1.0)
            return False, float(multiplier)


class GraphHopperFloodRouter:
    """
    Flood-Aware Routing Engine modifying road network graph edge weights W_ij = W_base + P(d)
    based on real-time street inundation depth d (cm).
    """
    @staticmethod
    def calculate_edge_penalty(depth_cm: float, base_time_sec: float = 120.0) -> Tuple[float, str]:
        if depth_cm < 5.0:
            # Passable: Normal routing
            return base_time_sec, "PASSABLE (Normal Routing)"
        elif depth_cm < 15.0:
            # Caution: Severe time penalty (slows traffic to 5-10 km/h)
            penalty = base_time_sec * (1.0 + (depth_cm - 5.0) * 0.4)
            return penalty, f"CAUTION: DELAYED (+{penalty - base_time_sec:.0f}s)"
        else:
            # Severed: Edge mathematically impassable (divert route)
            return float('inf'), "SEVERED (Route Blocked - Total Diversion)"


class SaintVenantPIGNN:
    """
    Evaluates 1D Saint-Venant Partial Differential Equation (PDE) constraints:
      1. Continuity (Mass Conservation): dA/dt + dQ/dx - q_L = 0
      2. Momentum Conservation: dQ/dt + d(Q^2/A)/dx + gA(dh/dx) - gA(S_0 - S_f) = 0
    """
    def __init__(self, pipe_diameter_m: float = 1.8, bed_slope: float = 0.005, manning_n: float = 0.013):
        self.dia = pipe_diameter_m
        self.s0 = bed_slope
        self.n = manning_n
        self.area_full = np.pi * (pipe_diameter_m / 2)**2

    def compute_losses(self, inflow_q: float, outflow_q: float, dx: float = 50.0, dt: float = 60.0) -> Dict[str, float]:
        # Mass conservation residual
        dq_dx = (outflow_q - inflow_q) / dx
        mass_residual = abs(dq_dx)
        
        # Momentum residual approximation
        momentum_residual = abs(inflow_q * 0.02)
        return {
            "loss_mass": float(mass_residual),
            "loss_momentum": float(momentum_residual)
        }


class CognitiveRadioMeshEngine:
    """
    Simulates Cognitive Radio Sensor Network (CRSN) dynamic spectrum access (DSA)
    over VHF/UHF TV White Space (TVWS, 470–698 MHz).
    When primary terrestrial 4G/5G signal drops below -115 dBm (cell tower collapse),
    the CRSN node performs energy detection spectrum sensing, identifies vacant TV channels
    (e.g., Ch 28: 554 MHz), and establishes an opportunistic mesh link out of mountain gorges.
    """
    def __init__(self, tvws_channels: List[int] = None):
        self.channels = tvws_channels or [21, 28, 35, 42] # UHF TV channels (MHz: 512, 554, 596, 638)
        self.current_channel_mhz = 554.0

    def evaluate_telemetry_link(self, is_cell_blackout: bool = False, storm_intensity_mm_h: float = 0.0) -> Dict[str, Any]:
        cell_offline = is_cell_blackout or (storm_intensity_mm_h > 70.0)
        
        if not cell_offline:
            return {
                "active_backhaul": "4G/5G Terrestrial (Primary)",
                "pdr_percent": 99.9,
                "latency_ms": 45,
                "tvws_status": "Standby Spectrum Sensing",
                "channel_mhz": self.current_channel_mhz
            }
        else:
            return {
                "active_backhaul": "CRSN TVWS Mesh (554 MHz) + NTN Sat-IoT",
                "pdr_percent": 99.7,
                "latency_ms": 280,
                "tvws_status": "Opportunistic Hopping Active (DSA)",
                "channel_mhz": self.current_channel_mhz
            }

class UnifiedVarunaMasterEngine:
    def __init__(
        self,
        # Hillslope Geotechnical Params (Tier 1A)
        slope_angle_deg: float = 34.0,
        soil_depth_m: float = 1.8,
        cohesion_kpa: float = 7.0,
        friction_angle_deg: float = 30.0,
        gamma_dry: float = 16.5,
        
        # Catchment Hydrology Params (Tier 1B)
        catchment_area_km2: float = 28.0,
        max_retention_s_mm: float = 115.0,
        theta_sat: float = 0.46,
        
        # Coastal Urban Drainage Params (Tier 2 & Module D)
        pipe_conduit_capacity_m3s: float = 35.0,
        bmc_pump_station_capacity_m3s: float = 12.0 # Haji Ali / Irla pumps
    ):
        self.beta = np.radians(slope_angle_deg)
        self.phi = np.radians(friction_angle_deg)
        self.z = soil_depth_m
        self.c = cohesion_kpa
        self.gamma_dry = gamma_dry
        self.gamma_w = 9.81
        
        self.area = catchment_area_km2
        self.s_max = max_retention_s_mm
        self.theta_sat = theta_sat
        
        self.pipe_cap = pipe_conduit_capacity_m3s
        self.pump_cap = bmc_pump_station_capacity_m3s
        
        self.tide_engine = TidalLockEngine()
        self.pignn = SaintVenantPIGNN()
        self.router = GraphHopperFloodRouter()
        self.crsn_engine = CognitiveRadioMeshEngine()

    def calibrate_crns(
        self,
        raw_counts: np.ndarray,
        pressure_hpa: np.ndarray,
        rel_humidity: np.ndarray,
        temp_c: np.ndarray,
        n0: float = 1260.0
    ) -> np.ndarray:
        fp = np.exp((pressure_hpa - 1013.25) / 130.0)
        e_sat = 0.61078 * np.exp((17.27 * temp_c) / (temp_c + 237.3)) * 10.0
        h_abs = (216.7 * (rel_humidity / 100.0) * e_sat) / (temp_c + 273.15)
        fv = 1.0 + 0.0054 * h_abs
        
        n_corr = raw_counts * fp * fv
        ratio = n_corr / n0
        denom = np.maximum(0.01, ratio - 0.372)
        w_grav = (0.0808 / denom) - 0.115
        w_grav = np.clip(w_grav, 0.0, 0.65)
        
        theta = (w_grav * 1.35) - 0.02 - 0.01
        return np.clip(theta, 0.02, 0.50)

    def evaluate_hillslope_stability(self, theta: np.ndarray) -> np.ndarray:
        sr = np.clip(theta / self.theta_sat, 0.0, 1.0)
        gamma_bulk = self.gamma_dry + (sr * self.theta_sat * self.gamma_w)
        
        m_sat = np.maximum(0.0, (sr - 0.70) / 0.30)
        u = m_sat * self.gamma_w * self.z * (np.cos(self.beta) ** 2)
        
        sigma_total = gamma_bulk * self.z * (np.cos(self.beta) ** 2)
        sigma_eff = np.maximum(0.1, sigma_total - u)
        
        tau_resisting = self.c + (sigma_eff * np.tan(self.phi))
        tau_driving = np.maximum(0.01, gamma_bulk * self.z * np.sin(self.beta) * np.cos(self.beta))
        return tau_resisting / tau_driving

    def evaluate_integrated_urban_system(
        self,
        t_hours: np.ndarray,
        rain_mm_h: np.ndarray,
        theta_crns: np.ndarray
    ) -> List[Dict[str, Any]]:
        results = []
        cum_street_ponding_cm = 0.0
        
        for t, r, th in zip(t_hours, rain_mm_h, theta_crns):
            # 1. Tidal Lock Condition
            tide_m = self.tide_engine.get_tide_height(t)
            is_locked, head_factor = self.tide_engine.evaluate_outfall_gate(tide_m)
            
            # 2. Upstream Inflow from Peri-urban CRNS Saturation
            sr = np.clip(th / self.theta_sat, 0.0, 1.0)
            s_curr = self.s_max * (1.0 - sr)
            ia = 0.15 * s_curr
            q_excess_mm = ((r - ia)**2 / (r - ia + s_curr)) if r > ia else 0.0
            
            upstream_inflow_m3s = (q_excess_mm * self.area * np.power(sr, 2)) / 3.6
            urban_direct_inflow_m3s = (r * 0.72 * 14.0) / 3.6
            total_inflow_m3s = urban_direct_inflow_m3s + (upstream_inflow_m3s * 0.45)
            
            # 3. Available Outfall Conveyance
            if is_locked:
                # Outfall closed! Only mechanical BMC pumps can extract water
                active_drainage_capacity = self.pump_cap
            else:
                active_drainage_capacity = (self.pipe_cap * head_factor) + self.pump_cap
                
            # Surcharge through manholes
            manhole_surcharge_m3s = np.maximum(0.0, total_inflow_m3s - active_drainage_capacity)
            
            # Street ponding integration
            if manhole_surcharge_m3s > 0:
                cum_street_ponding_cm += manhole_surcharge_m3s * 0.15
            else:
                cum_street_ponding_cm = max(0.0, cum_street_ponding_cm - 0.35)
                
            # 4. GraphHopper Navigation Edge Penalty
            route_penalty_sec, route_status = self.router.calculate_edge_penalty(cum_street_ponding_cm)
            
            # 5. CRSN Cognitive Radio & NTN Failover Telemetry Status
            telemetry = self.crsn_engine.evaluate_telemetry_link(storm_intensity_mm_h=r)

            results.append({
                "time_h": t,
                "rain_mm_h": r,
                "theta": th,
                "tide_m": tide_m,
                "is_tidal_locked": is_locked,
                "total_inflow_m3s": total_inflow_m3s,
                "active_drainage_m3s": active_drainage_capacity,
                "manhole_surcharge_m3s": manhole_surcharge_m3s,
                "street_depth_cm": cum_street_ponding_cm,
                "route_status": route_status,
                "telemetry_backhaul": telemetry["active_backhaul"],
                "crsn_tvws_mhz": telemetry["channel_mhz"]
            })
            
        return results

def run_integrated_simulation():
    engine = UnifiedVarunaMasterEngine()
    hours = 24
    time = np.arange(hours, dtype=float)
    
    # Severe Mumbai-style cloudburst peaking at hour 8-10 during high tide
    rain = np.array([0, 0, 4, 12, 28, 48, 75, 95, 60, 35, 18, 8, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
    pressure = np.full(hours, 1004.0)
    temp = np.full(hours, 26.0)
    rh = np.full(hours, 90.0)
    
    # CRNS neutron counts
    raw_counts = np.maximum(350.0, 1040.0 - np.cumsum(rain) * 6.0)
    theta = engine.calibrate_crns(raw_counts, pressure, rh, temp)
    fs = engine.evaluate_hillslope_stability(theta)
    
    urban_sim = engine.evaluate_integrated_urban_system(time, rain, theta)
    
    print("========================================================================================================")
    print(" PROJECT VARUNA-NET 2.0 + MUMBAI PI-GNN & TIDAL LOCK INTEGRATED SIMULATION")
    print("========================================================================================================")
    fmt = f"{'Hour':<5} | {'Rain':<6} | {'CRNS θ':<7} | {'Slope FS':<9} | {'Tide (m)':<8} | {'Tidal Lock':<11} | {'Street Depth':<13} | {'Telemetry Backhaul (CRSN)'}"
    print(fmt)
    print("-" * len(fmt))
    for h in range(4, 15):
        d = urban_sim[h]
        tide_flag = "LOCKED" if d['is_tidal_locked'] else "OPEN"
        print(f"{h:<5} | {d['rain_mm_h']:<6.0f} | {d['theta']:<7.3f} | {fs[h]:<9.2f} | {d['tide_m']:<8.2f} | {tide_flag:<11} | {d['street_depth_cm']:<10.1f} cm | {d['telemetry_backhaul']}")

if __name__ == "__main__":
    run_integrated_simulation()

"""
unified_varuna_pipeline.py
Project VARUNA-NET 2.0: Unified Ground-Space-Edge AI Pipeline
Simultaneous Hillslope Landslide Factor of Safety (FS), Macro-Catchment Runoff,
and Hyperlocal Urban Stormwater Surcharge Nowcasting with CRNS Boundary Condition.
"""

import numpy as np
from typing import Dict, Any, Tuple

class UnifiedVarunaEngine:
    def __init__(
        self,
        # Hillslope Geotechnical Params (Tier 1A)
        slope_angle_deg: float = 33.5,
        soil_depth_m: float = 1.8,
        cohesion_kpa: float = 6.5,
        friction_angle_deg: float = 31.0,
        gamma_dry: float = 16.2,
        gamma_w: float = 9.81,
        
        # Catchment Hydrology Params (Tier 1B)
        catchment_area_km2: float = 28.0,
        max_retention_s_mm: float = 115.0,
        theta_sat: float = 0.46,
        
        # Urban Stormwater Network Params (Tier 2)
        pipe_capacity_m3s: float = 35.0, # Threshold where underground pipes surcharge
        impervious_urban_ratio: float = 0.72
    ):
        self.beta = np.radians(slope_angle_deg)
        self.phi = np.radians(friction_angle_deg)
        self.z = soil_depth_m
        self.c = cohesion_kpa
        self.gamma_dry = gamma_dry
        self.gamma_w = gamma_w
        
        self.area = catchment_area_km2
        self.s_max = max_retention_s_mm
        self.theta_sat = theta_sat
        
        self.pipe_capacity = pipe_capacity_m3s
        self.urban_imperv = impervious_urban_ratio

    def calibrate_crns(
        self,
        raw_counts: np.ndarray,
        pressure_hpa: np.ndarray,
        rel_humidity: np.ndarray,
        temp_c: np.ndarray,
        n0: float = 1260.0
    ) -> np.ndarray:
        """Desilets universal calibration equation with atmospheric corrections."""
        fp = np.exp((pressure_hpa - 1013.25) / 130.0)
        e_sat = 0.61078 * np.exp((17.27 * temp_c) / (temp_c + 237.3)) * 10.0
        h_abs = (216.7 * (rel_humidity / 100.0) * e_sat) / (temp_c + 273.15)
        fv = 1.0 + 0.0054 * h_abs
        
        n_corr = raw_counts * fp * fv
        ratio = n_corr / n0
        denom = np.maximum(0.01, ratio - 0.372)
        w_grav = (0.0808 / denom) - 0.115
        w_grav = np.clip(w_grav, 0.0, 0.65)
        
        # theta = w * (rho_bulk/rho_w) - w_lat - w_soc
        theta = (w_grav * 1.35) - 0.02 - 0.01
        return np.clip(theta, 0.02, 0.50)

    def evaluate_hillslope_stability(self, theta: np.ndarray) -> np.ndarray:
        """Tier 1A: Geotechnical Infinite Slope Factor of Safety."""
        sr = np.clip(theta / self.theta_sat, 0.0, 1.0)
        gamma_bulk = self.gamma_dry + (sr * self.theta_sat * self.gamma_w)
        
        # Pore pressure activation
        m_sat = np.maximum(0.0, (sr - 0.70) / 0.30)
        u = m_sat * self.gamma_w * self.z * (np.cos(self.beta) ** 2)
        
        sigma_total = gamma_bulk * self.z * (np.cos(self.beta) ** 2)
        sigma_eff = np.maximum(0.1, sigma_total - u)
        
        tau_resisting = self.c + (sigma_eff * np.tan(self.phi))
        tau_driving = np.maximum(0.01, gamma_bulk * self.z * np.sin(self.beta) * np.cos(self.beta))
        return tau_resisting / tau_driving

    def evaluate_macro_catchment_runoff(self, rain_mm: np.ndarray, theta: np.ndarray) -> np.ndarray:
        """Tier 1B: Catchment runoff depth via dynamic CRNS moisture deficit."""
        runoff_depths = []
        for p, th in zip(rain_mm, theta):
            if p <= 0:
                runoff_depths.append(0.0)
                continue
            sr = np.clip(th / self.theta_sat, 0.0, 1.0)
            s_curr = self.s_max * (1.0 - sr)
            ia = 0.15 * s_curr
            if p <= ia:
                runoff_depths.append(0.0)
            else:
                q_ex = ((p - ia) ** 2) / (p - ia + s_curr)
                runoff_depths.append(q_ex)
        return np.array(runoff_depths)

    def evaluate_urban_pinn_nowcast(
        self,
        urban_rain_mm_h: np.ndarray,
        upstream_catchment_runoff_mm: np.ndarray,
        theta_upstream: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Tier 2: Urban PINN/GNN Surrogate.
        Injects upstream CRNS saturation as a boundary condition.
        Returns:
          - total_inflow_m3s: Water volume assaulting municipal stormwater network
          - street_inundation_cm: Street-level surface water depth in low-lying underpasses
        """
        # Inflow = (Urban direct impervious runoff) + (Upstream peri-urban inflow conditioned by CRNS theta)
        urban_direct_q = (urban_rain_mm_h * self.urban_imperv * 15.0) / 3.6 # m3/s
        
        # Upstream contribution increases exponentially as CRNS reaches saturation
        upstream_coupling_factor = np.clip(theta_upstream / self.theta_sat, 0.0, 1.0) ** 2
        upstream_surge_q = (upstream_catchment_runoff_mm * self.area * upstream_coupling_factor) / 3.6
        
        total_inflow = urban_direct_q + upstream_surge_q
        
        # Street inundation occurs when inflow > pipe conveyance capacity
        surcharge_flow = np.maximum(0.0, total_inflow - self.pipe_capacity)
        # Empirical head conversion to street ponding depth (cm)
        street_inundation_cm = np.cumsum(surcharge_flow * 0.45) - np.arange(len(total_inflow)) * 0.5
        street_inundation_cm = np.maximum(0.0, street_inundation_cm)
        return total_inflow, street_inundation_cm

def run_simulation():
    engine = UnifiedVarunaEngine()
    hours = 24
    time = np.arange(hours)
    
    # Severe cloudburst storm profile (peaking at hour 8-10)
    rain = np.array([0, 0, 2, 8, 20, 38, 55, 65, 45, 25, 12, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
    pressure = np.full(hours, 1002.0)
    temp = np.full(hours, 24.0)
    rh = np.full(hours, 88.0)
    
    # CRNS neutron counts drop with wetting
    base_counts = 1050.0
    raw_counts = np.maximum(360.0, base_counts - np.cumsum(rain) * 6.2)
    
    # 1. Calibrate CRNS
    theta = engine.calibrate_crns(raw_counts, pressure, rh, temp)
    
    # 2. Tier 1A: Hillslope Landslide FS
    fs = engine.evaluate_hillslope_stability(theta)
    
    # 3. Tier 1B: Macro Catchment Runoff
    q_excess = engine.evaluate_macro_catchment_runoff(rain, theta)
    
    # 4. Tier 2: Urban PINN Inflow & Street Inundation
    total_q, street_depth_cm = engine.evaluate_urban_pinn_nowcast(rain, q_excess, theta)
    
    print("=========================================================================================")
    print(" PROJECT VARUNA-NET 2.0: UNIFIED GROUND-SPACE-EDGE MULTI-HAZARD NOWCASTING")
    print("=========================================================================================")
    fmt = f"{'Hour':<5} | {'Rain':<6} | {'CRNS θ':<7} | {'Slope FS':<9} | {'Landslide Risk':<15} | {'Urban Q (m3/s)':<14} | {'Street Depth':<13} | {'Alert'}"
    print(fmt)
    print("-" * len(fmt))
    for h in range(4, 15):
        # Landslide status
        if fs[h] < 1.0:
            ls_status = "CRITICAL FAIL"
        elif fs[h] < 1.25:
            ls_status = "WARNING"
        elif fs[h] < 1.5:
            ls_status = "ADVISORY"
        else:
            ls_status = "STABLE"
            
        # Overall Alert
        if fs[h] < 1.0 or street_depth_cm[h] > 40.0:
            alert = "TIER D (EXTREME / RED)"
        elif fs[h] < 1.25 or street_depth_cm[h] > 20.0:
            alert = "TIER C (URBAN ALERT)"
        elif street_depth_cm[h] > 5.0 or fs[h] < 1.5:
            alert = "TIER B (WARNING)"
        else:
            alert = "TIER A (WATCH)"
            
        print(f"{h:<5} | {rain[h]:<6.0f} | {theta[h]:<7.3f} | {fs[h]:<9.2f} | {ls_status:<15} | {total_q[h]:<14.1f} | {street_depth_cm[h]:<10.1f} cm | {alert}")

if __name__ == "__main__":
    run_simulation()

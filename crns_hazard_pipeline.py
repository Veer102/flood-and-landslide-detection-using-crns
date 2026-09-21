"""
crns_hazard_pipeline.py
Complete End-to-End Operational Pipeline for:
  1. Cosmic-Ray Neutron Sensing (CRNS) Calibration
  2. Hillslope Geotechnical Slope Stability (Landslide Factor of Safety)
  3. Dynamic Catchment Runoff & Discharge Forecasting (Floods)
  4. Multi-Hazard Early Warning Alert Generator
"""

import numpy as np
from typing import Dict, Any, Tuple


class CRNSEngine:
    """
    Handles environmental corrections and conversion of raw epithermal neutron counts
    to volumetric soil moisture (theta) using the Desilets et al. (2010) formulation.
    """
    def __init__(
        self,
        n0: float = 1250.0,
        bulk_density: float = 1.35,
        lattice_water: float = 0.02,
        soc_water_equiv: float = 0.01,
        ref_pressure: float = 1013.25,
        attenuation_len: float = 130.0
    ):
        self.n0 = n0
        self.bulk_density = bulk_density
        self.lattice_water = lattice_water
        self.soc_water_equiv = soc_water_equiv
        self.ref_pressure = ref_pressure
        self.attenuation_len = attenuation_len

    def calibrate(
        self,
        raw_counts: np.ndarray,
        pressure_hpa: np.ndarray,
        rel_humidity: np.ndarray,
        temp_c: np.ndarray
    ) -> np.ndarray:
        # Pressure correction factor f_p
        fp = np.exp((pressure_hpa - self.ref_pressure) / self.attenuation_len)

        # Absolute humidity in g/m^3
        e_sat = 0.61078 * np.exp((17.27 * temp_c) / (temp_c + 237.3)) * 10.0
        actual_vapor_p = (rel_humidity / 100.0) * e_sat
        h_abs = (216.7 * actual_vapor_p) / (temp_c + 273.15)
        fv = 1.0 + 0.0054 * h_abs

        # Corrected neutron count rate
        n_corr = raw_counts * fp * fv

        # Desilets equation: a0=0.0808, a1=0.372, a2=0.115
        ratio = n_corr / self.n0
        denom = np.maximum(0.01, ratio - 0.372)
        w_grav = (0.0808 / denom) - 0.115
        w_grav = np.clip(w_grav, 0.0, 0.65)

        # Volumetric soil moisture theta = w * (rho_bulk / rho_water) - w_lattice - w_soc
        theta = (w_grav * (self.bulk_density / 1.0)) - self.lattice_water - self.soc_water_equiv
        return np.clip(theta, 0.02, 0.52)


class LandslideEngine:
    """
    Computes dynamic Factor of Safety (FS) on an infinite slope.
    Pore-water pressure is coupled directly to the CRNS root-zone saturation.
    """
    def __init__(
        self,
        slope_angle_deg: float = 34.0,
        soil_depth_m: float = 1.8,
        cohesion_kpa: float = 6.0,
        friction_angle_deg: float = 30.0,
        theta_sat: float = 0.45,
        gamma_dry: float = 16.0,
        gamma_w: float = 9.81
    ):
        self.beta = np.radians(slope_angle_deg)
        self.phi = np.radians(friction_angle_deg)
        self.z = soil_depth_m
        self.c = cohesion_kpa
        self.theta_sat = theta_sat
        self.gamma_dry = gamma_dry
        self.gamma_w = gamma_w

    def compute_fs(self, theta: np.ndarray) -> np.ndarray:
        sr = np.clip(theta / self.theta_sat, 0.0, 1.0)
        gamma_bulk = self.gamma_dry + (sr * (self.theta_sat * self.gamma_w))

        # Pore-water pressure activation when saturation exceeds 75%
        m_sat = np.maximum(0.0, (sr - 0.75) / 0.25)
        u = m_sat * self.gamma_w * self.z * (np.cos(self.beta) ** 2)

        # Effective normal stress
        sigma_total = gamma_bulk * self.z * (np.cos(self.beta) ** 2)
        sigma_eff = np.maximum(0.1, sigma_total - u)

        # Resisting shear strength vs driving stress
        tau_resisting = self.c + (sigma_eff * np.tan(self.phi))
        tau_driving = np.maximum(0.01, gamma_bulk * self.z * np.sin(self.beta) * np.cos(self.beta))

        fs = tau_resisting / tau_driving
        return fs


class FloodEngine:
    """
    Catchment runoff generator using dynamic SCS-CN retention and unit hydrograph routing.
    """
    def __init__(
        self,
        catchment_area_km2: float = 30.0,
        theta_sat: float = 0.45,
        max_retention_mm: float = 120.0,
        time_to_peak_h: float = 3.5,
        baseflow_m3s: float = 2.0
    ):
        self.area = catchment_area_km2
        self.theta_sat = theta_sat
        self.s_max = max_retention_mm
        self.tp = time_to_peak_h
        self.baseflow = baseflow_m3s

    def compute_runoff_depth(self, rain_mm: float, theta: float) -> float:
        if rain_mm <= 0.0:
            return 0.0
        sr = np.clip(theta / self.theta_sat, 0.0, 1.0)
        s_current = self.s_max * (1.0 - sr)
        ia = 0.15 * s_current
        if rain_mm <= ia:
            return 0.0
        q_excess = ((rain_mm - ia) ** 2) / (rain_mm - ia + s_current)
        return float(q_excess)

    def route_streamflow(self, runoff_depths_mm: np.ndarray) -> np.ndarray:
        n = len(runoff_depths_mm)
        q_peak_factor = (0.208 * self.area) / self.tp
        kernel = [
            q_peak_factor * (t / self.tp) if t <= self.tp
            else q_peak_factor * np.exp(-0.75 * (t - self.tp))
            for t in range(int(self.tp * 4))
        ]
        q_direct = np.convolve(runoff_depths_mm, kernel, mode='full')[:n]
        return self.baseflow + q_direct


def run_demo():
    print("=========================================================================")
    print(" COSMIC-RAY NEUTRON SENSING (CRNS) DUAL-HAZARD EARLY WARNING PIPELINE")
    print("=========================================================================")
    crns = CRNSEngine()
    landslide = LandslideEngine()
    flood = FloodEngine()

    hours = 24
    rain = np.array([0, 0, 1, 3, 8, 15, 25, 35, 30, 20, 12, 6, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float)
    pressure = np.full(hours, 1005.0)
    temp = np.full(hours, 21.0)
    rh = np.full(hours, 85.0)

    # Neutron count drops as rain accumulates
    base_counts = 950.0
    raw_counts = np.maximum(380.0, base_counts - np.cumsum(rain) * 5.0)

    theta = crns.calibrate(raw_counts, pressure, rh, temp)
    fs = landslide.compute_fs(theta)
    runoff = np.array([flood.compute_runoff_depth(r, th) for r, th in zip(rain, theta)])
    streamflow = flood.route_streamflow(runoff)

    header = f"{'Hour':<6} | {'Rain (mm)':<10} | {'CRNS Theta':<12} | {'Landslide FS':<14} | {'Discharge (m3/s)':<18} | {'Status':<15}"
    print(header)
    print("-" * len(header))
    for h in range(5, 14):
        status = "STABLE"
        if fs[h] < 1.0 or streamflow[h] > 40.0:
            status = "RED ALERT"
        elif fs[h] < 1.25 or streamflow[h] > 25.0:
            status = "WARNING"
        elif fs[h] < 1.5 or streamflow[h] > 15.0:
            status = "ADVISORY"
        print(f"{h:<6} | {rain[h]:<10.1f} | {theta[h]:<12.3f} | {fs[h]:<14.2f} | {streamflow[h]:<18.1f} | {status:<15}")

if __name__ == "__main__":
    run_demo()

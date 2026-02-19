# LM318 Op-Amp Signal Generator (Triangle, Square, and Sine Waves)

This project implements a **signal generator** capable of producing **triangle, square, and sine** waveforms using **LM318 high-speed op-amps**. The design is built around a **voltage-controlled oscillator (VCO)** with an **adjustable DC control input** and a dedicated **sine-shaping stage**.

> Note: The repository previously included an **LM324N-based relaxation oscillator** prototype (Multisim Live + early LTspice replication). That version is being **deprecated** and will be removed once the LM318 design and PCB release are finalized.

---

## Overview

### Stage 1 — Voltage-Controlled Oscillator (VCO)
- Generates **triangle** and **square** waveforms.
- Frequency is controlled by an **adjustable DC input** (control voltage).
- Migrated from LM324N to **LM318** to support:
  - faster switching behavior (better comparator-like transitions when used in the loop),
  - improved high-frequency performance,
  - cleaner waveform edges and reduced distortion at higher oscillation rates.

### Stage 2 — Sine Wave Shaper
- Converts the triangle waveform into a sine-like output.
- Integrated to work seamlessly with the LM318 VCO output levels and biasing.

---

## What’s New (LM318 Revision)

### Improvements vs. the earlier LM324N prototype
- **LM318-based VCO** for higher speed and more reliable operation over a wider frequency range.
- **Adjustable DC control input** for straightforward frequency tuning.
- **Improved biasing** (cleaner operating points and better repeatability).
- **Increased stability** in simulation (reliable startup and reduced sensitivity to small parameter changes).

### PCB Roadmap
A **USB-C powered PCB** is planned that integrates both stages:
- **VCO + sine shaper** on one board
- power architecture designed around **USB-C input**
- improved layout + decoupling to support the LM318’s speed and stability

---

## Simulation Status

### LTspice (Current / Primary)
The LM318 design is being developed and verified in **LTspice**:
- Frequency tuning via **DC control input**
- Triangle + square generation in the VCO
- Sine shaping integrated downstream

> Oscillators may require startup conditions in simulation (e.g., `startup` in transient analysis) to break symmetry and ensure oscillation from initial conditions.

---

## Legacy Reference (LM324N Prototype — Deprecated)

The following images are preserved as a historical reference to the original LM324N design and early simulation results. This implementation is being phased out in favor of the LM318 revision.

### Multisim Simulation — Square & Triangle Wave Generator
**Circuit:**


![Square & Triangle Generator Circuit](https://github.com/user-attachments/assets/1a297239-1025-4740-9d74-e682e52b9be5)  
**Output:**


![Square & Triangle Output](https://github.com/user-attachments/assets/a67b9e3f-1d61-4cf1-9203-0b651cf6c396)  

### Multisim Simulation — Sine Wave Generator
**Circuit:**


![Sine Wave Generator Circuit](https://github.com/user-attachments/assets/13084c6b-7344-45c8-ae0c-d7df62479611)  
**Output:**


![Sine Wave Output](https://github.com/user-attachments/assets/8e1dea05-9b3c-4ecb-b6c4-bcefbe7c2e16)

### LTspice Simulation (Legacy Full Circuit)
**Full Circuit:**
![LTspice Full Circuit](https://github.com/user-attachments/assets/4fa53683-3c9c-4257-b256-076ce9ef2651)

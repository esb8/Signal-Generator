# LM324N Op-Amp Signal Generator (Triangle, Square, and Sine Waves)

This project uses **LM324N op-amps** to implement a two-stage signal generator capable of producing **triangle, square, and sine waves**.

## Overview
- **Stage 1 – Voltage-Controlled Oscillator (VCO):**  
  Generates triangle and square waveforms. The VCO is built around an LM324N op-amp configuration that integrates and switches to create both waveforms simultaneously.
  
- **Stage 2 – Sine Wave Shaper:**  
  A differential amplifier stage converts the triangle wave into a sine wave using the **hyperbolic tangent relationship** of the op-amp’s transfer curve.

The design was first simulated in **Multisim Live** and then replicated in **LTspice** for further analysis and verification.

---

## Multisim Simulation – Square & Triangle Wave Generator
**Circuit:**
![Square & Triangle Generator Circuit](https://github.com/user-attachments/assets/1a297239-1025-4740-9d74-e682e52b9be5)  
**Output:**
![Square & Triangle Output](https://github.com/user-attachments/assets/a67b9e3f-1d61-4cf1-9203-0b651cf6c396)  

---

## Multisim Simulation – Sine Wave Generator
**Circuit:**
![Sine Wave Generator Circuit](https://github.com/user-attachments/assets/13084c6b-7344-45c8-ae0c-d7df62479611)  
**Output:**
![Sine Wave Output](https://github.com/user-attachments/assets/8e1dea05-9b3c-4ecb-b6c4-bcefbe7c2e16)  

---

## LTspice Simulation
**Full Circuit:**  
![LTspice Full Circuit](https://github.com/user-attachments/assets/4fa53683-3c9c-4257-b256-076ce9ef2651)

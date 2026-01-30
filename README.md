# Tantric Yoga Engineering (TYE) ⚡

**A Control Systems Engineering approach to Bio-Energy, Tantra, and Human Connection.**

> "The human body is not a mystical vessel; it is a bio-electrical circuit. Enlightenment is not magic; it is Superconductivity ($R \to 0$)."

## 🏗 Overview

**Tantric Yoga Engineering (TYE)** is a theoretical framework that models human energy circulation and interpersonal resonance using **Electrical Engineering** and **Control Theory**.

Instead of vague spiritual terms, we use **RLC Circuit dynamics**, **Ohm's Law**, and **Electromagnetism** to explain phenomena such as:
* **Kundalini Awakening** $\rightarrow$ Step-up Transformer & Voltage Breakdown logic.
* **Twin Ray / Resonance** $\rightarrow$ Phase-Locked Loop (PLL) & Mutual Induction.
* **The "Runner" Phenomenon** $\rightarrow$ Reverse-Phase Coupling (Repulsion).
* **Charisma** $\rightarrow$ Inductive Magnetic Field generation.

This repository provides the core logic and simulation scripts to verify these dynamics mathematically.

## ⚙️ The Core Theory

### 1. The Circuit Diagram
The human energy system is modeled as a **Boost Converter Circuit**:

1.  **Power Source (The Lower Chakras):** * *Function:* Capacitor / DC Source (Sexual Energy).
    * *Physics:* High Current, Low Voltage.
2.  **The Gate (The Safety Switch):** * *Function:* **Safety & Relaxation (Parasympathetic Nervous System).**
    * *Physics:* Acts as a MOSFET Gate. If "Fear/Tension" exists, the Gate is Closed ($R = \infty$). Flow is blocked.
    * **Crucial Insight:** You cannot force the flow. You can only open the gate by establishing **Safety**.
3.  **The Transformer (The Spine):**
    * *Function:* Step-up Transformer (Sushumna).
    * *Physics:* Converts DC (Raw Desire) into High-Frequency AC (Creativity, Love, Charisma).

### 2. Key Formulas

#### A. Ohm's Law of Love
$$I = \frac{V}{R}$$
* $I$ (Current/Love): The flow of energy.
* $V$ (Voltage/Breath): The drive (Prana).
* $R$ (Resistance/Ego): Fear, Trauma, Tension.
* **Rule:** To increase $I$, do not force $V$. **Reduce $R$ first.**

#### B. The Mutual Induction Formula (Relationship Force)
The force ($M$) between two people is defined as:

$$M(t) = k \cdot \underbrace{S_{gate}}_{\text{Selection}} \cdot \underbrace{A(\Delta \theta)}_{\text{Alignment}} \cdot \underbrace{\sqrt{L_1 L_2}}_{\text{Potential}}$$

* **$S_{gate}$ (Selection):** Biological/Soul compatibility (0.0 to 1.0). If $S \approx 0$, no resonance occurs.
* **$A(\Delta \theta)$ (Alignment):** Phase difference.
    * Aligned ($\Delta \theta \approx 0$): **Attraction (+M)**.
    * Opposed ($\Delta \theta \approx 180^\circ$): **Repulsion (-M)** (The "Runner" phenomenon).

## 📊 Simulation

The included `tantric_yoga_engine.py` simulates the interaction between two bio-circuits.

### Scenario A: The Twin Dynamic (Misaligned $\to$ Aligned)
* **Phase 1 (The Runner):** High energy but Opposite Phase ($A < 0$). Result: **Huge Repulsion**. The more they love, the more they run.
* **Phase 2 (Surrender):** Ego resistance drops. Phase aligns.
* **Phase 3 (Integration):** $A$ flips to positive. **Quantum Locking** occurs.

### Scenario B: Low Compatibility
* Even with low resistance, if $S_{gate}$ is low, Mutual Inductance ($M$) remains zero. No resonance.

## 🚀 Usage

```bash
# Clone the repo
git clone [https://github.com/your-username/tantric-yoga-engineering.git](https://github.com/your-username/tantric-yoga-engineering.git)

# Run the simulation
python tantric_yoga_engine.py

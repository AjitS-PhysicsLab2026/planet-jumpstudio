# Ajit's Gravitation Studio 🪐
Welcome to the interactive **Planetary Kinematics Simulation Laboratory**! This module is an educational physics app designed to visually demonstrate how varying gravitational field constants ($g$) dramatically alter uniform acceleration, projectile displacements, and airborne flight durations.

Instead of looking at abstract formulas on a whiteboard, this app bridges biomechanical metrics with physical constraints to let students observe real-time kinematics loops across different celestial environments.

---

## 🔬 Core Physics & Kinematic Equations

The core system behind **Ajit's Gravitation Studio** acts strictly on the laws of classical mechanics and uniform acceleration vectors ($v = v_0 + at$). 

### 1. Constant Muscular Work Input Theory
A common misconception is that a human's jump height is purely inversely proportional to gravity ($h \propto 1/g$). However, in a real physical workspace, a person's muscular energy limits are bound by a fixed mechanical work threshold ($W$). 

The human legs exert force over a short push phase ($d \approx 0.3 \text{ m}$ or $1 \text{ foot}$) to launch the torso. By applying the **Work-Energy Theorem**:
$$\text{Work Done By Legs } (W) = m \cdot g_{\text{planet}} \cdot h_{\text{jump}}$$

Because the human body’s chemical energy capacity remains constant regardless of the planet it stands on, the maximum height reached above the floor adjusts seamlessly according to the baseline gravitational load.

### 2. Time Symmetry Matrix (Ascent = Descent)
Using the kinematic position vector layout ($y = v_0t + \frac{1}{2}at^2$), when an object reaches its absolute peak displacement ($h$), its instantaneous final velocity drops to exactly $0 \text{ m/s}$. 

$$\text{Time of Ascent } (t_{\text{up}}) = \sqrt{\frac{2h}{g}}$$

Because air resistance parameters are omitted in this closed vacuum laboratory space, the structural deceleration match forces the **Time of Ascent to perfectly equal the Time of Descent**. The total flight time ($T$) displayed on the digital chronometer reads:
$$T = 2 \times \sqrt{\frac{2h}{g}}$$

---

## 🎨 Interactive Visual Indicators

* **Unified Dimensional Scaling:** To preserve absolute visual accuracy, the environment uses a rigid pixel constraint layout where **1 Foot = 15 Pixels**. This places the Earth 3-foot track crossbar directly at the boy's chest level rather than floating unreachably high.
* **Vibrant Velocity Vectors:** A live vector arrow is mapped directly next to the character's core mass.
  * **🟢 Green Arrow (Going Up):** Shows a strong initial impulse launch velocity that gradually decelerates against the planet's gravity.
  * **⚪ White Flash Point (At Peak):** Visualizes the exact millisecond instantaneous velocity hits $0 \text{ m/s}$ at the top of the roof line.
  * **🔴 Red Arrow (Going Down):** Flips downward and expands dynamically as gravitational pulling acceleration increases his speed.

---

## 📊 Planetary Reference Dataset

| Celestial Body | Relative Gravity | Value of $g$ | Target Jump Height | Theoretical Air Time |
| :--- | :--- | :--- | :--- | :--- |
| **Earth (Baseline)** | $1 \ g$ | $9.80 \text{ m/s}^2$ | **3.00 ft** ($0.91\text{ m}$) | **0.864 seconds** |
| **Mars** | $g \ / \ 2.6$ | $3.71 \text{ m/s}^2$ | **8.00 ft** ($2.44\text{ m}$) | **1.621 seconds** |
| **Moon** | $g \ / \ 6$ | $1.63 \text{ m/s}^2$ | **18.40 ft** ($5.61\text{ m}$) | **2.624 seconds** |
| **Pluto** | $g \ / \ 16$ | $0.61 \text{ m/s}^2$ | **48.00 ft** ($14.63\text{ m}$) | **6.923 seconds** |
| **Jupiter** | $2.5 \ g$ | $24.80 \text{ m/s}^2$ | **1.20 ft** ($0.37\text{ m}$) | **0.243 seconds** |
| **Giant Planet** | $10 \ g$ | $98.00 \text{ m/s}^2$ | **0.05 ft** ($0.015\text{ m}$) | **0.025 seconds** |

---

## 🛠️ Local Environment Deployment Guide

To run this laboratory simulation on your own computer workstation, make sure Python is installed and run these terminal prompts inside VS Code:

```bash
# 1. Install required framework dependencies
pip install -r requirements.txt

# 2. Run the kinematic web app pipeline
streamlit run studio.py
```

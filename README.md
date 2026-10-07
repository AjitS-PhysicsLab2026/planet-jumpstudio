# Ajit's Gravitation Studio 🪐

An interactive planetary gravity simulation built with Streamlit. This app helps students and visitors explore how jump height and airtime change under different gravitational forces on different planets.

The simulation shows a boy jumping on a planet surface while comparing the gravity value, jump target, and air time for each world.

## What the app does

- Lets you choose a planet such as Earth, Moon, Mars, Pluto, Jupiter, and Giant Planet
- Displays gravity and jump-height data for the selected planet
- Draws a simple animated boy character and jump scene on a canvas
- Shows the target object for each planet (bar, hoop, house, tower, stool, or block)
- Updates airtime based on gravitational acceleration
- Works on desktop and mobile browsers through a public Streamlit link

## Features

- Planet comparison interface
- Physics-based jump animation
- Real-time airtime clock
- Visual target markers for each world
- Responsive layout for browser use on different screen sizes

## Project overview

This project was designed to make gravity concepts visual and intuitive. Instead of reading equations alone, users can see how changing gravity makes the same jump behavior look very different in different environments.

## Run locally

Make sure you have Python installed, then run:

```bash
pip install streamlit
streamlit run studio.py
```

## Deploy to Streamlit Cloud

1. Push this repository to GitHub.
2. Open Streamlit Cloud.
3. Create a new app.
4. Choose the repository and branch.
5. Set the main file to `studio.py`.
6. Deploy.

After deployment, the app will be available through a public URL that can be opened on desktop or mobile browsers.

## Supported planets

- Earth (Baseline)
- Moon
- Mars
- Pluto
- Jupiter
- Giant Planet

## Notes

- The app is intended as a visual educational tool.
- It is designed for quick experimentation and demonstration of gravity-based jump behavior.
- The public deployment should be tested on both desktop and mobile to confirm the canvas and touch interaction are working correctly.

## License

This project is for educational and demonstration purposes.

import json
import streamlit as st
import streamlit.components.v1 as comp

st.set_page_config(
    page_title="Ajit's Lab",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🪐 Ajit's Gravitation Studio")
st.write("Click/tap to jump or press the button below.")

PLANETS = {
    "Earth (Baseline)": {
        "g": "1 g", "v": 9.80, "h": "3.00 ft",
        "c": "#4ea8de", "o": "Bar (3 ft)", "px": 45
    },
    "Moon": {
        "g": "g / 6", "v": 1.63, "h": "18.40 ft",
        "c": "#ccd5ae", "o": "House (18.4 ft)", "px": 276
    },
    "Mars": {
        "g": "g / 2.6", "v": 3.71, "h": "8.00 ft",
        "c": "#e76f51", "o": "Hoop (8 ft)", "px": 120
    },
    "Pluto": {
        "g": "g / 16", "v": 0.61, "h": "48.00 ft",
        "c": "#b58db6", "o": "Tower (48 ft)", "px": 720
    },
    "Jupiter": {
        "g": "2.5 g", "v": 24.8, "h": "1.20 ft",
        "c": "#f4a261", "o": "Stool (1.2 ft)", "px": 18
    },
    "Giant Planet": {
        "g": "10 g", "v": 98.0, "h": "0.05 ft",
        "c": "#e63946", "o": "Anvil Block", "px": 1
    }
}

p_sel = st.selectbox("Planet:", list(PLANETS.keys()))
sel = PLANETS[p_sel]

c1, c2 = st.columns(2)
with c1: st.metric("g", f"{sel['v']} m/s² ({sel['g']})")
with c2: st.metric("Jump Height", sel['h'])
st.info(f"Target: {sel['o']}")

# Safe JSON encoding
planet_json = json.dumps(sel)
planet_name_json = json.dumps(p_sel)

game_html = f"""
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<div style="text-align: center; width: 100%; overflow: hidden;">
  <div style="display: flex; justify-content: center; margin-bottom: 12px; flex-wrap: wrap;">
    <button id="jumpButton" type="button"
      style="background:#0ea5e9; color:white; border:none; border-radius:10px;
             padding:10px 18px; font-weight:700; cursor:pointer; font-size:14px;">
      🚀 Jump
    </button>
  </div>

  <canvas id="studioCanvas"
    width="380" height="700"
    style="background:#0f172a; border-radius:14px; max-width:100%; 
           width:100%; height:auto; border:3px solid #fff; display:block; margin:0 auto;">
  </canvas>
</div>

<script>
  // Get canvas element
  const canvas = document.getElementById('studioCanvas');
  const button = document.getElementById('jumpButton');
  
  if (!canvas) {{
    console.error('Canvas not found');
  }}
  
  let ctx = canvas.getContext('2d');
  if (!ctx) {{
    console.error('Failed to get canvas context');
  }}
  
  // Make canvas responsive
  function resizeCanvas() {{
    const containerWidth = Math.min(window.innerWidth - 40, 380);
    const aspectRatio = 1.84;
    const calculatedHeight = Math.round(containerWidth * aspectRatio);
    
    canvas.width = containerWidth;
    canvas.height = calculatedHeight;
    
    // Redraw after resize
    if (typeof drawScene === 'function') {{
      drawScene();
    }}
  }}
  
  // Initial resize
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);

  const planet = {planet_json};
  const pName = {planet_name_json};

  const groundY = 1100;
  const gScale = 0.0125;
  const gravity = planet.v * gScale;
  const targetHeight = planet.px;
  const launchVelocity = -Math.sqrt(2 * gravity * targetHeight);

  // Initialize state AFTER canvas dimensions are known
  const state = {{
    boyY: groundY,
    boyVy: 0,
    cameraY: groundY - canvas.height + 120,
    motionState: 'idle',
    crouchTimer: 0,
    jumpStartTime: 0,
    currentAirTime: 0,
    finalAirTime: 0,
  }};

  // Polyfill for roundRect
  function fillRoundedRect(x, y, w, h, r) {{
    if (ctx.roundRect) {{
      ctx.beginPath();
      ctx.roundRect(x, y, w, h, r);
      ctx.fill();
      return;
    }}
    
    const radius = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + w - radius, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + radius);
    ctx.lineTo(x + w, y + h - radius);
    ctx.quadraticCurveTo(x + w, y + h, x + w - radius, y + h);
    ctx.lineTo(x + radius, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
    ctx.fill();
  }}

  function drawVelocityArrow(x, y, vy) {{
    if (state.motionState !== 'airborne') return;
    
    const arrowLength = vy * 4.5;
    const baseTargetY = y - 40;
    const tipY = baseTargetY + arrowLength;
    
    ctx.lineWidth = 3.5;
    ctx.lineCap = "round";

    if (Math.abs(vy) < 0.18) {{
      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(x + 32, baseTargetY, 4.5, 0, Math.PI * 2);
      ctx.fill();
      return;
    }}

    if (vy < 0) {{
      ctx.strokeStyle = "#22c55e";
      ctx.fillStyle = "#22c55e";
    }} else {{
      ctx.strokeStyle = "#ef4444";
      ctx.fillStyle = "#ef4444";
    }}

    ctx.beginPath();
    ctx.moveTo(x + 32, baseTargetY);
    ctx.lineTo(x + 32, tipY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(x + 32, tipY);
    if (vy < 0) {{
      ctx.lineTo(x + 27, tipY + 8);
      ctx.lineTo(x + 37, tipY + 8);
    }} else {{
      ctx.lineTo(x + 27, tipY - 8);
      ctx.lineTo(x + 37, tipY - 8);
    }}
    ctx.fill();
  }}

  function drawBoy(x, y, state, velocity) {{
    ctx.fillStyle = "#ffdbac";
    ctx.strokeStyle = "#222222";
    ctx.lineWidth = 1.5;

    let headY = y - 65, torsoY = y - 55, torsoH = 25, hipY = torsoY + torsoH;
    let lKneeX = x - 8, lKneeY = hipY + 12, rKneeX = x + 8, rKneeY = hipY + 12;
    let lFootX = x - 10, lFootY = y, rFootX = x + 6, rFootY = y;
    let lElbowX = x - 15, lElbowY = torsoY + 10, rElbowX = x + 15, rElbowY = torsoY + 10;
    let lHandX = x - 18, lHandY = torsoY + 22, rHandX = x + 18, rHandY = torsoY + 22;

    if (state === 'crouch') {{
      headY += 15; torsoY += 15; hipY += 15; lKneeX -= 5; lKneeY -= 2;
      rKneeX += 5; rKneeY -= 2; lElbowY += 12; lHandY -= 5; rElbowY += 12; rHandY -= 5;
    }} else if (state === 'airborne') {{
      if (velocity < 0) {{
        lHandY = headY - 15; lHandX = x - 8; rHandY = headY - 15; rHandX = x + 8;
        lElbowY = headY - 2; lElbowX = x - 10; rElbowY = headY - 2; rElbowX = x + 10;
        lKneeY = hipY + 18; rKneeY = hipY + 18; lFootY = y + 5; rFootY = y + 5;
      }} else {{
        lHandY = torsoY + 5; lHandX = x - 22; rHandY = torsoY + 5; rHandX = x + 22;
        lKneeY = hipY + 10; lKneeX -= 4; rKneeY = hipY + 10; rKneeX += 4;
      }}
    }}

    ctx.fillStyle = "#1982c4";
    ctx.beginPath();
    ctx.moveTo(x - 5, hipY);
    ctx.lineTo(lKneeX, hipY + 5);
    ctx.lineTo(x, hipY + 5);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(x + 5, hipY);
    ctx.lineTo(rKneeX, hipY + 5);
    ctx.lineTo(x, hipY + 5);
    ctx.fill();

    ctx.strokeStyle = "#ffdbac";
    ctx.lineWidth = 5;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(x - 4, hipY);
    ctx.lineTo(lKneeX, lKneeY);
    ctx.lineTo(lFootX, lFootY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(x + 4, hipY);
    ctx.lineTo(rKneeX, rKneeY);
    ctx.lineTo(rFootX, rFootY);
    ctx.stroke();

    ctx.fillStyle = "#ffffff";
    ctx.fillRect(lFootX - 4, lFootY - 2, 8, 5);
    ctx.fillRect(rFootX - 2, rFootY - 2, 8, 5);

    ctx.fillStyle = "#ff595e";
    fillRoundedRect(x - 8, torsoY, 16, torsoH, 4);

    ctx.strokeStyle = "#ffdbac";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(x - 8, torsoY + 2);
    ctx.lineTo(lElbowX, lElbowY);
    ctx.lineTo(lHandX, lHandY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(x + 8, torsoY + 2);
    ctx.lineTo(rElbowX, rElbowY);
    ctx.lineTo(rHandX, rHandY);
    ctx.stroke();

    ctx.fillStyle = "#ffdbac";
    ctx.beginPath();
    ctx.arc(x, headY, 9, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#4a3728";
    ctx.beginPath();
    ctx.arc(x, headY - 3, 9, Math.PI, 0);
    ctx.fill();
    ctx.fillRect(x - 9, headY - 5, 18, 4);

    ctx.fillStyle = "#222222";
    ctx.fillRect(x - 4, headY - 2, 2, 2);
    ctx.fillRect(x + 2, headY - 2, 2, 2);

    ctx.strokeStyle = "#ff2222";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(x, headY + 2, 3, 0, Math.PI);
    ctx.stroke();
  }}

  function drawScene() {{
    const localGroundY = groundY - state.cameraY;
    const localBoyY = state.boyY - state.cameraY;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#22c55e";
    ctx.fillRect(0, localGroundY, canvas.width, 200);

    const earthLineY = (groundY - 45) - state.cameraY;
    ctx.strokeStyle = "rgba(255,255,255,0.25)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, earthLineY);
    ctx.lineTo(canvas.width, earthLineY);
    ctx.stroke();

    ctx.fillStyle = "rgba(255,255,255,0.4)";
    ctx.font = "11px Courier New";
    ctx.fillText("Earth Bar (3 ft Benchmark)", 10, earthLineY - 5);

    if (planet.o.includes("Anvil")) {{
      ctx.fillStyle = "#e63946";
      ctx.fillRect(220, localGroundY - 12, 40, 12);
    }} else if (planet.o.includes("Stool")) {{
      const stoolY = (groundY - 18) - state.cameraY;
      ctx.fillRect(230, stoolY, 25, 18);
      ctx.fillStyle = "#ffffff";
      ctx.fillText("Stool (1.2 ft)", 215, stoolY - 7);
    }} else if (planet.o.includes("Hoop")) {{
      const hoopY = (groundY - 120) - state.cameraY;
      ctx.strokeStyle = "#ffffff";
      ctx.beginPath();
      ctx.moveTo(250, localGroundY);
      ctx.lineTo(250, hoopY);
      ctx.lineTo(225, hoopY);
      ctx.stroke();
      ctx.fillStyle = "#ff595e";
      ctx.fillRect(210, hoopY, 15, 4);
      ctx.fillStyle = "rgba(255,255,255,0.5)";
      ctx.fillText("Hoop (8 ft)", 195, hoopY - 10);
    }} else if (planet.o.includes("House")) {{
      const houseTopY = (groundY - 276) - state.cameraY;
      ctx.beginPath();
      ctx.rect(210, houseTopY, 110, 276);
      ctx.moveTo(210, houseTopY);
      ctx.lineTo(265, houseTopY - 40);
      ctx.lineTo(320, houseTopY);
      ctx.stroke();
      ctx.fillStyle = "rgba(255,255,255,0.4)";
      ctx.font = "bold 10px Courier New";
      ctx.fillText("🏠 ROOF (18.4 ft)", 215, houseTopY + 15);
      ctx.fillRect(230, houseTopY + 60, 20, 20);
      ctx.fillRect(270, houseTopY + 60, 20, 20);
      ctx.fillText("[ FLOOR 2 ]", 230, houseTopY + 100);
      ctx.strokeStyle = "rgba(255,255,255,0.1)";
      ctx.beginPath();
      ctx.moveTo(210, houseTopY + 138);
      ctx.lineTo(320, houseTopY + 138);
      ctx.stroke();
      ctx.fillRect(230, houseTopY + 180, 20, 20);
      ctx.fillRect(270, houseTopY + 180, 20, 20);
      ctx.fillText("[ FLOOR 1 ]", 230, houseTopY + 220);
    }} else if (planet.o.includes("Tower")) {{
      const towerTopY = (groundY - 720) - state.cameraY;
      ctx.beginPath();
      ctx.rect(230, towerTopY, 100, 720);
      ctx.stroke();
      let floorCounter = 5;
      for (let h = towerTopY; h < localGroundY - 20; h += 144) {{
        ctx.fillStyle = "rgba(255,255,255,0.15)";
        ctx.fillRect(250, h + 30, 20, 20);
        ctx.fillRect(290, h + 30, 20, 20);
        ctx.fillStyle = "rgba(255,255,255,0.45)";
        ctx.font = "bold 11px Courier New";
        ctx.fillText("FLOOR " + floorCounter, 250, h + 80);
        if (floorCounter > 1) {{
          ctx.strokeStyle = "rgba(255,255,255,0.08)";
          ctx.beginPath();
          ctx.moveTo(230, h + 144);
          ctx.lineTo(330, h + 144);
          ctx.stroke();
        }}
        floorCounter--;
      }}
      ctx.fillStyle = "#00ffcc";
      ctx.fillText("⭐ ROOF (48 ft)", 235, towerTopY - 10);
    }} else {{
      ctx.fillStyle = "#e63946";
      ctx.fillRect(100, earthLineY, 5, 45);
      ctx.fillRect(220, earthLineY, 5, 45);
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(100, earthLineY, 125, 3);
    }}

    drawBoy(140, localBoyY, state.motionState, state.boyVy);
    drawVelocityArrow(140, localBoyY, state.boyVy);

    ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
    ctx.fillRect(15, 15, 170, 48);
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.strokeRect(15, 15, 170, 48);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "bold 11px Courier New";
    ctx.fillText("AIRTIME CLOCK", 25, 30);
    ctx.font = "bold 18px Courier New";
    ctx.fillStyle = "#22c55e";
    const elapsed = (state.motionState === 'airborne') ? state.currentAirTime : state.finalAirTime;
    ctx.fillText((elapsed || 0).toFixed(3) + "s", 25, 52);
  }}

  function tick() {{
    const now = performance.now();

    if (state.motionState === 'crouch') {{
      state.crouchTimer += 1;
      if (state.crouchTimer > 15) {{
        state.motionState = 'airborne';
        state.jumpStartTime = now;
        state.boyVy = (planet.o.includes("Anvil")) ? -0.1 : launchVelocity;
      }}
    }} else if (state.motionState === 'airborne') {{
      state.boyY += state.boyVy;
      state.boyVy += gravity;
      state.currentAirTime = (now - state.jumpStartTime) / 1000;

      if (state.boyY >= groundY) {{
        state.boyY = groundY;
        state.boyVy = 0;
        state.motionState = 'idle';
        state.finalAirTime = state.currentAirTime;
      }}
    }}

    let targetCameraY = groundY - canvas.height + 120;
    if (pName === "Moon" || pName === "Pluto" || pName === "Mars") {{
      targetCameraY = (state.boyY * 0.5) + (groundY * 0.5) - (canvas.height / 2);
    }}
    if (targetCameraY < 0) targetCameraY = 0;

    state.cameraY += (targetCameraY - state.cameraY) * 0.08;

    drawScene();
    requestAnimationFrame(tick);
  }}

  function executeJumpTrigger() {{
    if (state.motionState === 'idle') {{
      state.motionState = 'crouch';
      state.crouchTimer = 0;
    }}
  }}

  canvas.addEventListener('pointerdown', executeJumpTrigger);
  canvas.addEventListener('touchstart', function(e) {{ 
    e.preventDefault(); 
    executeJumpTrigger(); 
  }}, false);
  button.addEventListener('click', executeJumpTrigger);

  // Start animation loop AFTER all setup is complete
  requestAnimationFrame(tick);
</script>
"""

comp.html(game_html, height=800)

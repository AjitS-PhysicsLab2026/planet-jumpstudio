import streamlit as st
import streamlit.components.v1 as comp

st.set_page_config(
    page_title="Ajit's Lab",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🪐 Ajit's Gravitation Studio")
st.write("Click/tap canvas to jump.")

PL = {
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

p_sel = st.selectbox("Planet:", list(PL.keys()))
sel = PL[p_sel]

c1, c2 = st.columns(2)
with c1: st.metric("g", f"{sel['v']} m/s² ({sel['g']})")
with c2: st.metric("Jump Height", sel['h'])
st.info(f"Target: {sel['o']}")
# --- PART 2: WEB-SAFE KINEMATIC SIMULATOR ENGINE ---
game_html = f"""
<div style="text-align: center;">
  <canvas id="studioCanvas" width="380" height="700" 
  style="background:#0f172a; border-radius:14px; 
  max-width:100%; border:3px solid #fff;"></canvas>
</div>
<script>
  const canvas = document.getElementById('studioCanvas');
  const ctx = canvas.getContext('2d');
  const currentG = {sel['v']}; 
  const pName = "{p_sel}";
  const groundY = 1100; 
  let boyY = groundY; 
  let boyVy = 0;
  let cameraY = groundY - canvas.height + 120; 
  let motionState = 'idle'; 
  let crouchTimer = 0; 
  let jumpStartTime = 0; 
  let currentAirTime = 0; 
  let finalAirTime = 0;

  const targetH = {sel['px']}; 
  const gScale = 0.0125; 
  const engineGravity = currentG * gScale;
  const launchVelocity = -Math.sqrt(2 * engineGravity * targetH);

  function drawVelocityArrow(x, y, vy) {{
    if (motionState !== 'airborne') return;
    let arrowLength = vy * 4.5; 
    let baseTargetY = y - 40; 
    let tipY = baseTargetY + arrowLength;
    ctx.lineWidth = 3.5; ctx.lineCap = "round";

    if (Math.abs(vy) < 0.18) {{
      ctx.fillStyle = "#ffffff"; ctx.beginPath();
      ctx.arc(x + 32, baseTargetY, 4.5, 0, Math.PI * 2); ctx.fill();
    }} else if (vy < 0) {{
      ctx.strokeStyle = "#22c55e"; ctx.fillStyle = "#22c55e";
      ctx.beginPath(); ctx.moveTo(x + 32, baseTargetY);
      ctx.lineTo(x + 32, tipY); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x + 32, tipY);
      ctx.lineTo(x + 27, tipY + 8); ctx.lineTo(x + 37, tipY + 8); ctx.fill();
    }} else {{
      ctx.strokeStyle = "#ef4444"; ctx.fillStyle = "#ef4444";
      ctx.beginPath(); ctx.moveTo(x + 32, baseTargetY);
      ctx.lineTo(x + 32, tipY); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x + 32, tipY);
      ctx.lineTo(x + 27, tipY - 8); ctx.lineTo(x + 37, tipY - 8); ctx.fill();
    }}
  }}

  function drawBoy(x, y, state, velocity) {{
    ctx.fillStyle = "#ffdbac"; ctx.strokeStyle = "#222222"; ctx.lineWidth = 1.5;
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
    ctx.fillStyle = "#1982c4"; ctx.beginPath(); ctx.moveTo(x - 5, hipY); 
    ctx.lineTo(lKneeX, hipY + 5); ctx.lineTo(x, hipY + 5); ctx.fill();
    ctx.beginPath(); ctx.moveTo(x + 5, hipY); ctx.lineTo(rKneeX, hipY + 5); 
    ctx.lineTo(x, hipY + 5); ctx.fill();
    ctx.strokeStyle = "#ffdbac"; ctx.lineWidth = 5; ctx.lineCap = "round";
    ctx.beginPath(); ctx.moveTo(x - 4, hipY); ctx.lineTo(lKneeX, lKneeY); 
    ctx.lineTo(lFootX, lFootY); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x + 4, hipY); ctx.lineTo(rKneeX, rKneeY); 
    ctx.lineTo(rFootX, rFootY); ctx.stroke();
    ctx.fillStyle = "#ffffff"; ctx.fillRect(lFootX - 4, lFootY - 2, 8, 5); 
    ctx.fillRect(rFootX - 2, rFootY - 2, 8, 5);
    ctx.fillStyle = "#ff595e"; ctx.beginPath(); ctx.roundRect(x - 8, torsoY, 16, torsoH, 4); 
    ctx.fill();
    ctx.strokeStyle = "#ffdbac"; ctx.lineWidth = 4;
    ctx.beginPath(); ctx.moveTo(x - 8, torsoY + 2); ctx.lineTo(lElbowX, lElbowY); 
    ctx.lineTo(lHandX, lHandY); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x + 8, torsoY + 2); ctx.lineTo(rElbowX, rElbowY); 
    ctx.lineTo(rHandX, rHandY); ctx.stroke();
    ctx.fillStyle = "#ffdbac"; ctx.beginPath(); ctx.arc(x, headY, 9, 0, Math.PI * 2); 
    ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#4a3728"; ctx.beginPath(); ctx.arc(x, headY - 3, 9, Math.PI, 0); 
    ctx.fill(); ctx.fillRect(x - 9, headY - 5, 18, 4);
    ctx.fillStyle = "#222222"; ctx.fillRect(x - 4, headY - 2, 2, 2); 
    ctx.fillRect(x + 2, headY - 2, 2, 2);
    ctx.strokeStyle = "#ff2222"; ctx.lineWidth = 1; ctx.beginPath(); 
    ctx.arc(x, headY + 2, 3, 0, Math.PI); ctx.stroke();
  }}

  function renderStudio() {{
    if (motionState === 'crouch') {{
      crouchTimer += 1;
      if (crouchTimer > 15) {{ 
        motionState = 'airborne'; jumpStartTime = performance.now(); 
        boyVy = (pName === "Giant Planet") ? -0.1 : launchVelocity; 
      }}
    }} else if (motionState === 'airborne') {{
      boyY += boyVy;
      if (pName === "Giant Planet") {{ 
        boyVy += engineGravity; boyY += (Math.random() - 0.5) * 1.5; 
      }} else {{ boyVy += engineGravity; }}
      currentAirTime = (performance.now() - jumpStartTime) / 1000;
      if (boyY >= groundY) {{ 
        boyY = groundY; boyVy = 0; motionState = 'idle'; finalAirTime = currentAirTime; 
      }}
    }}

    let targetCameraY = groundY - canvas.height + 120;
    if (pName === "Moon" || pName === "Pluto" || pName === "Mars") {{
      targetCameraY = (boyY * 0.5) + (groundY * 0.5) - (canvas.height / 2);
    }}
    if (targetCameraY < 0) targetCameraY = 0;
    cameraY += (targetCameraY - cameraY) * 0.08;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let localGroundY = groundY - cameraY, localBoyY = boyY - cameraY;
    ctx.fillStyle = "#22c55e"; ctx.fillRect(0, localGroundY, canvas.width, 200);

    let earthLineY = (groundY - 45) - cameraY;
    ctx.strokeStyle = "rgba(255, 255, 255, 0.25)"; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(0, earthLineY); ctx.lineTo(canvas.width, earthLineY); ctx.stroke();
    ctx.fillStyle = "rgba(255, 255, 255, 0.4)"; ctx.font = "11px Courier New"; 
    ctx.fillText("Earth Bar (3 ft Benchmark)", 10, earthLineY - 5);

    ctx.strokeStyle = "#ffffff"; ctx.fillStyle = "rgba(255, 255, 255, 0.05)";
    
    if (pName === "Earth (Baseline)") {{
      ctx.fillStyle = "#e63946"; ctx.fillRect(100, earthLineY, 5, 45); ctx.fillRect(220, earthLineY, 5, 45);
      ctx.fillStyle = "#ffffff"; ctx.fillRect(100, earthLineY, 125, 3);
    }} else if (pName === "Jupiter") {{
      let stoolY = (groundY - 18) - cameraY; ctx.fillRect(230, stoolY, 25, 18);
      ctx.fillStyle = "#ffffff"; ctx.fillText("Stool (1.2 ft)", 215, stoolY - 7);
    }} else if (pName === "Mars") {{
      let hoopY = (groundY - 120) - cameraY; ctx.strokeStyle = "#ffffff"; 
      ctx.beginPath(); ctx.moveTo(250, localGroundY); ctx.lineTo(250, hoopY); ctx.lineTo(225, hoopY); ctx.stroke();
      ctx.fillStyle = "#ff595e"; ctx.fillRect(210, hoopY, 15, 4);
      ctx.fillStyle = "rgba(255,255,255,0.5)"; ctx.fillText("Hoop (8 ft)", 195, hoopY - 10);
    }} else if (pName === "Moon") {{
      let houseTopY = (groundY - 276) - cameraY;
      ctx.beginPath(); ctx.rect(210, houseTopY, 110, 276); 
      ctx.moveTo(210, houseTopY); ctx.lineTo(265, houseTopY - 40); ctx.lineTo(320, houseTopY); ctx.stroke();
      ctx.fillStyle = "rgba(255,255,255,0.4)"; ctx.font = "bold 10px Courier New";
      ctx.fillText("🏠 ROOF (18.4 ft)", 215, houseTopY + 15);
      ctx.fillRect(230, houseTopY + 60, 20, 20); ctx.fillRect(270, houseTopY + 60, 20, 20); 
      ctx.fillText("[ FLOOR 2 ]", 230, houseTopY + 100);
      ctx.strokeStyle = "rgba(255,255,255,0.1)"; ctx.beginPath(); ctx.moveTo(210, houseTopY + 138); ctx.lineTo(320, houseTopY + 138); ctx.stroke();
      ctx.fillRect(230, houseTopY + 180, 20, 20); ctx.fillRect(270, houseTopY + 180, 20, 20); 
      ctx.fillText("[ FLOOR 1 ]", 230, houseTopY + 220);
    }} else if (pName === "Pluto") {{
      let towerTopY = (groundY - 720) - cameraY;
      ctx.beginPath(); ctx.rect(230, towerTopY, 100, 720); ctx.stroke();
      let floorCounter = 5;
      for(let h = towerTopY; h < localGroundY - 20; h += 144) {{
        ctx.fillStyle = "rgba(255,255,255,0.15)"; ctx.fillRect(250, h + 30, 20, 20); ctx.fillRect(290, h + 30, 20, 20);
        ctx.fillStyle = "rgba(255,255,255,0.45)"; ctx.font = "bold 11px Courier New"; ctx.fillText("FLOOR " + floorCounter, 250, h + 80);
        if (floorCounter > 1) {{ ctx.strokeStyle = "rgba(255,255,255,0.08)"; ctx.beginPath(); ctx.moveTo(230, h + 144); ctx.lineTo(330, h + 144); ctx.stroke(); }}
        floorCounter--;
      }}
      ctx.fillStyle = "#00ffcc"; ctx.fillText("⭐ ROOF (48 ft)", 235, towerTopY - 10);
    }} else if (pName === "Giant Planet") {{
      ctx.fillStyle = "#e63946"; ctx.fillRect(220, localGroundY - 12, 40, 12);
    }}

    drawBoy(140, localBoyY, motionState, boyVy);
    drawVelocityArrow(140, localBoyY, boyVy);

    ctx.fillStyle = "rgba(15, 23, 42, 0.85)"; ctx.fillRect(15, 15, 160, 48);
    ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.strokeRect(15, 15, 160, 48);
    ctx.fillStyle = "#94a3b8"; ctx.font = "bold 11px Courier New"; ctx.fillText("AIRTIME CLOCK", 25, 30);
    ctx.font = "bold 18px Courier New"; ctx.fillStyle = "#22c55e";
    let elapsed = (motionState === 'airborne') ? currentAirTime : finalAirTime; ctx.fillText(elapsed.toFixed(3) + "s", 25, 52);
    requestAnimationFrame(renderStudio);
  }}
  function executeJumpTrigger() {{ if (motionState === 'idle') {{ motionState = 'crouch'; crouchTimer = 0; }} }}
  canvas.addEventListener('mousedown', executeJumpTrigger); 
  canvas.addEventListener('touchstart', function(e) {{ e.preventDefault(); executeJumpTrigger(); }}, false);
  renderStudio();
</script>
"""
comp.html(game_html, height=720)

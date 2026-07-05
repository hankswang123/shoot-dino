from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = """      if (input.w) truck.userData.speed += accel * dt;
      if (input.s) truck.userData.speed -= reverseAccel * dt;
      if (!input.w && !input.s) {
        const drag = Math.sign(truck.userData.speed) * friction * dt;
        if (Math.abs(drag) > Math.abs(truck.userData.speed)) truck.userData.speed = 0;
        else truck.userData.speed -= drag;
      }
      truck.userData.speed = THREE.MathUtils.clamp(truck.userData.speed, maxReverse, maxForward);
"""
new = """      if (input.w) truck.userData.speed -= accel * dt;
      if (input.s) truck.userData.speed += reverseAccel * dt;
      if (!input.w && !input.s) {
        const drag = Math.sign(truck.userData.speed) * friction * dt;
        if (Math.abs(drag) > Math.abs(truck.userData.speed)) truck.userData.speed = 0;
        else truck.userData.speed -= drag;
      }
      truck.userData.speed = THREE.MathUtils.clamp(truck.userData.speed, -maxForward, -maxReverse);
"""
if old not in text:
    raise SystemExit('W/S speed block not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')

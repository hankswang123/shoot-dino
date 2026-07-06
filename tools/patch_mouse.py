from pathlib import Path
path=Path('index.html')
text=path.read_text(encoding='utf-8')
text=text.replace("""      const aimPoint = aimTarget ? aimTarget.point : getAimPointFromGunRay(gunRay);
      setCrosshairAtWorldPoint(aimPoint, !!aimTarget);""", """      const aimPoint = getAimPointFromGunRay(gunRay);
      if (aimTarget) aimPoint.copy(aimTarget.point);
      setCrosshairAtWorldPoint(aimPoint, !!aimTarget);""")
old="""    window.addEventListener('mousemove', (e) => {
      if (document.pointerLockElement === canvas) {
        yawOffset -= e.movementX * 0.0022;
        pitch = THREE.MathUtils.clamp(pitch - e.movementY * 0.0018, -0.38, 0.62);
      }
    });"""
new="""    window.addEventListener('mousemove', (e) => {
      if (document.pointerLockElement === canvas) {
        yawOffset -= e.movementX * 0.0022;
        pitch = THREE.MathUtils.clamp(pitch - e.movementY * 0.0018, -0.38, 0.62);
      } else if (running && !gameOver) {
        const nx = (e.clientX / window.innerWidth) * 2 - 1;
        const ny = (e.clientY / window.innerHeight) * 2 - 1;
        yawOffset = THREE.MathUtils.clamp(-nx * 0.95, -1.15, 1.15);
        pitch = THREE.MathUtils.clamp(-ny * 0.38, -0.38, 0.62);
      }
    });"""
if old not in text:
    raise SystemExit('mousemove block not found')
text=text.replace(old,new,1)
path.write_text(text, encoding='utf-8')

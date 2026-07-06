from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = """    function getGunDirection() {
      const horizontalAngle = truck.userData.heading + yawOffset;
      const vertical = THREE.MathUtils.clamp(pitch * 0.75, -0.28, 0.46);
      return new THREE.Vector3(
        -Math.sin(horizontalAngle) * Math.cos(vertical),
        vertical,
        -Math.cos(horizontalAngle) * Math.cos(vertical)
      ).normalize();
    }
"""
new = """    function getGunDirection() {
      const horizontalAngle = truck.userData.heading + yawOffset;
      const vertical = THREE.MathUtils.clamp(pitch, -0.45, 1.42);
      return new THREE.Vector3(
        -Math.sin(horizontalAngle) * Math.cos(vertical),
        Math.sin(vertical),
        -Math.cos(horizontalAngle) * Math.cos(vertical)
      ).normalize();
    }
"""
if old not in text:
    raise SystemExit('getGunDirection block not found')
text = text.replace(old, new, 1)
text = text.replace('barrel.rotation.set(Math.PI / 2 + pitch * 0.7 - recoil, yawOffset, 0);', 'barrel.rotation.set(Math.PI / 2 + THREE.MathUtils.clamp(pitch, -0.45, 1.42) - recoil, yawOffset, 0);')
text = text.replace('pitch = THREE.MathUtils.clamp(pitch - e.movementY * 0.0018, -0.38, 0.62);', 'pitch = THREE.MathUtils.clamp(pitch - e.movementY * 0.0018, -0.45, 1.55);')
text = text.replace('pitch = THREE.MathUtils.clamp(-ny * 0.38, -0.38, 0.62);', 'pitch = THREE.MathUtils.clamp(-ny * 1.15, -0.45, 1.55);')
path.write_text(text, encoding='utf-8')

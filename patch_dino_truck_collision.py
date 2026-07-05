from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = """    function updateEnemies(dt) {
      let alive = 0;
"""
new = """    function separateDinoFromTruck(dino) {
      const truckCollisionRadius = 3.8;
      const dinoCollisionRadius = 1.25 * dino.scale.x;
      const minDistance = truckCollisionRadius + dinoCollisionRadius;
      const away = new THREE.Vector3(dino.position.x - truck.position.x, 0, dino.position.z - truck.position.z);
      let distance = away.length();
      if (distance === 0) {
        away.set(1, 0, 0);
        distance = 1;
      } else {
        away.divideScalar(distance);
      }
      if (distance < minDistance) {
        dino.position.x = truck.position.x + away.x * minDistance;
        dino.position.z = truck.position.z + away.z * minDistance;
        return true;
      }
      return distance < minDistance + 1.2;
    }

    function updateEnemies(dt) {
      let alive = 0;
"""
if old not in text:
    raise SystemExit('updateEnemies anchor not found')
text = text.replace(old, new, 1)
old2 = """        dino.position.x = THREE.MathUtils.clamp(dino.position.x, -worldSize + 5, worldSize - 5);
        dino.position.z = THREE.MathUtils.clamp(dino.position.z, -worldSize + 5, worldSize - 5);
        dino.rotation.y = Math.atan2(dir.x, dir.z) + Math.PI / 2;
        dino.position.y = Math.abs(Math.sin(clock.elapsedTime * 5.5 + dino.id)) * 0.06;
"""
new2 = """        dino.position.x = THREE.MathUtils.clamp(dino.position.x, -worldSize + 5, worldSize - 5);
        dino.position.z = THREE.MathUtils.clamp(dino.position.z, -worldSize + 5, worldSize - 5);
        const canAttackTruck = separateDinoFromTruck(dino);
        dino.rotation.y = Math.atan2(dir.x, dir.z) + Math.PI / 2;
        dino.position.y = Math.abs(Math.sin(clock.elapsedTime * 5.5 + dino.id)) * 0.06;
"""
if old2 not in text:
    raise SystemExit('dino movement block not found')
text = text.replace(old2, new2, 1)
old3 = """        if (dist < 5.7 && data.attackCooldown <= 0) {
          data.attackCooldown = 1.15;
          damagePlayer(8 + wave * 2);
        }
"""
new3 = """        if (canAttackTruck && data.attackCooldown <= 0) {
          data.attackCooldown = 1.15;
          damagePlayer(8 + wave * 2);
        }
"""
if old3 not in text:
    raise SystemExit('attack block not found')
text = text.replace(old3, new3, 1)
path.write_text(text, encoding='utf-8')

from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Replace single machine gun construction with two mountable guns.
old = """      const turretBase = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.72, 0.35, 18), materials.metal);
      turretBase.position.set(0, 2.03, 2.05);
      turretBase.castShadow = true;
      truck.add(turretBase);

      const barrel = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.16, 3.2, 14), materials.metal);
      barrel.rotation.x = Math.PI / 2;
      barrel.position.set(0, 2.25, 0.38);
      barrel.castShadow = true;
      truck.add(barrel);
      truck.userData.barrel = barrel;

      const muzzle = new THREE.Mesh(new THREE.ConeGeometry(0.34, 0.8, 16), materials.flash.clone());
      muzzle.rotation.x = -Math.PI / 2;
      muzzle.position.set(0, 2.25, -1.35);
      muzzle.visible = false;
      truck.add(muzzle);
      truck.userData.muzzle = muzzle;
"""
new = """      truck.userData.barrels = [];
      truck.userData.muzzles = [];
      truck.userData.dualGunsEnabled = false;

      const turretBase = new THREE.Mesh(new THREE.CylinderGeometry(0.72, 0.92, 0.35, 18), materials.metal);
      turretBase.position.set(0, 2.03, 2.05);
      turretBase.castShadow = true;
      truck.add(turretBase);

      function createMachineGun(x, primary) {
        const barrel = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.16, 3.2, 14), materials.metal);
        barrel.rotation.x = Math.PI / 2;
        barrel.position.set(x, 2.25, 0.38);
        barrel.castShadow = true;
        barrel.visible = primary;
        truck.add(barrel);
        truck.userData.barrels.push(barrel);

        const muzzle = new THREE.Mesh(new THREE.ConeGeometry(0.34, 0.8, 16), materials.flash.clone());
        muzzle.rotation.x = -Math.PI / 2;
        muzzle.position.set(x, 2.25, -1.35);
        muzzle.visible = false;
        truck.add(muzzle);
        truck.userData.muzzles.push(muzzle);
        return { barrel, muzzle };
      }

      const leftGun = createMachineGun(-0.34, true);
      createMachineGun(0.34, false);
      truck.userData.barrel = leftGun.barrel;
      truck.userData.muzzle = leftGun.muzzle;
"""
if old not in text:
    raise SystemExit('single machine gun block not found')
text = text.replace(old, new, 1)

# Add dual gun helper before createDino species block.
anchor = "    const dinoSpecies = ['trex', 'triceratops', 'pteranodon'];"
helper = """    function setDualMachineGunsEnabled(enabled) {
      truck.userData.dualGunsEnabled = enabled;
      truck.userData.barrels.forEach((barrel, index) => {
        barrel.visible = index === 0 || enabled;
      });
    }

"""
if helper.strip() not in text:
    text = text.replace(anchor, helper + anchor, 1)

# Enable dual guns from second wave.
text = text.replace("    function spawnWave() {\n      spawningNextWave = false;", "    function spawnWave() {\n      spawningNextWave = false;\n      setDualMachineGunsEnabled(wave >= 2);", 1)

# Rotate all visible barrels.
old = """      const barrel = truck.userData.barrel;
      if (barrel) {
        barrel.rotation.set(Math.PI / 2 + pitch * 0.7 - recoil, yawOffset, 0);
        barrel.rotation.y = yawOffset;
      }
"""
new = """      for (const barrel of truck.userData.barrels || []) {
        if (!barrel.visible) continue;
        barrel.rotation.set(Math.PI / 2 + pitch * 0.7 - recoil, yawOffset, 0);
        barrel.rotation.y = yawOffset;
      }
"""
if old not in text:
    raise SystemExit('barrel rotation block not found')
text = text.replace(old, new, 1)

# Replace muzzle/gun ray helpers.
old = """    function getMuzzleWorldPosition() {
      const pos = new THREE.Vector3(0, 2.25, -1.75);
      return truck.localToWorld(pos);
    }
"""
new = """    function getMuzzleWorldPosition(index = 0) {
      const muzzle = truck.userData.muzzles?.[index];
      const x = muzzle ? muzzle.position.x : 0;
      const pos = new THREE.Vector3(x, 2.25, -1.75);
      return truck.localToWorld(pos);
    }
"""
if old not in text:
    raise SystemExit('getMuzzleWorldPosition block not found')
text = text.replace(old, new, 1)

old = """    function getGunRay() {
      return { origin: getMuzzleWorldPosition(), direction: getGunDirection() };
    }
"""
new = """    function getGunRay() {
      return { origin: getMuzzleWorldPosition(), direction: getGunDirection() };
    }

    function getGunRays() {
      return (truck.userData.muzzles || [])
        .map((muzzle, index) => ({ muzzle, index }))
        .filter(({ index }) => index === 0 || truck.userData.dualGunsEnabled)
        .map(({ index }) => ({ origin: getMuzzleWorldPosition(index), direction: getGunDirection() }));
    }
"""
if old not in text:
    raise SystemExit('getGunRay block not found')
text = text.replace(old, new, 1)

# Replace shoot function body with multi-gun loop (preserve header).
start = text.index("    function shoot() {")
end = text.index("\n\n    function findEnemyRoot", start)
old_func = text[start:end]
new_func = r'''    function shoot() {
      if (!running || gameOver || fireCooldown > 0) return;
      fireCooldown = 0.075;
      recoil = 0.16;
      shake = Math.min(0.32, shake + 0.09);
      playGunSound();

      const gunRays = getGunRays();
      for (const gunRay of getGunRays()) {
        const muzzle = truck.userData.muzzles[gunRays.indexOf(gunRay)];
        if (muzzle) {
          muzzle.visible = true;
          muzzle.material.opacity = 0.95;
          effects.push({ type: 'muzzle', mesh: muzzle, life: 0.045, maxLife: 0.045 });
        }

        updateAimTarget();
        aimRaycaster.set(gunRay.origin, gunRay.direction);
        const muzzlePos = gunRay.origin;
        let endPoint = getAimPointFromGunRay(gunRay);

        if (aimTarget && !aimTarget.dino.userData.dead) {
          endPoint.copy(aimTarget.point);
          damageDino(aimTarget.dino, 14 + Math.round(Math.random() * 8), aimTarget.point);
        } else {
          const hitObjects = enemies.filter(e => !e.userData.dead).flatMap(e => e.children);
          const hits = aimRaycaster.intersectObjects(hitObjects, false);
          if (hits.length) {
            const hit = hits[0];
            endPoint.copy(hit.point);
            const dino = findEnemyRoot(hit.object);
            if (dino && !dino.userData.dead) damageDino(dino, 14 + Math.round(Math.random() * 8), hit.point);
          }
        }
        createBulletTracer(muzzlePos, endPoint);
      }
    }'''
text = text[:start] + new_func + text[end:]

# Add last-two force chase.
text = text.replace("    function updateEnemies(dt) {\n      let alive = 0;", "    function updateEnemies(dt) {\n      let alive = 0;\n      const livingCount = enemies.filter(e => !e.userData.dead && e.parent === scene).length;\n      const forceChasePlayer = livingCount <= 2;", 1)
text = text.replace("        if (dist < 70 || wave >= 3) dir = toPlayer.normalize();", "        if (forceChasePlayer || dist < 70 || wave >= 3) dir = toPlayer.normalize();", 1)

# Reset dual guns on restart before spawning first wave.
text = text.replace("      spawningNextWave = false;\n      running = true;", "      spawningNextWave = false;\n      setDualMachineGunsEnabled(false);\n      running = true;", 1)

path.write_text(text, encoding='utf-8')

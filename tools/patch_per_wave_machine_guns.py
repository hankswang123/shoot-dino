from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Replace dynamic gun setup inside createTruck.
old = """      truck.userData.barrels = [];
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
new = """      truck.userData.barrels = [];
      truck.userData.muzzles = [];
      truck.userData.activeGunCount = 1;

      const turretBase = new THREE.Mesh(new THREE.CylinderGeometry(0.92, 1.15, 0.35, 18), materials.metal);
      turretBase.position.set(0, 2.03, 2.05);
      turretBase.castShadow = true;
      truck.add(turretBase);

      ensureMachineGunCount(1);
      truck.userData.barrel = truck.userData.barrels[0];
      truck.userData.muzzle = truck.userData.muzzles[0];
"""
if old not in text:
    raise SystemExit('old dynamic gun block not found')
text = text.replace(old, new, 1)

# Replace setDual helper with generic helpers.
old = """    function setDualMachineGunsEnabled(enabled) {
      truck.userData.dualGunsEnabled = enabled;
      truck.userData.barrels.forEach((barrel, index) => {
        barrel.visible = index === 0 || enabled;
      });
    }

"""
new = """    function createMachineGun(x, primary) {
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

    function ensureMachineGunCount(count) {
      while (truck.userData.barrels.length < count) createMachineGun(0, false);
    }

    function setMachineGunCountForWave(waveNumber) {
      const count = Math.max(1, waveNumber);
      ensureMachineGunCount(count);
      truck.userData.activeGunCount = count;
      truck.userData.barrels.forEach((barrel, index) => {
        const x = (index - (count - 1) / 2) * 0.34;
        barrel.position.x = x;
        barrel.visible = index < count;
        truck.userData.muzzles[index].position.x = x;
      });
    }

"""
if old not in text:
    raise SystemExit('old setDual helper not found')
text = text.replace(old, new, 1)

# Wave start and reset use per-wave count.
text = text.replace('setDualMachineGunsEnabled(wave >= 2);', 'setMachineGunCountForWave(wave);')
text = text.replace('setDualMachineGunsEnabled(false);', 'setMachineGunCountForWave(1);')

# getGunRays active filter.
old = """    function getGunRays() {
      return (truck.userData.muzzles || [])
        .map((muzzle, index) => ({ muzzle, index }))
        .filter(({ index }) => index === 0 || truck.userData.dualGunsEnabled)
        .map(({ index }) => ({ origin: getMuzzleWorldPosition(index), direction: getGunDirection() }));
    }
"""
new = """    function getGunRays() {
      return (truck.userData.muzzles || [])
        .map((muzzle, index) => ({ muzzle, index }))
        .filter(({ index }) => index < truck.userData.activeGunCount)
        .map(({ index }) => ({ index, origin: getMuzzleWorldPosition(index), direction: getGunDirection() }));
    }
"""
if old not in text:
    raise SystemExit('old getGunRays block not found')
text = text.replace(old, new, 1)

# Fix shoot loop to use gunRays variable and gunRay.index.
text = text.replace('      const gunRays = getGunRays();\n      for (const gunRay of getGunRays()) {\n        const muzzle = truck.userData.muzzles[gunRays.indexOf(gunRay)];', '      const gunRays = getGunRays();\n      for (const gunRay of gunRays) {\n        const muzzle = truck.userData.muzzles[gunRay.index];')

path.write_text(text, encoding='utf-8')

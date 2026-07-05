from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Add next-wave spawn guard state.
text = text.replace("    let wave = 1;\n    let playerHealth = 100;", "    let wave = 1;\n    let spawningNextWave = false;\n    let playerHealth = 100;")

# Replace createDino with species variants and helpers.
start = text.index("    function createDino() {")
end = text.index("\n\n    function spawnWave()", start)
new_create = r'''    const dinoSpecies = ['trex', 'triceratops', 'pteranodon'];

    function addBodyPart(group, mesh, mat) {
      mesh.material = mat;
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      group.add(mesh);
      return mesh;
    }

    function addTrexFeatures(group, mat) {
      const jaw = addBodyPart(group, new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.28, 0.62), mat), mat);
      jaw.position.set(2.18, 2.33, 0);
      const brow = addBodyPart(group, new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.18, 0.72), mat), mat);
      brow.position.set(1.72, 2.83, 0);
      for (const z of [-0.55, 0.55]) {
        const arm = addBodyPart(group, new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.11, 0.85, 8), mat), mat);
        arm.position.set(0.85, 1.55, z);
        arm.rotation.z = 0.72;
      }
    }

    function addTriceratopsFeatures(group, mat) {
      const frill = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.95, 0.35, 18), mat), mat);
      frill.position.set(1.28, 2.55, 0);
      frill.rotation.z = Math.PI / 2;
      const noseHorn = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.75, 10), mat), mat);
      noseHorn.position.set(2.26, 2.54, 0);
      noseHorn.rotation.z = -Math.PI / 2;
      for (const z of [-0.36, 0.36]) {
        const horn = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.11, 0.95, 10), mat), mat);
        horn.position.set(1.74, 2.9, z);
        horn.rotation.z = -Math.PI / 2.25;
      }
    }

    function addPteranodonFeatures(group, mat) {
      const crest = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.18, 1.0, 8), mat), mat);
      crest.position.set(1.25, 2.76, 0);
      crest.rotation.z = Math.PI / 2;
      for (const z of [-1, 1]) {
        const wing = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.18, 4.2, 4), mat), mat);
        wing.position.set(0.05, 1.88, z * 1.35);
        wing.rotation.x = z * Math.PI / 2;
        wing.rotation.z = 1.38;
        wing.scale.set(1.0, 1.0, 0.32);
      }
    }

    function createDino() {
      const species = dinoSpecies[Math.floor(Math.random() * dinoSpecies.length)];
      const colors = { trex: 0x5f7f36, triceratops: 0x7b7040, pteranodon: 0x536f7c };
      const mat = new THREE.MeshStandardMaterial({ color: colors[species], roughness: 0.92 });
      const group = new THREE.Group();
      const body = addBodyPart(group, new THREE.Mesh(new THREE.CapsuleGeometry(0.9, 2.35, 6, 12), mat), mat);
      body.rotation.z = Math.PI / 2;
      body.position.y = 1.6;

      const neck = addBodyPart(group, new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.36, 1.15, 8), mat), mat);
      neck.position.set(1.1, 2.15, 0);
      neck.rotation.z = -0.62;

      const head = addBodyPart(group, new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.55, 0.55), mat), mat);
      head.position.set(1.72, 2.55, 0);

      const tail = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.36, 2.25, 10), mat), mat);
      tail.rotation.z = Math.PI / 2;
      tail.position.set(-1.95, 1.72, 0);

      for (const x of [-0.7, 0.65]) {
        for (const z of [-0.42, 0.42]) {
          const leg = addBodyPart(group, new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.24, 1.38, 8), mat), mat);
          leg.position.set(x, 0.7, z);
        }
      }

      if (species === 'trex') addTrexFeatures(group, mat);
      if (species === 'triceratops') addTriceratopsFeatures(group, mat);
      if (species === 'pteranodon') addPteranodonFeatures(group, mat);

      let scale = rand(1.1, 1.75);
      if (species === 'trex') scale *= 1.18;
      if (species === 'triceratops') scale *= 1.08;
      if (species === 'pteranodon') scale *= 0.82;
      group.scale.set(scale, scale, scale);
      const hpMultiplier = species === 'trex' ? 1.35 : species === 'triceratops' ? 1.55 : 0.75;
      const speedMultiplier = species === 'pteranodon' ? 1.55 : species === 'triceratops' ? 0.78 : 1.0;
      group.userData = {
        type: species,
        hp: Math.round((45 * scale + wave * 8) * hpMultiplier),
        maxHp: Math.round((45 * scale + wave * 8) * hpMultiplier),
        speed: (rand(3.6, 6.2) / scale + wave * 0.12) * speedMultiplier,
        stateTimer: rand(0, 3),
        wanderAngle: rand(0, Math.PI * 2),
        attackCooldown: 0,
        hitFlash: 0,
        dead: false,
        deathTimer: 0,
        flyHeight: species === 'pteranodon' ? rand(4.8, 7.2) : 0,
        baseMaterial: mat,
        bodyParts: group.children
      };
      return group;
    }'''
text = text[:start] + new_create + text[end:]

# Patch spawnWave count and guard reset.
text = text.replace("    function spawnWave() {\n      const count = 4 + wave * 2;", "    function getWaveDinoCount() {\n      return 6 + (wave - 1) * 10;\n    }\n\n    function spawnWave() {\n      spawningNextWave = false;\n      const count = getWaveDinoCount();")

# Fix pteranodon vertical bob and species material restore.
text = text.replace("          if (data.hitFlash <= 0) data.bodyParts.forEach(p => p.material = materials.dino);", "          if (data.hitFlash <= 0) data.bodyParts.forEach(p => p.material = data.baseMaterial);")
text = text.replace("        dino.position.y = Math.abs(Math.sin(clock.elapsedTime * 5.5 + dino.id)) * 0.06;", "        dino.position.y = data.flyHeight + Math.abs(Math.sin(clock.elapsedTime * 5.5 + dino.id)) * (data.flyHeight ? 0.45 : 0.06);")

# Add spawn guard to stop thousands of queued wave spawns.
text = text.replace("      if (alive === 0 && running && !gameOver && enemies.length === 0) {\n        wave++;\n        setTimeout(() => { if (running && !gameOver) spawnWave(); }, 700);\n      }", "      if (alive === 0 && running && !gameOver && !spawningNextWave) {\n        spawningNextWave = true;\n        wave++;\n        setTimeout(() => { if (running && !gameOver) spawnWave(); }, 700);\n      }")

# Count only live enemies still attached to the scene for HUD and hints.
text = text.replace("const living = enemies.filter(e => !e.userData.dead);", "const living = enemies.filter(e => !e.userData.dead && e.parent === scene);")
text = text.replace("leftEl.textContent = enemies.filter(e => !e.userData.dead).length;", "leftEl.textContent = enemies.filter(e => !e.userData.dead && e.parent === scene).length;")

# Reset guard when restarting.
text = text.replace("      gameOver = false;\n      running = true;", "      gameOver = false;\n      spawningNextWave = false;\n      running = true;")

path.write_text(text, encoding='utf-8')

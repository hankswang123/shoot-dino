from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')

# Add biome objects state after obstacles/effects arrays.
text = text.replace("    const obstacles = [];\n    const bullets = [];", "    const obstacles = [];\n    const biomeObjects = [];\n    const bullets = [];", 1)

# Insert biome helpers before createTerrain.
anchor = "    function createTerrain() {"
helpers = r'''    const biomes = [
      { name: '草原', sky: 0x8ec8ff, fog: 0x8ec8ff, ground: 0x56702a, leaf: 0x245c2c, rock: 0x6f7168, prop: 'palm' },
      { name: '沙漠', sky: 0xf0c987, fog: 0xf0c987, ground: 0xc79a4a, leaf: 0x8d9c3d, rock: 0x9b8061, prop: 'rock' },
      { name: '森林', sky: 0x6fa4b8, fog: 0x6fa4b8, ground: 0x2f552a, leaf: 0x174d24, rock: 0x5f675e, prop: 'forest' },
      { name: '湿地', sky: 0x7f9e94, fog: 0x7f9e94, ground: 0x3d5a38, leaf: 0x1d6938, rock: 0x556057, prop: 'mixed' }
    ];

    function trackBiomeObject(obj) {
      biomeObjects.push(obj);
      return obj;
    }

    function clearBiomeObjects() {
      for (const obj of biomeObjects) scene.remove(obj);
      biomeObjects.length = 0;
      for (let i = obstacles.length - 1; i >= 0; i--) {
        if (obstacles[i].biome) obstacles.splice(i, 1);
      }
    }

    function applyBiomeForWave(waveNumber) {
      clearBiomeObjects();
      const biome = biomes[(waveNumber - 1) % biomes.length];
      scene.background = new THREE.Color(biome.sky);
      scene.fog = new THREE.Fog(biome.fog, 90, 310);
      materials.ground.color.setHex(biome.ground);
      materials.leaf.color.setHex(biome.leaf);
      materials.rock.color.setHex(biome.rock);
      for (let i = 0; i < 22; i++) {
        const p = randomEdgePosition(48, worldSize - 18);
        if (biome.prop === 'rock' || Math.random() < 0.38) createBiomeRock(p.x, p.z, rand(1.0, 2.8), biome);
        else createBiomePalm(p.x, p.z, rand(0.7, 1.35), biome);
      }
    }

    function createBiomePalm(x, z, s, biome) {
      const group = new THREE.Group();
      group.position.set(x, 0, z);
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.28*s, 0.46*s, 6.5*s, 7), materials.trunk);
      trunk.position.y = 3.25*s;
      trunk.castShadow = true;
      group.add(trunk);
      for (let i = 0; i < (biome.prop === 'forest' ? 10 : 6); i++) {
        const leaf = new THREE.Mesh(new THREE.ConeGeometry(1.0*s, 5.0*s, 4), materials.leaf);
        leaf.position.y = 6.8*s;
        leaf.rotation.z = Math.PI / 2 + rand(-0.25, 0.25);
        leaf.rotation.y = i / 8 * Math.PI * 2;
        leaf.position.x = Math.cos(leaf.rotation.y) * 1.4*s;
        leaf.position.z = Math.sin(leaf.rotation.y) * 1.4*s;
        leaf.castShadow = true;
        group.add(leaf);
      }
      scene.add(trackBiomeObject(group));
      obstacles.push({ x, z, radius: 1.05 * s, type: 'biome-tree', biome: true });
    }

    function createBiomeRock(x, z, s, biome) {
      const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(s, 0), materials.rock);
      rock.position.set(x, s * 0.38, z);
      rock.scale.set(rand(1, 2.2), rand(0.35, 0.9), rand(0.8, 1.9));
      rock.rotation.set(rand(0, 1), rand(0, Math.PI * 2), rand(0, 1));
      rock.castShadow = true;
      rock.receiveShadow = true;
      scene.add(trackBiomeObject(rock));
      obstacles.push({ x, z, radius: 1.2 * s * Math.max(rock.scale.x, rock.scale.z), type: 'biome-rock', biome: true });
    }

'''
if 'const biomes = [' not in text:
    text = text.replace(anchor, helpers + anchor, 1)

# Mark static obstacles as non-biome.
text = text.replace("obstacles.push({ x, z, radius, type });", "obstacles.push({ x, z, radius, type, biome: false });")

# Apply biome on each wave start.
text = text.replace("    function spawnWave() {\n      spawningNextWave = false;\n      setDualMachineGunsEnabled(wave >= 2);", "    function spawnWave() {\n      spawningNextWave = false;\n      applyBiomeForWave(wave);\n      setDualMachineGunsEnabled(wave >= 2);", 1)

# Add AI pacing properties.
text = text.replace("        speed: (rand(3.6, 6.2) / scale + wave * 0.12) * speedMultiplier,\n        stateTimer:", "        speed: (rand(3.1, 5.1) / scale + wave * 0.06) * speedMultiplier,\n        engageDelay: 0,\n        chaseRange: rand(58, 88),\n        stateTimer:", 1)

# Set per-dino engage delay in spawnWave after position/rotation.
text = text.replace("        dino.rotation.y = -angle + Math.PI / 2;\n        scene.add(dino);", "        dino.rotation.y = -angle + Math.PI / 2;\n        dino.userData.engageDelay = wave >= 3 ? rand(2.5, 9.5) + i * 0.12 : rand(0.2, 2.8);\n        scene.add(dino);", 1)

# Update AI chase condition and speed.
text = text.replace("        data.attackCooldown = Math.max(0, data.attackCooldown - dt);\n        data.stateTimer -= dt;", "        data.attackCooldown = Math.max(0, data.attackCooldown - dt);\n        data.engageDelay = Math.max(0, data.engageDelay - dt);\n        data.stateTimer -= dt;", 1)
text = text.replace("        if (forceChasePlayer || dist < 70 || wave >= 3) dir = toPlayer.normalize();", "        if (forceChasePlayer || (data.engageDelay <= 0 && dist < data.chaseRange)) dir = toPlayer.normalize();", 1)
text = text.replace("        const speed = data.speed * (dist < 28 ? 1.28 : 1.0);", "        const speed = data.speed * (dist < 28 ? 1.06 : 0.88);", 1)

path.write_text(text, encoding='utf-8')

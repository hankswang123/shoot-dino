from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')

# HUD panel and DOM lookup.
text = text.replace('      <div class="panel">剩余恐龙：<span id="left">0</span></div>\n    </div>', '      <div class="panel">剩余恐龙：<span id="left">0</span></div>\n      <div class="panel">防空武器：<span id="antiAir">3</span>/3</div>\n    </div>', 1)
text = text.replace("    const leftEl = document.getElementById('left');\n    const dinoHintEl", "    const leftEl = document.getElementById('left');\n    const antiAirEl = document.getElementById('antiAir');\n    const dinoHintEl", 1)

# State.
text = text.replace('    let playerHealth = 100;\n    let fireCooldown = 0;', '    let playerHealth = 100;\n    let antiAirCharges = 3;\n    let fireCooldown = 0;', 1)

# Wave start refill and reset.
text = text.replace('    function spawnWave() {\n      spawningNextWave = false;', '    function spawnWave() {\n      spawningNextWave = false;\n      playerHealth = 100;\n      antiAirCharges = 3;', 1)

# Add anti-air function before damageDino.
anchor = '    function damageDino(dino, dmg, point) {'
func = r'''    function useAntiAirWeapon() {
      if (!running || gameOver || antiAirCharges <= 0) return;
      const pteranodons = enemies.filter(e => !e.userData.dead && e.parent === scene && e.userData.type === 'pteranodon');
      if (!pteranodons.length) return;
      pteranodons.sort((a, b) => truck.position.distanceTo(a.position) - truck.position.distanceTo(b.position));
      const target = pteranodons[0];
      antiAirCharges--;
      const start = getMuzzleWorldPosition(0);
      const end = target.position.clone().add(new THREE.Vector3(0, target.userData.flyHeight ? 2.2 : 1.5, 0));
      createBulletTracer(start, end);
      createHitSpark(end);
      damageDino(target, target.userData.maxHp, target.position.clone().add(new THREE.Vector3(0, 2, 0)));
      updateHud();
    }

'''
if 'function useAntiAirWeapon()' not in text:
    text = text.replace(anchor, func + anchor, 1)

# Update HUD.
text = text.replace('      leftEl.textContent = enemies.filter(e => !e.userData.dead && e.parent === scene).length;\n      updateDinoHint();', '      leftEl.textContent = enemies.filter(e => !e.userData.dead && e.parent === scene).length;\n      antiAirEl.textContent = antiAirCharges;\n      updateDinoHint();', 1)

# Reset state and keybinding.
text = text.replace('      playerHealth = 100;\n      gameOver = false;', '      playerHealth = 100;\n      antiAirCharges = 3;\n      gameOver = false;', 1)
text = text.replace("      if (k === 'r') resetGame();", "      if (k === 'r') resetGame();\n      if (k === 'q') useAntiAirWeapon();", 1)
text = text.replace('操作：W 前进，S 倒车，A/D 转向，鼠标移动瞄准，左键机枪射击，R 重开。', '操作：W 前进，S 倒车，A/D 转向，鼠标移动瞄准，左键机枪射击，Q 防空武器，R 重开。')

path.write_text(text, encoding='utf-8')

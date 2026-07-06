from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')
text = text.replace('      <div class="panel">剩余恐龙：<span id="left">0</span></div>\n    </div>', '      <div class="panel">剩余恐龙：<span id="left">0</span></div>\n    </div>\n    <div id="dinoHint" class="panel"></div>')
text = text.replace('      操作：W/S 加速与倒车，A/D 转向，鼠标移动瞄准，左键机枪射击，R 重开。<br />', '      操作：W 前进，S 倒车，A/D 转向，鼠标移动瞄准，左键机枪射击，R 重开。<br />')
text = text.replace("    const leftEl = document.getElementById('left');\n    const centerMessage", "    const leftEl = document.getElementById('left');\n    const dinoHintEl = document.getElementById('dinoHint');\n    const centerMessage")
css_anchor = """    #tips {
      position: absolute;
      left: 22px;
      bottom: 18px;
      max-width: 520px;
      color: rgba(255,255,255,.72);
      font-size: 13px;
      line-height: 1.55;
    }
"""
css_insert = css_anchor + """
    #dinoHint {
      position: absolute;
      right: 22px;
      top: 18px;
      max-width: 340px;
      display: none;
      color: #ffe08a;
      font-weight: 900;
      line-height: 1.45;
    }
"""
if '#dinoHint' not in text[:text.find('</style>')]:
    text = text.replace(css_anchor, css_insert)
old = """    function updateHud() {
      healthBar.style.transform = `scaleX(${playerHealth / 100})`;
      scoreEl.textContent = score;
      waveEl.textContent = wave;
      leftEl.textContent = enemies.filter(e => !e.userData.dead).length;
    }
"""
new = """    function formatDinoDirection(dino) {
      const dx = dino.position.x - truck.position.x;
      const dz = dino.position.z - truck.position.z;
      const distance = Math.round(Math.sqrt(dx * dx + dz * dz));
      const angle = Math.atan2(dx, dz) - truck.userData.heading;
      const normalized = Math.atan2(Math.sin(angle), Math.cos(angle));
      const labels = ['前方', '右前方', '右侧', '右后方', '后方', '左后方', '左侧', '左前方'];
      const index = Math.round((normalized + Math.PI) / (Math.PI / 4)) % 8;
      return `${labels[index]} ${distance}m`;
    }

    function updateDinoHint() {
      const living = enemies.filter(e => !e.userData.dead);
      if (living.length > 0 && living.length <= 2) {
        dinoHintEl.style.display = 'block';
        const lines = living
          .sort((a, b) => truck.position.distanceTo(a.position) - truck.position.distanceTo(b.position))
          .map((dino, index) => `恐龙 ${index + 1}：${formatDinoDirection(dino)}`);
        dinoHintEl.innerHTML = `最后 ${living.length} 只恐龙位置<br>${lines.join('<br>')}`;
      } else {
        dinoHintEl.style.display = 'none';
        dinoHintEl.textContent = '';
      }
    }

    function updateHud() {
      healthBar.style.transform = `scaleX(${playerHealth / 100})`;
      scoreEl.textContent = score;
      waveEl.textContent = wave;
      leftEl.textContent = enemies.filter(e => !e.userData.dead).length;
      updateDinoHint();
    }
"""
if old not in text:
    raise SystemExit('updateHud block not found')
text = text.replace(old, new, 1)
# Keep hint fresh while the last dinos move.
text = text.replace('      leftEl.textContent = alive;\n    }', '      leftEl.textContent = alive;\n      updateDinoHint();\n    }', 1)
path.write_text(text, encoding='utf-8')

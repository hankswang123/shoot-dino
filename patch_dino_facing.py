from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')
anchor = "    function getWaveDinoCount() {"
helper = """    function faceDinoAlongDirection(dino, dir) {
      dino.rotation.y = Math.atan2(dir.x, dir.z) - Math.PI / 2;
    }

"""
if helper.strip() not in text:
    text = text.replace(anchor, helper + anchor, 1)
text = text.replace("        dino.rotation.y = -angle + Math.PI / 2;", "        faceDinoAlongDirection(dino, new THREE.Vector3(-Math.cos(angle), 0, -Math.sin(angle)));")
text = text.replace("        dino.rotation.y = Math.atan2(dir.x, dir.z) + Math.PI / 2;", "        faceDinoAlongDirection(dino, dir);")
path.write_text(text, encoding='utf-8')

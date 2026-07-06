from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')
text = text.replace("""      const hitVolume = new THREE.Mesh(new THREE.BoxGeometry(3.8, 1.7, 7.2), hitMat);
      hitVolume.position.set(0.15, 2.05, 0);""", """      const hitVolume = new THREE.Mesh(new THREE.BoxGeometry(3.8, 1.7, 7.2), hitMat);
      hitVolume.material.colorWrite = false;
      hitVolume.position.set(0.15, 2.05, 0);""")
text = text.replace("""      const tail = group.children[3];
      tail.scale.set(0.38, 1.25, 0.38);
      const beak = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.16, 1.65, 12), mat), mat);""", """      const tail = group.children[3];
      tail.scale.set(0.38, 1.25, 0.38);
      for (const leg of group.children.slice(4, 8)) leg.scale.set(0.25, 0.55, 0.25);
      const beak = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.16, 1.65, 12), mat), mat);""")
path.write_text(text, encoding='utf-8')

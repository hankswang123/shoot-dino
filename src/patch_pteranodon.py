from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = r'''    function addPteranodonFeatures(group, mat) {
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
    }'''
new = r'''    function addPteranodonHitVolume(group, mat) {
      const hitMat = mat.clone();
      hitMat.transparent = true;
      hitMat.opacity = 0;
      hitMat.colorWrite = false;
      hitMat.depthWrite = false;
      const hitVolume = new THREE.Mesh(new THREE.BoxGeometry(3.8, 1.7, 7.2), hitMat);
      hitVolume.position.set(0.15, 2.05, 0);
      hitVolume.userData.isHitVolume = true;
      group.add(hitVolume);
      return hitVolume;
    }

    function makePteranodonSilhouette(group, mat) {
      const body = group.children[0];
      body.scale.set(0.55, 1.18, 0.42);
      const head = group.children[2];
      head.scale.set(0.62, 0.55, 0.55);
      const tail = group.children[3];
      tail.scale.set(0.38, 1.25, 0.38);
      const beak = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.16, 1.65, 12), mat), mat);
      beak.position.set(2.42, 2.52, 0);
      beak.rotation.z = -Math.PI / 2;
      beak.scale.set(1.9, 0.35, 0.35);
    }

    function addPteranodonFeatures(group, mat) {
      makePteranodonSilhouette(group, mat);
      const crest = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.16, 1.05, 8), mat), mat);
      crest.position.set(1.42, 2.86, 0);
      crest.rotation.z = Math.PI / 2;
      for (const z of [-1, 1]) {
        const wing = addBodyPart(group, new THREE.Mesh(new THREE.ConeGeometry(0.2, 4.9, 4), mat), mat);
        wing.position.set(-0.08, 1.92, z * 1.72);
        wing.rotation.x = z * Math.PI / 2;
        wing.rotation.z = 1.42;
        wing.scale.set(1.9, 1.15, 0.22);
      }
      addPteranodonHitVolume(group, mat);
    }'''
if old not in text:
    raise SystemExit('old pteranodon features block not found')
text = text.replace(old, new, 1)
text = text.replace('        bodyParts: group.children\n      };', '        bodyParts: group.children.filter(p => !p.userData.isHitVolume)\n      };')
path.write_text(text, encoding='utf-8')

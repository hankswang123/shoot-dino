from pathlib import Path
path = Path('index.html')
text = path.read_text(encoding='utf-8')
old = """      const barrel = truck.userData.barrel;
      if (barrel) {
        const aimHeading = heading + Math.PI;
        barrel.rotation.set(Math.PI / 2 + pitch * 0.45 - recoil, 0, 0);
        barrel.rotation.y = -yawOffset;
      }
      recoil = Math.max(0, recoil - dt * 5.5);
      updateAimTarget();
    }

    function updateAimTarget() {
      aimTarget = null;
      const livingEnemies = enemies.filter(e => !e.userData.dead);
      if (!livingEnemies.length) {
        crosshair.style.left = '50%';
        crosshair.style.top = '50%';
        crosshair.style.transform = 'translate(-50%, -50%) scale(1)';
        return;
      }

      aimRaycaster.setFromCamera(pointer, camera);
      const hitObjects = livingEnemies.flatMap(e => e.children);
      const directHits = aimRaycaster.intersectObjects(hitObjects, false);
      if (directHits.length) {
        const hit = directHits[0];
        const dino = findEnemyRoot(hit.object);
        if (dino) aimTarget = { dino, point: hit.point.clone(), distance: hit.distance };
      }

      if (!aimTarget) {
        const center = new THREE.Vector2(window.innerWidth / 2, window.innerHeight / 2);
        let best = null;
        for (const dino of livingEnemies) {
          const targetPoint = dino.position.clone().add(new THREE.Vector3(0, 2.1 * dino.scale.y, 0));
          const projected = targetPoint.clone().project(camera);
          if (projected.z < -1 || projected.z > 1) continue;
          const screen = new THREE.Vector2((projected.x * 0.5 + 0.5) * window.innerWidth, (-projected.y * 0.5 + 0.5) * window.innerHeight);
          const screenDistance = screen.distanceTo(center);
          const worldDistance = camera.position.distanceTo(targetPoint);
          if (screenDistance <= 86 && (!best || screenDistance < best.screenDistance || (screenDistance === best.screenDistance && worldDistance < best.distance))) {
            best = { dino, point: targetPoint, screen, screenDistance, distance: worldDistance };
          }
        }
        if (best) aimTarget = best;
      }

      if (aimTarget) {
        const projected = aimTarget.point.clone().project(camera);
        const x = (projected.x * 0.5 + 0.5) * window.innerWidth;
        const y = (-projected.y * 0.5 + 0.5) * window.innerHeight;
        crosshair.style.left = `${x}px`;
        crosshair.style.top = `${y}px`;
        crosshair.style.transform = 'translate(-50%, -50%) scale(1.25)';
      } else {
        crosshair.style.left = '50%';
        crosshair.style.top = '50%';
        crosshair.style.transform = 'translate(-50%, -50%) scale(1)';
      }
    }

    function getMuzzleWorldPosition() {
      const pos = new THREE.Vector3(0, 2.25, -1.75);
      return truck.localToWorld(pos);
    }
"""
new = """      const barrel = truck.userData.barrel;
      if (barrel) {
        barrel.rotation.set(Math.PI / 2 + pitch * 0.7 - recoil, yawOffset, 0);
        barrel.rotation.y = yawOffset;
      }
      recoil = Math.max(0, recoil - dt * 5.5);
      updateAimTarget();
    }

    function getMuzzleWorldPosition() {
      const pos = new THREE.Vector3(0, 2.25, -1.75);
      return truck.localToWorld(pos);
    }

    function getGunDirection() {
      const horizontalAngle = truck.userData.heading + yawOffset;
      const vertical = THREE.MathUtils.clamp(pitch * 0.75, -0.28, 0.46);
      return new THREE.Vector3(
        -Math.sin(horizontalAngle) * Math.cos(vertical),
        vertical,
        -Math.cos(horizontalAngle) * Math.cos(vertical)
      ).normalize();
    }

    function getGunRay() {
      return { origin: getMuzzleWorldPosition(), direction: getGunDirection() };
    }

    function getAimPointFromGunRay(gunRay) {
      return gunRay.origin.clone().add(gunRay.direction.clone().multiplyScalar(140));
    }

    function setCrosshairAtWorldPoint(point, locked) {
      const projected = point.clone().project(camera);
      const x = THREE.MathUtils.clamp((projected.x * 0.5 + 0.5) * window.innerWidth, 18, window.innerWidth - 18);
      const y = THREE.MathUtils.clamp((-projected.y * 0.5 + 0.5) * window.innerHeight, 18, window.innerHeight - 18);
      crosshair.style.left = `${x}px`;
      crosshair.style.top = `${y}px`;
      crosshair.style.transform = `translate(-50%, -50%) scale(${locked ? 1.25 : 1})`;
    }

    function findAimAssistTarget(gunRay, livingEnemies) {
      let best = null;
      for (const dino of livingEnemies) {
        const targetPoint = dino.position.clone().add(new THREE.Vector3(0, 2.0 * dino.scale.y, 0));
        const toTarget = targetPoint.clone().sub(gunRay.origin);
        const forwardDistance = toTarget.dot(gunRay.direction);
        if (forwardDistance < 0 || forwardDistance > 150) continue;
        const closestPoint = gunRay.origin.clone().add(gunRay.direction.clone().multiplyScalar(forwardDistance));
        const missDistance = closestPoint.distanceTo(targetPoint);
        const lockRadius = 3.0 + dino.scale.x * 1.8;
        if (missDistance <= lockRadius && (!best || missDistance < best.missDistance || forwardDistance < best.distance)) {
          best = { dino, point: targetPoint, distance: forwardDistance, missDistance };
        }
      }
      return best;
    }

    function updateAimTarget() {
      aimTarget = null;
      const gunRay = getGunRay();
      const livingEnemies = enemies.filter(e => !e.userData.dead);
      const hitObjects = livingEnemies.flatMap(e => e.children);
      aimRaycaster.set(gunRay.origin, gunRay.direction);
      const directHits = aimRaycaster.intersectObjects(hitObjects, false);

      if (directHits.length) {
        const hit = directHits[0];
        const dino = findEnemyRoot(hit.object);
        if (dino) aimTarget = { dino, point: hit.point.clone(), distance: hit.distance };
      } else {
        aimTarget = findAimAssistTarget(gunRay, livingEnemies);
      }

      const aimPoint = aimTarget ? aimTarget.point : getAimPointFromGunRay(gunRay);
      setCrosshairAtWorldPoint(aimPoint, !!aimTarget);
    }
"""
if old not in text:
    raise SystemExit('old camera/aim block not found')
text = text.replace(old, new, 1)
old2 = """      updateAimTarget();
      aimRaycaster.setFromCamera(pointer, camera);
      const muzzlePos = getMuzzleWorldPosition();
      let endPoint = muzzlePos.clone().add(aimRaycaster.ray.direction.clone().multiplyScalar(120));

      if (aimTarget && !aimTarget.dino.userData.dead) {
        endPoint.copy(aimTarget.point);
        damageDino(aimTarget.dino, 18 + Math.round(Math.random() * 10), aimTarget.point);
      } else {
        const hitObjects = enemies.filter(e => !e.userData.dead).flatMap(e => e.children);
        const hits = aimRaycaster.intersectObjects(hitObjects, false);
        if (hits.length) {
          const hit = hits[0];
          endPoint.copy(hit.point);
          const dino = findEnemyRoot(hit.object);
          if (dino && !dino.userData.dead) damageDino(dino, 18 + Math.round(Math.random() * 10), hit.point);
        }
      }
      createBulletTracer(muzzlePos, endPoint);
"""
new2 = """      const gunRay = getGunRay();
      updateAimTarget();
      aimRaycaster.set(gunRay.origin, gunRay.direction);
      const muzzlePos = gunRay.origin;
      let endPoint = getAimPointFromGunRay(gunRay);

      if (aimTarget && !aimTarget.dino.userData.dead) {
        endPoint.copy(aimTarget.point);
        damageDino(aimTarget.dino, 18 + Math.round(Math.random() * 10), aimTarget.point);
      } else {
        const hitObjects = enemies.filter(e => !e.userData.dead).flatMap(e => e.children);
        const hits = aimRaycaster.intersectObjects(hitObjects, false);
        if (hits.length) {
          const hit = hits[0];
          endPoint.copy(hit.point);
          const dino = findEnemyRoot(hit.object);
          if (dino && !dino.userData.dead) damageDino(dino, 18 + Math.round(Math.random() * 10), hit.point);
        }
      }
      createBulletTracer(muzzlePos, endPoint);
"""
if old2 not in text:
    raise SystemExit('old shoot block not found')
text = text.replace(old2, new2, 1)
path.write_text(text, encoding='utf-8')

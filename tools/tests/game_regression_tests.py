from pathlib import Path

html = Path('index.html').read_text(encoding='utf-8')


def assert_contains(text, needle, label):
    if needle not in text:
        raise AssertionError(f"Missing {label}: {needle}")


def test_target_lock_crosshair_and_shooting():
    assert_contains(html, 'let aimTarget = null;', 'aim target state')
    assert_contains(html, 'function updateAimTarget()', 'aim target update loop')
    assert_contains(html, 'crosshair.style.transform', 'dynamic crosshair placement')
    assert_contains(html, 'if (aimTarget && !aimTarget.dino.userData.dead)', 'direct target shooting branch')


def test_obstacle_collision_registry_and_truck_blocking():
    assert_contains(html, 'const obstacles = [];', 'obstacle collision registry')
    assert_contains(html, 'function registerObstacle', 'obstacle registration helper')
    assert_contains(html, 'function resolveTruckObstacleCollision', 'truck obstacle collision resolver')
    assert_contains(html, 'truck.position.copy(previousPosition)', 'collision rollback for solid obstacles')


def test_crosshair_and_bullets_use_machine_gun_ray():
    assert_contains(html, 'function getGunDirection()', 'machine gun direction helper')
    assert_contains(html, 'function getGunRay()', 'machine gun ray helper')
    assert_contains(html, 'aimRaycaster.set(gunRay.origin, gunRay.direction)', 'raycast from gun muzzle direction')
    assert_contains(html, 'const aimPoint = getAimPointFromGunRay(gunRay)', 'crosshair projected from gun ray')
    assert_contains(html, 'barrelPivot.lookAt(aimPoint);', 'barrel pivot aims at crosshair direction')


def test_dinosaurs_cannot_overlap_truck():
    assert_contains(html, 'const truckCollisionRadius = 3.8;', 'truck collision radius for dinosaurs')
    assert_contains(html, 'function separateDinoFromTruck(dino)', 'dino truck separation helper')
    assert_contains(html, 'dino.position.x = truck.position.x + away.x * minDistance;', 'push dino outside truck radius')
    assert_contains(html, 'const canAttackTruck = separateDinoFromTruck(dino);', 'separation result used for attack')
    assert_contains(html, 'if (canAttackTruck && data.attackCooldown <= 0)', 'attack allowed without overlap')


def test_w_moves_forward_and_s_reverses():
    assert_contains(html, 'if (input.w) truck.userData.speed -= accel * dt;', 'W accelerates toward visual forward')
    assert_contains(html, 'if (input.s) truck.userData.speed += reverseAccel * dt;', 'S accelerates toward reverse')
    assert_contains(html, 'truck.userData.speed = THREE.MathUtils.clamp(truck.userData.speed, -maxForward, -maxReverse);', 'speed clamp supports swapped forward reverse ranges')


def test_last_dinosaur_location_hint():
    assert_contains(html, '<div id="dinoHint"', 'dinosaur hint HUD element')
    assert_contains(html, "const dinoHintEl = document.getElementById('dinoHint');", 'dinosaur hint DOM lookup')
    assert_contains(html, 'function updateDinoHint()', 'dinosaur hint updater')
    assert_contains(html, 'if (living.length > 0 && living.length <= 2)', 'hint only for one or two dinosaurs')
    assert_contains(html, 'formatDinoDirection(dino)', 'direction formatting helper')
    assert_contains(html, 'updateDinoHint();', 'hint updated with HUD')


def test_wave_counts_and_spawn_guard():
    assert_contains(html, 'let spawningNextWave = false;', 'next wave spawn guard')
    assert_contains(html, 'function getWaveDinoCount()', 'wave count helper')
    assert_contains(html, 'return 6 + (wave - 1) * 10;', 'first wave six then plus ten')
    assert_contains(html, 'if (alive === 0 && running && !gameOver && !spawningNextWave)', 'single next-wave scheduling guard')
    assert_contains(html, 'spawningNextWave = true;', 'spawn guard enabled before timeout')
    assert_contains(html, 'enemies.filter(e => !e.userData.dead && e.parent === scene).length', 'HUD counts only live scene enemies')


def test_multiple_dinosaur_species_models():
    assert_contains(html, "const dinoSpecies = ['trex', 'triceratops', 'pteranodon'];", 'dinosaur species list')
    assert_contains(html, 'function addTrexFeatures(group, mat)', 'trex geometry features')
    assert_contains(html, 'function addTriceratopsFeatures(group, mat)', 'triceratops geometry features')
    assert_contains(html, 'function addPteranodonFeatures(group, mat)', 'pteranodon geometry features')
    assert_contains(html, "type: species", 'species stored in dino userdata')


def test_pteranodon_is_light_and_easy_to_hit():
    assert_contains(html, 'function addPteranodonHitVolume(group, mat)', 'pteranodon generous hit volume helper')
    assert_contains(html, 'hitVolume.userData.isHitVolume = true;', 'pteranodon hit volume marker')
    assert_contains(html, 'hitVolume.material.colorWrite = false;', 'hit volume invisible but raycastable')
    assert_contains(html, 'function makePteranodonSilhouette(group, mat)', 'pteranodon slim silhouette helper')
    assert_contains(html, 'beak.scale.set(1.9, 0.35, 0.35);', 'long bird-like beak')
    assert_contains(html, 'body.scale.set(0.55, 1.18, 0.42);', 'slender long pteranodon body')
    assert_contains(html, 'wing.scale.set(1.9, 1.15, 0.22);', 'wide thin pteranodon wings')


def test_last_two_dinosaurs_force_chase_player():
    assert_contains(html, 'const livingCount = enemies.filter(e => !e.userData.dead && e.parent === scene).length;', 'living dinosaur count before AI loop')
    assert_contains(html, 'const forceChasePlayer = livingCount <= 2;', 'last two force chase flag')
    assert_contains(html, 'if (forceChasePlayer || (data.engageDelay <= 0 && dist < data.chaseRange))', 'last two always chase while others wait for engage delay')


def test_each_wave_adds_one_machine_gun():
    assert_contains(html, 'truck.userData.barrels = [];', 'barrel array initialized')
    assert_contains(html, 'truck.userData.muzzles = [];', 'muzzle array initialized')
    assert_contains(html, 'function setMachineGunCountForWave(waveNumber)', 'per-wave gun count helper')
    assert_contains(html, 'const count = Math.max(1, waveNumber);', 'one active gun per wave number')
    assert_contains(html, 'ensureMachineGunCount(count);', 'creates extra guns as waves increase')
    assert_contains(html, 'setMachineGunCountForWave(wave);', 'wave start updates active gun count')
    assert_contains(html, '.filter(({ index }) => index < truck.userData.activeGunCount)', 'only active wave guns shoot')
    assert_contains(html, 'for (const gunRay of gunRays)', 'shoots every active gun')
    assert_contains(html, 'truck.userData.muzzles[gunRay.index]', 'muzzle flash matches each gun ray')


def test_machine_gun_can_aim_high_for_overhead_pteranodons():
    assert_contains(html, 'const vertical = THREE.MathUtils.clamp(pitch, -0.45, 1.42);', 'gun supports high upward pitch')
    assert_contains(html, 'Math.sin(vertical)', 'gun direction uses true vertical sine')
    assert_contains(html, 'Math.cos(vertical)', 'gun direction uses horizontal cosine')
    assert_contains(html, 'pitch = THREE.MathUtils.clamp(pitch - e.movementY * 0.0018, -0.45, 1.55);', 'pointer lock can aim overhead')
    assert_contains(html, 'pitch = THREE.MathUtils.clamp(-ny * 1.15, -0.45, 1.55);', 'unlocked mouse can aim overhead')


def test_each_wave_applies_new_biome_scene():
    assert_contains(html, 'const biomes = [', 'biome scene list')
    assert_contains(html, "name: '沙漠'", 'desert biome')
    assert_contains(html, "name: '森林'", 'forest biome')
    assert_contains(html, "name: '草原'", 'grassland biome')
    assert_contains(html, 'const biomeObjects = [];', 'biome object registry')
    assert_contains(html, 'function applyBiomeForWave(waveNumber)', 'biome switch helper')
    assert_contains(html, 'clearBiomeObjects();', 'old biome objects are removed')
    assert_contains(html, 'applyBiomeForWave(wave);', 'biome applied at wave start')


def test_large_waves_do_not_all_rush_immediately():
    assert_contains(html, 'engageDelay: 0,', 'dino has engage delay state')
    assert_contains(html, 'dino.userData.engageDelay = wave >= 3 ? rand(2.5, 9.5) + i * 0.12 : rand(0.2, 2.8);', 'staggered engage delay per wave')
    assert_contains(html, 'data.engageDelay = Math.max(0, data.engageDelay - dt);', 'engage delay counts down')
    assert_contains(html, 'if (forceChasePlayer || (data.engageDelay <= 0 && dist < data.chaseRange))', 'chase requires delay and range except last two')
    assert_contains(html, 'const speed = data.speed * (dist < 28 ? 1.06 : 0.88);', 'reduced chase speed')


def test_dinosaur_head_faces_movement_direction():
    assert_contains(html, 'function faceDinoAlongDirection(dino, dir)', 'dinosaur facing helper')
    assert_contains(html, 'dino.rotation.y = Math.atan2(dir.x, dir.z) - Math.PI / 2;', 'head plus x points along movement direction')
    assert_contains(html, 'faceDinoAlongDirection(dino, dir);', 'AI uses facing helper while moving')
    assert_contains(html, 'faceDinoAlongDirection(dino, new THREE.Vector3(-Math.cos(angle), 0, -Math.sin(angle)));', 'spawned dinosaurs initially face map center')


def test_new_wave_refills_health_and_scales_anti_air():
    assert_contains(html, 'let antiAirCharges = 3;', 'anti-air charge state')
    assert_contains(html, 'let antiAirMaxCharges = 3;', 'anti-air max charge state')
    assert_contains(html, 'playerHealth = 100;', 'wave start refills player health')
    assert_contains(html, 'function calculateAntiAirChargesForWave(pteranodonCount)', 'anti-air scales with pteranodon count')
    assert_contains(html, 'antiAirMaxCharges = calculateAntiAirChargesForWave(pteranodonCount);', 'wave start calculates dynamic anti-air max')
    assert_contains(html, 'antiAirCharges = antiAirMaxCharges;', 'wave start fills dynamic anti-air charges')
    assert_contains(html, 'antiAirEl.textContent = antiAirCharges;', 'HUD updates anti-air charge count')
    assert_contains(html, 'antiAirMaxEl.textContent = antiAirMaxCharges;', 'HUD updates anti-air max count')


def test_anti_air_super_weapon_targets_pteranodons():
    assert_contains(html, '<div class="panel">防空武器：<span id="antiAir">3</span>/<span id="antiAirMax">3</span></div>', 'anti-air HUD display')
    assert_contains(html, "const antiAirEl = document.getElementById('antiAir');", 'anti-air DOM lookup')
    assert_contains(html, 'function useAntiAirWeapon()', 'anti-air weapon function')
    assert_contains(html, "e.userData.type === 'pteranodon'", 'anti-air targets only pteranodons')
    assert_contains(html, 'antiAirCharges--;', 'anti-air charges consumed')
    assert_contains(html, 'damageDino(target, target.userData.maxHp, target.position.clone()', 'anti-air destroys selected pteranodon')
    assert_contains(html, "if (k === 'q') useAntiAirWeapon();", 'Q key fires anti-air weapon')


def test_hud_stats_are_collapsible_by_click():
    assert_contains(html, '<div id="topbar">', 'HUD stats are always visible')
    assert_contains(html, '#topbar {', 'HUD topbar CSS rule')
    assert_contains(html, 'opacity: .78;', 'HUD is translucent')
    assert_contains(html, 'pointer-events: none;', 'HUD does not intercept game controls')



def test_machine_gun_visuals_rotate_to_crosshair_direction():
    assert_contains(html, 'function updateMachineGunAiming()', 'machine gun visual aiming helper')
    assert_contains(html, 'barrelPivot.lookAt(aimPoint);', 'gun pivot rotates toward crosshair aim point')
    assert_contains(html, 'muzzle.position.copy(barrelPivot.worldToLocal(aimPoint.clone()).normalize().multiplyScalar(3.25));', 'muzzle follows rotated barrel direction')
    assert_contains(html, 'updateMachineGunAiming();', 'gun aiming updated every camera frame')


def test_new_waves_change_roads_weather_and_scene_props():
    assert_contains(html, 'const roadObjects = [];', 'road object registry')
    assert_contains(html, 'const weatherObjects = [];', 'weather object registry')
    assert_contains(html, 'function createBiomeRoad(biome)', 'biome road creator')
    assert_contains(html, 'function createBiomeWeather(biome)', 'biome weather creator')
    assert_contains(html, "weather: 'rain'", 'rain weather variant')
    assert_contains(html, "weather: 'dust'", 'dust weather variant')
    assert_contains(html, "road: 'straight'", 'straight road variant')
    assert_contains(html, "road: 'river'", 'river or wet road variant')
    assert_contains(html, 'createBiomeRoad(biome);', 'biome applies road changes')
    assert_contains(html, 'createBiomeWeather(biome);', 'biome applies weather changes')


def test_hud_stats_are_always_visible_translucent_overlay():
    assert_contains(html, '<div id="topbar">', 'HUD stats are not initially collapsed')
    assert_contains(html, 'background: rgba(8, 18, 16, .34);', 'HUD panels are more transparent')
    assert_contains(html, 'opacity: .78;', 'HUD overlay opacity is reduced')
    assert_contains(html, 'pointer-events: none;', 'HUD stats do not block sight or clicks')

def test_player_can_summon_dinosaurs_when_out_of_view():
    assert_contains(html, 'function summonDinosaurs()', 'summon dinosaurs helper')
    assert_contains(html, 'dino.userData.engageDelay = 0;', 'summon clears engage delay')
    assert_contains(html, 'dino.userData.chaseRange = worldSize * 2;', 'summon expands chase range')
    assert_contains(html, 'dino.userData.summoned = true;', 'summon marks dinosaurs as summoned')
    assert_contains(html, "if (k === 'e') summonDinosaurs();", 'E key summons dinosaurs')
    assert_contains(html, 'E 召唤恐龙', 'tips mention summon control')


if __name__ == '__main__':
    tests = [test_target_lock_crosshair_and_shooting, test_obstacle_collision_registry_and_truck_blocking, test_crosshair_and_bullets_use_machine_gun_ray, test_dinosaurs_cannot_overlap_truck, test_w_moves_forward_and_s_reverses, test_last_dinosaur_location_hint, test_wave_counts_and_spawn_guard, test_multiple_dinosaur_species_models, test_pteranodon_is_light_and_easy_to_hit, test_last_two_dinosaurs_force_chase_player, test_each_wave_adds_one_machine_gun, test_machine_gun_can_aim_high_for_overhead_pteranodons, test_each_wave_applies_new_biome_scene, test_large_waves_do_not_all_rush_immediately, test_dinosaur_head_faces_movement_direction, test_new_wave_refills_health_and_scales_anti_air, test_anti_air_super_weapon_targets_pteranodons, test_hud_stats_are_collapsible_by_click, test_machine_gun_visuals_rotate_to_crosshair_direction, test_new_waves_change_roads_weather_and_scene_props, test_hud_stats_are_always_visible_translucent_overlay, test_player_can_summon_dinosaurs_when_out_of_view]
    for test in tests:
        test()
    print(f"{len(tests)} regression tests passed")

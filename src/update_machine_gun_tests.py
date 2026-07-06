from pathlib import Path
path = Path('src/tests/game_regression_tests.py')
text = path.read_text(encoding='utf-8')
old = '''def test_second_wave_enables_dual_machine_guns():
    assert_contains(html, 'truck.userData.barrels = [];', 'barrel array initialized')
    assert_contains(html, 'truck.userData.muzzles = [];', 'muzzle array initialized')
    assert_contains(html, 'function setDualMachineGunsEnabled(enabled)', 'dual gun enable helper')
    assert_contains(html, 'setDualMachineGunsEnabled(wave >= 2);', 'dual guns enabled from second wave')
    assert_contains(html, 'function getGunRays()', 'multiple gun rays helper')
    assert_contains(html, 'for (const gunRay of getGunRays())', 'shoots every enabled gun')
'''
new = '''def test_each_wave_adds_one_machine_gun():
    assert_contains(html, 'truck.userData.barrels = [];', 'barrel array initialized')
    assert_contains(html, 'truck.userData.muzzles = [];', 'muzzle array initialized')
    assert_contains(html, 'function setMachineGunCountForWave(waveNumber)', 'per-wave gun count helper')
    assert_contains(html, 'const count = Math.max(1, waveNumber);', 'one active gun per wave number')
    assert_contains(html, 'ensureMachineGunCount(count);', 'creates extra guns as waves increase')
    assert_contains(html, 'setMachineGunCountForWave(wave);', 'wave start updates active gun count')
    assert_contains(html, '.filter(({ index }) => index < truck.userData.activeGunCount)', 'only active wave guns shoot')
    assert_contains(html, 'for (const gunRay of gunRays)', 'shoots every active gun')
    assert_contains(html, 'truck.userData.muzzles[gunRay.index]', 'muzzle flash matches each gun ray')
'''
if old not in text:
    raise SystemExit('old dual gun test not found')
text = text.replace(old, new, 1)
text = text.replace('test_second_wave_enables_dual_machine_guns', 'test_each_wave_adds_one_machine_gun')
path.write_text(text, encoding='utf-8')

from pathlib import Path
path = Path('src/tests/game_regression_tests.py')
text = path.read_text(encoding='utf-8')
insert = '''\n\ndef test_last_two_dinosaurs_force_chase_player():\n    assert_contains(html, 'const livingCount = enemies.filter(e => !e.userData.dead && e.parent === scene).length;', 'living dinosaur count before AI loop')\n    assert_contains(html, 'const forceChasePlayer = livingCount <= 2;', 'last two force chase flag')\n    assert_contains(html, 'if (forceChasePlayer || dist < 70 || wave >= 3)', 'last two always chase player')\n\n\ndef test_second_wave_enables_dual_machine_guns():\n    assert_contains(html, 'truck.userData.barrels = [];', 'barrel array initialized')\n    assert_contains(html, 'truck.userData.muzzles = [];', 'muzzle array initialized')\n    assert_contains(html, 'function setDualMachineGunsEnabled(enabled)', 'dual gun enable helper')\n    assert_contains(html, 'setDualMachineGunsEnabled(wave >= 2);', 'dual guns enabled from second wave')\n    assert_contains(html, 'function getGunRays()', 'multiple gun rays helper')\n    assert_contains(html, 'for (const gunRay of getGunRays())', 'shoots every enabled gun')\n'''
if 'test_last_two_dinosaurs_force_chase_player' not in text:
    text = text.replace("\n\nif __name__ == '__main__':", insert + "\n\nif __name__ == '__main__':")
    text = text.replace('test_pteranodon_is_light_and_easy_to_hit]', 'test_pteranodon_is_light_and_easy_to_hit, test_last_two_dinosaurs_force_chase_player, test_second_wave_enables_dual_machine_guns]')
path.write_text(text, encoding='utf-8')

from pathlib import Path
path = Path('tests/game_regression_tests.py')
text = path.read_text(encoding='utf-8')
insert = '''\n\ndef test_dinosaurs_cannot_overlap_truck():\n    assert_contains(html, 'const truckCollisionRadius = 3.8;', 'truck collision radius for dinosaurs')\n    assert_contains(html, 'function separateDinoFromTruck(dino)', 'dino truck separation helper')\n    assert_contains(html, 'dino.position.x = truck.position.x + away.x * minDistance;', 'push dino outside truck radius')\n    assert_contains(html, 'const canAttackTruck = separateDinoFromTruck(dino);', 'separation result used for attack')\n    assert_contains(html, 'if (canAttackTruck && data.attackCooldown <= 0)', 'attack allowed without overlap')\n'''
if 'test_dinosaurs_cannot_overlap_truck' not in text:
    text = text.replace("\n\nif __name__ == '__main__':", insert + "\n\nif __name__ == '__main__':")
    text = text.replace('test_crosshair_and_bullets_use_machine_gun_ray]', 'test_crosshair_and_bullets_use_machine_gun_ray, test_dinosaurs_cannot_overlap_truck]')
path.write_text(text, encoding='utf-8')

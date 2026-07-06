from pathlib import Path

path = Path('src/tests/game_regression_tests.py')
text = path.read_text(encoding='utf-8')
insert = '''\n\ndef test_crosshair_and_bullets_use_machine_gun_ray():\n    assert_contains(html, 'function getGunDirection()', 'machine gun direction helper')\n    assert_contains(html, 'function getGunRay()', 'machine gun ray helper')\n    assert_contains(html, 'aimRaycaster.set(gunRay.origin, gunRay.direction)', 'raycast from gun muzzle direction')\n    assert_contains(html, 'const aimPoint = getAimPointFromGunRay(gunRay)', 'crosshair projected from gun ray')\n    assert_contains(html, 'barrel.rotation.y = yawOffset;', 'barrel yaw matches gun direction')\n'''
if 'test_crosshair_and_bullets_use_machine_gun_ray' not in text:
    text = text.replace("\n\nif __name__ == '__main__':", insert + "\n\nif __name__ == '__main__':")
    text = text.replace('tests = [test_target_lock_crosshair_and_shooting, test_obstacle_collision_registry_and_truck_blocking]', 'tests = [test_target_lock_crosshair_and_shooting, test_obstacle_collision_registry_and_truck_blocking, test_crosshair_and_bullets_use_machine_gun_ray]')
path.write_text(text, encoding='utf-8')

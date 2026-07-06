from pathlib import Path
path = Path('tools/tests/game_regression_tests.py')
text = path.read_text(encoding='utf-8')
insert = '''\n\ndef test_dinosaur_head_faces_movement_direction():\n    assert_contains(html, 'function faceDinoAlongDirection(dino, dir)', 'dinosaur facing helper')\n    assert_contains(html, 'dino.rotation.y = Math.atan2(dir.x, dir.z) - Math.PI / 2;', 'head plus x points along movement direction')\n    assert_contains(html, 'faceDinoAlongDirection(dino, dir);', 'AI uses facing helper while moving')\n    assert_contains(html, 'faceDinoAlongDirection(dino, new THREE.Vector3(-Math.cos(angle), 0, -Math.sin(angle)));', 'spawned dinosaurs initially face map center')\n'''
if 'test_dinosaur_head_faces_movement_direction' not in text:
    text = text.replace("\n\nif __name__ == '__main__':", insert + "\n\nif __name__ == '__main__':")
    text = text.replace('test_large_waves_do_not_all_rush_immediately]', 'test_large_waves_do_not_all_rush_immediately, test_dinosaur_head_faces_movement_direction]')
path.write_text(text, encoding='utf-8')

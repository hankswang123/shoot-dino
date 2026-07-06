from pathlib import Path
path = Path('src/tests/game_regression_tests.py')
text = path.read_text(encoding='utf-8')
insert = '''\n\ndef test_w_moves_forward_and_s_reverses():\n    assert_contains(html, 'if (input.w) truck.userData.speed -= accel * dt;', 'W accelerates toward visual forward')\n    assert_contains(html, 'if (input.s) truck.userData.speed += reverseAccel * dt;', 'S accelerates toward reverse')\n    assert_contains(html, 'truck.userData.speed = THREE.MathUtils.clamp(truck.userData.speed, -maxForward, -maxReverse);', 'speed clamp supports swapped forward reverse ranges')\n'''
if 'test_w_moves_forward_and_s_reverses' not in text:
    text = text.replace("\n\nif __name__ == '__main__':", insert + "\n\nif __name__ == '__main__':")
    text = text.replace('test_dinosaurs_cannot_overlap_truck]', 'test_dinosaurs_cannot_overlap_truck, test_w_moves_forward_and_s_reverses]')
path.write_text(text, encoding='utf-8')

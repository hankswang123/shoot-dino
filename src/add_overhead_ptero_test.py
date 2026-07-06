from pathlib import Path
path = Path('src/tests/game_regression_tests.py')
text = path.read_text(encoding='utf-8')
insert = '''\n\ndef test_machine_gun_can_aim_high_for_overhead_pteranodons():\n    assert_contains(html, 'const vertical = THREE.MathUtils.clamp(pitch, -0.45, 1.42);', 'gun supports high upward pitch')\n    assert_contains(html, 'Math.sin(vertical)', 'gun direction uses true vertical sine')\n    assert_contains(html, 'Math.cos(vertical)', 'gun direction uses horizontal cosine')\n    assert_contains(html, 'pitch = THREE.MathUtils.clamp(pitch - e.movementY * 0.0018, -0.45, 1.55);', 'pointer lock can aim overhead')\n    assert_contains(html, 'pitch = THREE.MathUtils.clamp(-ny * 1.15, -0.45, 1.55);', 'unlocked mouse can aim overhead')\n'''
if 'test_machine_gun_can_aim_high_for_overhead_pteranodons' not in text:
    text = text.replace("\n\nif __name__ == '__main__':", insert + "\n\nif __name__ == '__main__':")
    text = text.replace('test_second_wave_enables_dual_machine_guns]', 'test_second_wave_enables_dual_machine_guns, test_machine_gun_can_aim_high_for_overhead_pteranodons]')
path.write_text(text, encoding='utf-8')

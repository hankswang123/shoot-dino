from pathlib import Path
path = Path('tools/tests/game_regression_tests.py')
text = path.read_text(encoding='utf-8')
insert = '''\n\ndef test_last_dinosaur_location_hint():\n    assert_contains(html, '<div id="dinoHint"', 'dinosaur hint HUD element')\n    assert_contains(html, "const dinoHintEl = document.getElementById('dinoHint');", 'dinosaur hint DOM lookup')\n    assert_contains(html, 'function updateDinoHint()', 'dinosaur hint updater')\n    assert_contains(html, 'if (living.length > 0 && living.length <= 2)', 'hint only for one or two dinosaurs')\n    assert_contains(html, 'formatDinoDirection(dino)', 'direction formatting helper')\n    assert_contains(html, 'updateDinoHint();', 'hint updated with HUD')\n'''
if 'test_last_dinosaur_location_hint' not in text:
    text = text.replace("\n\nif __name__ == '__main__':", insert + "\n\nif __name__ == '__main__':")
    text = text.replace('test_w_moves_forward_and_s_reverses]', 'test_w_moves_forward_and_s_reverses, test_last_dinosaur_location_hint]')
path.write_text(text, encoding='utf-8')

from pathlib import Path
path = Path('tools/tests/game_regression_tests.py')
text = path.read_text(encoding='utf-8')
insert = '''\n\ndef test_pteranodon_is_light_and_easy_to_hit():\n    assert_contains(html, 'function addPteranodonHitVolume(group, mat)', 'pteranodon generous hit volume helper')\n    assert_contains(html, 'hitVolume.userData.isHitVolume = true;', 'pteranodon hit volume marker')\n    assert_contains(html, 'hitVolume.material.colorWrite = false;', 'hit volume invisible but raycastable')\n    assert_contains(html, 'function makePteranodonSilhouette(group, mat)', 'pteranodon slim silhouette helper')\n    assert_contains(html, 'beak.scale.set(1.9, 0.35, 0.35);', 'long bird-like beak')\n    assert_contains(html, 'body.scale.set(0.55, 1.18, 0.42);', 'slender long pteranodon body')\n    assert_contains(html, 'wing.scale.set(1.9, 1.15, 0.22);', 'wide thin pteranodon wings')\n'''
if 'test_pteranodon_is_light_and_easy_to_hit' not in text:
    text = text.replace("\n\nif __name__ == '__main__':", insert + "\n\nif __name__ == '__main__':")
    text = text.replace('test_multiple_dinosaur_species_models]', 'test_multiple_dinosaur_species_models, test_pteranodon_is_light_and_easy_to_hit]')
path.write_text(text, encoding='utf-8')

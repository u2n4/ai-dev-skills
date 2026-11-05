"""Schema tests for the marketplace, plugin manifests and skill frontmatter.

Run from the repo root: uv run --with pyyaml==6.0.2 python -m unittest discover -s tests -v
"""

import json
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
PLUGIN_MANIFESTS = sorted((ROOT / "plugins").glob("*/.claude-plugin/plugin.json"))
SKILL_FILES = sorted((ROOT / "plugins").glob("*/skills/*/SKILL.md"))
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def split_frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        raise ValueError("file must start with '---' on line 1")
    for i in range(1, len(lines)):
        if lines[i] == "---":
            return lines[1:i]
    raise ValueError("frontmatter has no closing '---'")


class MarketplaceTests(unittest.TestCase):
    def test_marketplace_has_name_owner_and_plugins(self):
        data = load_json(MARKETPLACE)
        self.assertIsInstance(data.get("name"), str)
        self.assertTrue(data["name"])
        self.assertIsInstance(data.get("owner"), dict)
        self.assertIsInstance(data.get("plugins"), list)
        self.assertGreater(len(data["plugins"]), 0)

    def test_each_plugin_entry_points_to_its_own_manifest(self):
        data = load_json(MARKETPLACE)
        for entry in data["plugins"]:
            with self.subTest(plugin=entry.get("name")):
                source = entry.get("source")
                self.assertIsInstance(source, str)
                self.assertTrue(source.startswith("./"), source)
                manifest = ROOT / source[2:] / ".claude-plugin" / "plugin.json"
                self.assertTrue(manifest.is_file(), f"missing {manifest}")
                self.assertEqual(load_json(manifest)["name"], entry["name"])


class PluginManifestTests(unittest.TestCase):
    def test_plugin_manifests_exist(self):
        self.assertEqual(len(PLUGIN_MANIFESTS), 2, PLUGIN_MANIFESTS)

    def test_plugin_manifests_have_name_and_semver_version(self):
        for path in PLUGIN_MANIFESTS:
            with self.subTest(manifest=str(path.relative_to(ROOT))):
                data = load_json(path)
                self.assertIsInstance(data.get("name"), str)
                self.assertTrue(data["name"])
                self.assertRegex(data.get("version", ""), SEMVER)
                self.assertIsInstance(data.get("description"), str)

    def test_no_placeholder_values_left_in_manifests(self):
        for path in [MARKETPLACE, *PLUGIN_MANIFESTS]:
            with self.subTest(manifest=str(path.relative_to(ROOT))):
                self.assertNotIn("UPDATE_ON_RELEASE", path.read_text(encoding="utf-8"))


class SkillFrontmatterTests(unittest.TestCase):
    def test_skill_files_exist(self):
        self.assertEqual(len(SKILL_FILES), 2, SKILL_FILES)

    def test_frontmatter_parses_and_has_name_and_description(self):
        for path in SKILL_FILES:
            with self.subTest(skill=str(path.relative_to(ROOT))):
                fm = yaml.safe_load("\n".join(split_frontmatter(path.read_text(encoding="utf-8"))))
                self.assertIsInstance(fm, dict)
                self.assertEqual(fm.get("name"), path.parent.name)
                self.assertIsInstance(fm.get("description"), str)
                self.assertTrue(fm["description"].strip())

    def test_description_is_quoted_when_it_contains_colon_space(self):
        for path in SKILL_FILES:
            with self.subTest(skill=str(path.relative_to(ROOT))):
                for line in split_frontmatter(path.read_text(encoding="utf-8")):
                    if line.startswith("description:"):
                        value = line[len("description:"):].strip()
                        if ": " in value:
                            self.assertTrue(
                                value[:1] in ("'", '"'),
                                "description contains ': ' and must be quoted",
                            )


if __name__ == "__main__":
    unittest.main()

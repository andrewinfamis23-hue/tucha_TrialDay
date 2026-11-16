import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class SandboxLayoutTest(unittest.TestCase):
    def test_no_production_artifacts_are_packaged(self) -> None:
        forbidden = {".env", "update.sh", "deploy.ps1"}
        packaged = {path.name.casefold() for path in ROOT.rglob("*") if path.is_file()}
        self.assertTrue(forbidden.isdisjoint(packaged))

    def test_exactly_six_business_menus_are_declared(self) -> None:
        source = (ROOT / "addons/tucha_crm/views/views.xml").read_text(encoding="utf-8")
        children = source.count('parent="menu_tucha_root"')
        self.assertEqual(children, 6)

    def test_wms_mock_is_runtime_isolated(self) -> None:
        compose = (ROOT / "compose.yaml").read_text(encoding="utf-8")
        seed = (ROOT / "docker/seed_data.sql").read_text(encoding="utf-8")
        self.assertIn('"127.0.0.1:18069:8069"', compose)
        self.assertIn("CREATE SCHEMA IF NOT EXISTS wms_mock", seed)
        self.assertIn("GRANT SELECT ON ALL TABLES IN SCHEMA wms_mock", seed)
        self.assertNotIn('"127.0.0.1:15432:5432"', compose)


if __name__ == "__main__":
    unittest.main()

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
        self.assertIn('"127.0.0.1:80:80"', compose)
        self.assertNotIn("18069", compose)
        self.assertIn("CREATE SCHEMA IF NOT EXISTS wms_mock", seed)
        self.assertIn("GRANT SELECT ON ALL TABLES IN SCHEMA wms_mock", seed)
        self.assertNotIn('"127.0.0.1:15432:5432"', compose)

    def test_addon_path_is_not_hidden_by_odoo_volume(self) -> None:
        dockerfile = (ROOT / "docker/Dockerfile").read_text(encoding="utf-8")
        config = (ROOT / "docker/odoo.conf").read_text(encoding="utf-8")
        self.assertIn("/opt/tucha-addons/tucha_crm", dockerfile)
        self.assertIn("addons_path = /opt/tucha-addons,", config)
        self.assertNotIn("COPY addons/tucha_crm /mnt/extra-addons", dockerfile)

    def test_candidate_entry_points_exist(self) -> None:
        hooks = (ROOT / "addons/tucha_crm/hooks.py").read_text(encoding="utf-8")
        views = (ROOT / "addons/tucha_crm/views/views.xml").read_text(encoding="utf-8")
        tasks = (ROOT / "TASKS.md").read_text(encoding="utf-8")
        self.assertIn('"login": "manager@example.test"', hooks)
        self.assertEqual(hooks.count('"lang": "ru_RU"'), 2)
        self.assertIn('id="action_tucha_request_import"', views)
        self.assertIn("Куда нажать", tasks)
        self.assertIn("SOLUTION.md", tasks)

    def test_single_database_opens_without_database_manager(self) -> None:
        config = (ROOT / "docker/odoo.conf").read_text(encoding="utf-8")
        startup = (ROOT / "docker/start-sandbox.sh").read_text(encoding="utf-8")
        self.assertIn("list_db = False", config)
        self.assertNotIn("dbfilter", config)
        self.assertIn("proxy_mode = True", config)
        self.assertIn('--database="$DB_NAME"', startup)

    def test_prod_ui_is_pinned_and_has_no_production_connection(self) -> None:
        manifest = (ROOT / "addons/tucha_crm/__manifest__.py").read_text(encoding="utf-8")
        provenance = (ROOT / "docs/PROD_UI_SOURCE.md").read_text(encoding="utf-8")
        proxy = (ROOT / "docker/nginx.conf").read_text(encoding="utf-8")
        self.assertIn("sandbox_interface.js", manifest)
        self.assertIn("12df4b9", provenance)
        self.assertIn("proxy_pass http://odoo:8069", proxy)
        self.assertNotIn("94.141.162.84", provenance)

    def test_candidate_reasoning_and_ai_use_are_reviewed(self) -> None:
        worklog = (ROOT / "WORKLOG.md").read_text(encoding="utf-8")
        self.assertFalse((ROOT / "EVALUATION.md").exists())
        self.assertFalse((ROOT / "INTERVIEW.md").exists())
        self.assertIn("Что в задании было неясно", worklog)
        self.assertIn("Что предложил ИИ", worklog)
        self.assertIn("Как я это проверил", worklog)


if __name__ == "__main__":
    unittest.main()

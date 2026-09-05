import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "monitor_github", Path(__file__).parents[1] / "scripts" / "monitor_github.py"
)
monitor = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(monitor)


class MonitorTests(unittest.TestCase):
    def test_autobot_is_highlighted_and_workflow_is_linked(self):
        repository = {
            "name": "Autobot",
            "full_name": "JungyulPark/Autobot",
            "html_url": "https://github.com/JungyulPark/Autobot",
            "private": False,
            "pushed_at": "2026-08-19T00:00:00Z",
            "updated_at": "2026-08-19T00:00:00Z",
        }
        with patch.object(
            monitor,
            "workflow_status",
            return_value=("success", "https://github.com/run/1"),
        ):
            report = monitor.build_report("JungyulPark", [repository], None)

        self.assertIn("**Autobot (watched)**", report)
        self.assertIn("[success](https://github.com/run/1)", report)
        self.assertIn("Repositories checked: **1**", report)

    def test_pagination_collects_every_repository(self):
        first_page = [
            {"name": str(number), "full_name": f"JungyulPark/{number}"}
            for number in range(100)
        ]
        final_repository = {"name": "last", "full_name": "JungyulPark/last"}
        with patch.object(
            monitor, "api_get", side_effect=[(first_page, {}), ([final_repository], {})]
        ):
            repositories = monitor.all_repositories("JungyulPark", None)

        self.assertEqual(101, len(repositories))


if __name__ == "__main__":
    unittest.main()

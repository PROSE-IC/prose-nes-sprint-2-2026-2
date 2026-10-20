from pathlib import Path
import math
import sys
import unittest

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from common.dashboard_app import load_all_team_reports, load_reports


def comparison_with_two_teams():
    import pandas as pd
    from common.dashboard_app import render_team_comparison
    frame = pd.DataFrame([
        {'Equipe': 'T1', 'Sprint': 'Sprint 2', 'Dimens\u00e3o': 'SPACE-P (Performance)', 'Nota': 5.83},
        {'Equipe': 'T2', 'Sprint': 'Sprint 2', 'Dimens\u00e3o': 'SPACE-P (Performance)', 'Nota': 7.00},
    ])
    render_team_comparison(frame, 'T1', ['Sprint 2'], ['SPACE-P (Performance)'])


class DashboardTest(unittest.TestCase):
    def test_scope_and_reports(self):
        teams = {path.name for path in (ROOT / 'teams').iterdir() if path.is_dir()}
        self.assertEqual(teams, {'t1'})
        reports = load_reports(ROOT / 'teams/t1/data/relatos', 'T1')
        self.assertEqual([report.sprint for report in reports], ['Sprint 0', 'Sprint 1', 'Sprint 2'])
        self.assertEqual(len(load_all_team_reports(ROOT / 'teams/t1')), 3)
        current = reports[-1]
        self.assertEqual(current.participation, '6/6 (100.0%)')
        self.assertTrue(math.isclose(current.overall, 6.894097222222222, abs_tol=0.005))
        self.assertEqual(len(current.space), 4)
        self.assertEqual(len(current.top5), 5)
        self.assertEqual(len(current.bottom5), 5)
        partial = [label for label, _ in current.top5 + current.bottom5 if 'Discuss' in label]
        self.assertTrue(partial)
        self.assertTrue(all('2 respostas' in label for label in partial))

    def test_app_and_filters(self):
        app = AppTest.from_file(str(ROOT / 'teams/t1/app.py'), default_timeout=30).run()
        self.assertFalse(app.exception)
        self.assertIn('T1', app.title[0].value)
        self.assertEqual(app.sidebar.multiselect[0].value, ['Sprint 0', 'Sprint 1', 'Sprint 2'])
        self.assertEqual(len(app.get('plotly_chart')), 3)
        self.assertTrue(any('pelo menos duas equipes' in info.value for info in app.info))
        app.sidebar.multiselect[0].set_value(['Sprint 2']).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox[0].value, 'Sprint 2')
        self.assertTrue(any(metric.label == 'Nota do Survey' and metric.value == '6.89' for metric in app.metric))
        app.sidebar.multiselect[1].set_value(['SPACE-P (Performance)']).run()
        self.assertFalse(app.exception)
        self.assertTrue(any(metric.label == 'M\u00e9dia SPACE filtrada' and metric.value == '5.83' for metric in app.metric))

    def test_comparison_supports_future_teams(self):
        app = AppTest.from_function(comparison_with_two_teams, default_timeout=30).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.get('plotly_chart')), 1)
        self.assertFalse(app.info)
        self.assertTrue(any('T1, T2' in caption.value for caption in app.caption))


if __name__ == '__main__':
    unittest.main()

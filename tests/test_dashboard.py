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
        self.assertEqual(teams, {'t1', 't7', 't10'})
        reports = load_reports(ROOT / 'teams/t1/data/relatos', 'T1')
        self.assertEqual([report.sprint for report in reports], ['Sprint 0', 'Sprint 1', 'Sprint 2'])
        self.assertEqual(len(load_all_team_reports(ROOT / 'teams/t1')), 9)
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
        self.assertEqual(len(app.get('plotly_chart')), 4)
        self.assertFalse(any('pelo menos duas equipes' in info.value for info in app.info))
        self.assertTrue(any('T1, T7, T10' in caption.value for caption in app.caption))
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

    def test_t7_reports_and_filtered_dashboard(self):
        reports = load_reports(ROOT / 'teams/t7/data/relatos', 'T7')
        self.assertEqual([report.sprint for report in reports], ['Sprint 0', 'Sprint 1', 'Sprint 2'])
        current = reports[-1]
        self.assertEqual(current.participation, '1/6 (16.7%)')
        self.assertEqual(current.overall, 5.0)
        self.assertEqual(len(current.space), 4)
        self.assertFalse(any('Discuss' in label for label, _ in current.top5 + current.bottom5))
        app = AppTest.from_file(str(ROOT / 'teams/t7/app.py'), default_timeout=30).run()
        self.assertFalse(app.exception)
        self.assertIn('T7', app.title[0].value)
        self.assertEqual(len(app.get('plotly_chart')), 4)
        app.sidebar.multiselect[0].set_value(['Sprint 2']).run()
        self.assertFalse(app.exception)
        self.assertTrue(any(metric.label == 'Nota do Survey' and metric.value == '5.00' for metric in app.metric))
        self.assertTrue(any('T1, T7, T10' in caption.value for caption in app.caption))

    def test_t10_reports_and_filtered_dashboard(self):
        reports = load_reports(ROOT / 'teams/t10/data/relatos', 'T10')
        self.assertEqual([report.sprint for report in reports], ['Sprint 0', 'Sprint 1', 'Sprint 2'])
        current = reports[-1]
        self.assertEqual(current.participation, '5/6 (83.3%)')
        self.assertTrue(math.isclose(current.overall, 5.527083333333334, abs_tol=.005))
        self.assertEqual(len(current.space), 4)
        self.assertIn(('Participa\u00e7\u00e3o nas discuss\u00f5es da equipe', 8.0), current.top5)
        self.assertTrue(any('2 respostas v\u00e1lidas' in label for label, _ in current.top5))
        app = AppTest.from_file(str(ROOT / 'teams/t10/app.py'), default_timeout=30).run()
        self.assertFalse(app.exception)
        self.assertIn('T10', app.title[0].value)
        self.assertEqual(len(app.get('plotly_chart')), 4)
        app.sidebar.multiselect[0].set_value(['Sprint 2']).run()
        self.assertFalse(app.exception)
        self.assertTrue(any(metric.label == 'Nota do Survey' and metric.value == '5.53' for metric in app.metric))
        self.assertTrue(any('T1, T7, T10' in caption.value for caption in app.caption))


if __name__ == '__main__':
    unittest.main()

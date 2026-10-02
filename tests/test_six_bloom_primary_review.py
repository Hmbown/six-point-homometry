"""Cross-implementation regressions for the independently written attack."""
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
import six_bloom_primary as author
import six_bloom_primary_review as review
import six_bloom_support as support


class FreshAuditTests(unittest.TestCase):
    def test_raw_catalogue_preserves_nonunit_scales(self):
        catalogue = review.raw_collisions()
        doubles = [tuple(row['normal']) for row in catalogue if row['scales'] == [1, 2]]
        self.assertEqual(set(doubles), {(0, 1), (1, 0), (1, -1)})
        self.assertEqual(len(catalogue), 12)

    def test_all_finite_images_against_separate_gap_keys(self):
        for independent in review.small_images():
            n = independent['n']
            gap = author.small_image(n)
            self.assertEqual(independent['support'], support.support_count(n))
            self.assertEqual(independent['nontrivial_edges'], gap['nontrivial_pair_count'])
            self.assertEqual(len(independent['congruent_parameters']), gap['congruent_parameters'])
            self.assertEqual(independent['fiber_size_histogram'], gap['fiber_histogram'])

    def test_saved_complete_tables_every_histogram_entry(self):
        independent = json.loads((ROOT/'results/2026-10-01-six-primary-review/independent-audit.json').read_text())
        paired = json.loads((ROOT/'results/2026-10-01-six-bloom-primary/pair-certificate.json').read_text())
        actual = independent['paired']
        self.assertEqual(actual['processed'], 4_147_200)
        self.assertEqual(actual['ranks'], paired['ranks'])
        for rank in ('rank1', 'rank2'):
            expected = [{k: v for k, v in row.items() if k != 'witness'} for row in paired[rank]]
            self.assertEqual(actual[rank], expected)
        endpoint = json.loads((ROOT/'results/2026-10-01-six-bloom-primary/endpoint-certificate.json').read_text())
        original = independent['endpoint_original_minors']
        self.assertEqual(original['original_matrix_ranks'],
                         {str(int(rank)+2): count for rank, count in endpoint['ranks'].items()})
        self.assertEqual(original['rank4'],
                         [{'third_minor_gcd': row['content'], 'fourth_minor_gcd': row['minor_gcd'],
                           'count': row['count']} for row in endpoint['rank2']])

    def test_different_pivot_affordability_slice(self):
        with redirect_stdout(StringIO()):
            result = review.paired_y_pivot(1)
        self.assertEqual(result['processed'], 518400)
        self.assertEqual(sum(result['ranks'].values()), result['processed'])
        self.assertLessEqual(result['max_entry'], 30)
        self.assertLessEqual(result['max_minor'], 120)

    def test_independent_even_shared_endpoint_exhibits(self):
        independent = review.even_controls()
        self.assertEqual(len(independent), 120)
        self.assertEqual((independent[0]['n'], independent[-1]['n']), (18, 256))
        for row in independent:
            self.assertEqual(len(set(map(tuple, row['classes']))), 3)
            self.assertEqual(row['classes'][1], row['classes'][2])


if __name__ == '__main__':
    unittest.main(verbosity=2)

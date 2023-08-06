from unittest import TestCase
from EDAspy.optimization import EMNA
from EDAspy.benchmarks import ContinuousBenchmarkingCEC14
import numpy as np


class TestUMDAc(TestCase):

    def test_constructor(self):
        n_variables = 10
        emna = EMNA(size_gen=300, max_iter=100, dead_iter=20, n_variables=10, landscape_bounds=(-60, 60), alpha=0.5)

        assert emna.size_gen == 300
        assert emna.max_iter == 100
        assert emna.dead_iter == 20
        assert emna.n_variables == n_variables
        assert emna.alpha == 0.5
        assert emna.landscape_bounds == (-60, 60)

    def test_new_generation(self):
        n_variables = 10
        emna = EMNA(size_gen=300, max_iter=100, dead_iter=20, n_variables=10, landscape_bounds=(-60, 60))
        benchmarking = ContinuousBenchmarkingCEC14(n_variables)

        emna.minimize(benchmarking.cec14_4, False)

        assert emna.generation.shape[0] == emna.size_gen + (emna.size_gen * emna.elite_factor)

    def test_check_generation(self):
        n_variables = 10
        emna = EMNA(size_gen=300, max_iter=100, dead_iter=20, n_variables=10, landscape_bounds=(-60, 60))

        gen = np.random.normal(
            [0]*emna.n_variables, [10]*emna.n_variables, [emna.size_gen, emna.n_variables]
        )
        emna.generation = gen
        benchmarking = ContinuousBenchmarkingCEC14(n_variables)
        emna._check_generation(benchmarking.cec14_4)
        assert len(emna.evaluations) == len(emna.generation)


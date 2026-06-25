import pytest
import math
from stream_stats import QuickStats

def test_empty():
    qs = QuickStats()
    assert qs.n == 0
    assert math.isnan(qs.avg)
    assert math.isnan(qs.s)

def test_new_obs():
    qs = QuickStats()
    qs.new_obs(1).new_obs(2).new_obs(3)
    assert qs.n == 3
    assert qs.avg == pytest.approx(2)
    assert qs.s == pytest.approx(1)
    assert qs.max == pytest.approx(3)
    assert qs.min == pytest.approx(1)
    assert qs.mle_var == pytest.approx(2.0 / 3.0)

def test_add_all():
    qs = QuickStats()
    qs.add_all([1, 2, 3])
    assert qs.n == 3
    assert qs.avg == pytest.approx(2)
    assert qs.s == pytest.approx(1)
    assert qs.max == pytest.approx(3)
    assert qs.min == pytest.approx(1)
    assert qs.mle_var == pytest.approx(2.0 / 3.0)

def test_reset():
    qs = QuickStats()
    qs.add_all([1,2,3,4,5])
    assert qs.n == 5
    qs.reset()
    assert qs.n == 0
    assert math.isnan(qs.avg)
    assert math.isnan(qs.s)
    assert qs.max == -math.inf
    assert qs.min == math.inf

def test_loss():
    qs = QuickStats()
    qs.add_all([1, 2, 3])
    assert qs.loss() == pytest.approx(5.0)
    assert qs.loss(target = 5) == pytest.approx(10.0)

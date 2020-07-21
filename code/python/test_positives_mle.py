import pytest

from positives_mle import PositivesMLE


@pytest.mark.parametrize(('recall'
                         , 'fpr'
                          , 'expected')
    , [
                             pytest.param(
                                 0.69
                                 , 0.045
                                 , 0.045
                                 , id='regular1')
     ])
def test_range_low_bound(recall
                         , fpr
                          , expected):
    p = PositivesMLE(recall
                         , fpr)
    actual = p.range_low_bound()
    assert expected == actual

@pytest.mark.parametrize(('recall'
                         , 'fpr'
                          , 'expected')
    , [
                             pytest.param(
                                 0.69
                                 , 0.045
                                 , 0.69
                                 , id='regular1')
     ])
def test_range_high_bound(recall
                         , fpr
                          , expected):
    p = PositivesMLE(recall
                         , fpr)
    actual = p.range_high_bound()
    assert expected == actual


@pytest.mark.parametrize(('recall'
                         , 'fpr'
                          , 'val'
                          , 'expected')
    , [
                             pytest.param(
                                 0.69
                                 , 0.045
                                 , 0.01
                                 , False
                                 , id='below')
                             , pytest.param(
                                 0.69
                                 , 0.045
                                 , 0.3
                                 , True
                                 , id='in')
                             , pytest.param(
                                 0.69
                                 , 0.045
                                 , 0.8
                                 , False
                                 , id='above')
                         ])
def test_is_in_range(recall
                         , fpr
                         , val
                         , expected):
    p = PositivesMLE(recall
                         , fpr)
    actual = p.is_in_range(val)
    assert expected == actual



@pytest.mark.parametrize(('recall'
                         , 'fpr'
                          , 'val'
                          , 'expected')
    , [
                             pytest.param(
                                 0.69
                                 , 0.045
                                 , 0.01
                                 , -0.054263566
                                 , id='below')
                             , pytest.param(
                                 0.69
                                 , 0.045
                                 , 0.3
                                 , 0.395348837

                                 , id='in')
                             , pytest.param(
                                 0.69
                                 , 0.045
                                 , 0.8
                                 , 1.170542636
                                 , id='above')
                         ])
def test_estimate_positives(recall
                         , fpr
                         , val
                         , expected):
    p = PositivesMLE(recall
                         , fpr)
    actual = round(p.estimate_positives(val),3)
    assert round(expected, 3) == actual


@pytest.mark.parametrize(('recall'
                         , 'fpr'
                          , 'expected')
    , [
                             pytest.param(
                                 0.69
                                 , 0.045
                                 , 'f(x)=1.55*x -0.07'
                                 , id='regular1')
     ])
def test_get_formula(recall
                         , fpr
                          , expected):
    p = PositivesMLE(recall
                         , fpr)
    actual = p.get_formula()
    assert expected == actual

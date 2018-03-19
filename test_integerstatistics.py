from roulette import IntegerStatistics

def test_integerstatistics():
    '''Test that statistics are calculated correctly for a sample dataset.'''
    data = [10,8,13,9,11,14,6,4,12,7,5]
    sample = IntegerStatistics(data)
    assert sample.mean() == 9.0
    assert len(sample) == 11.0
    assert sum(sample) == 99
    assert round(sample.stdev(),3) == 3.317
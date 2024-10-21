from lib.mapAsync import mapAsync

def test_mapAsync():
    assert mapAsync(lambda x: x + 1)([1, 2, 3]) == [2, 3, 4]

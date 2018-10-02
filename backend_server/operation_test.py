import operations as op

def test_basic():
    list = op.getNewsSummariesForUser("test", 1)
    print(list)

if __name__ == "__main__":
    test_basic()

import mongodb_client as client

def test_basic():
    db = client.get_db('tap-news')

    assert db.news.count() == 1551
    print("good")

if __name__ == "__main__":
    test_basic()

from telliot_feeds.queries.abi_query import AbiQuery
from telliot_feeds.queries.morphware import Morphware


def test_query_data():
    q = Morphware(version=1)
    print(q.query_data.hex())
    print(q.abi)
    print(q.query_id.hex())

    qr = AbiQuery.get_query_from_data(q.query_data)
    assert isinstance(qr, Morphware)
    assert qr.version == 1


def test_get_query_from_data():
    query_data = (
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\tMorphwar"
        b"e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x01"
    )

    q = AbiQuery.get_query_from_data(query_data)
    print(q)

    assert isinstance(q, Morphware)
    assert q.version == 1


def test_generate_query_data():
    """Test correct query data if query has no parameters."""

    class FakeQueryType(AbiQuery):
        pass

    q = FakeQueryType()

    print(q.query_data.hex())
    print(q.query_id.hex())

    assert (
        q.query_data.hex()
        == "00000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000080000000000000000000000000000000000000000000000000000000000000000d46616b6551756572795479706500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000"  # noqa: E501
    )
    assert q.query_id.hex() == "b0437cc90a5c0e7aab994a16a941b6823d05ef5067b90085fc19f86f464da3de"

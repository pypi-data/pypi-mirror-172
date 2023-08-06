from abf.utils import aws


def test_tag_dict_to_aws():
    results = aws.tag_dict_to_aws({"Key": "Value"})
    assert [{"Key": "Key", "Value": "Value"}] == results

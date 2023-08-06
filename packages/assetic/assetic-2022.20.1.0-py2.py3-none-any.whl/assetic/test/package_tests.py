"""
Need py3.7 min to run pytest
"""
import assetic


def init_asseticsdk():
    """
    Test initialising the SDK
    Assumes default settings
    :return: True unless exception
    """
    try:
        asseticsdk = assetic.AsseticSDK()
    except Exception as ex:
        raise ex
    return True


def test_answer():
    assert init_asseticsdk() == True

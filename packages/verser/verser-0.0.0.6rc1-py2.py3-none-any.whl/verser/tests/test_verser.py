from ..verser_ import create_version_instance, VersionParts, get_next_version
import random


def test_create_version_instance():
    assert create_version_instance("1.0.17.2rc2") == VersionParts(1, 0, 17, 2, 2, True)
    assert create_version_instance("1.0.17.2") == VersionParts(1, 0, 17, 2, 0, False)
    assert create_version_instance("1.0.17.3rc4") == VersionParts(1, 0, 17, 3, 4, True)


def test_get_next_version(capsys):
    for item in range(100):
        # inc = random.choice((True, False,))
        inc = True
        pre = random.choice((True, False,))
        with capsys.disabled():
            n = get_next_version(increment=inc, pre_release=pre, verbose=True)
            assert n is not None

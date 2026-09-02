# Standard ament_python test boilerplate, unchanged from the pattern
# `ros2 pkg create --build-type ament_python` generates. This course does
# not enforce a copyright header, so the check is skipped rather than run
# against a header format the package intentionally does not use.
import pytest


@pytest.mark.copyright
@pytest.mark.linter
@pytest.mark.skip(reason='This teaching example does not use a copyright header.')
def test_copyright():
    pass

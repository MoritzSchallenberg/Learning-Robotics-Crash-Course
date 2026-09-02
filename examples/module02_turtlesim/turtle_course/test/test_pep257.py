# Standard ament_python test boilerplate, unchanged from the pattern
# `ros2 pkg create --build-type ament_python` generates.
from ament_pep257.main import main


def test_pep257():
    rc = main(argv=['.', 'test'])
    assert rc == 0, 'Found code style errors / warnings'

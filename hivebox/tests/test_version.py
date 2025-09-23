# tests/test_version.py
import pytest
from app.version import get_version, print_version
   
def test_get_version():
    """Test get_version returns correct version string"""
    version = get_version()
    assert version == "0.1.0"
    assert isinstance(version, str)
   
def test_print_version(capsys):
    """Test print_version outputs correct format"""
    returned_version = print_version()
    captured = capsys.readouterr()
       
    assert "HiveBox version: 0.1.0" in captured.out
    assert returned_version == "0.1.0"
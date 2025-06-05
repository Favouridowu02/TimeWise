import os
import logging
import pytest
from utils.logging_utils import setup_logging

# Python

def test_log_file_created(tmp_path):
    log_file = tmp_path / "mylog.log"
    setup_logging(str(log_file))
    assert log_file.exists()

def test_console_and_file_logging(tmp_path, capsys):
    log_file = tmp_path / "test.log"
    setup_logging(str(log_file))
    logger = logging.getLogger()
    logger.info("Hello Info")
    logger.debug("Hello Debug")
    # Flush handlers
    for h in logger.handlers:
        h.flush()
    # Check file content
    with open(log_file, "r") as f:
        content = f.read()
    assert "Hello Info" in content
    assert "Hello Debug" in content
    # Check console output (INFO only)
    captured = capsys.readouterr()
    assert "Hello Info" in captured.out or "Hello Info" in captured.err

def test_debug_not_in_console(tmp_path, capsys):
    log_file = tmp_path / "debug.log"
    setup_logging(str(log_file))
    logger = logging.getLogger()
    logger.debug("DebugOnly")
    for h in logger.handlers:
        h.flush()
    captured = capsys.readouterr()
    assert "DebugOnly" not in captured.out
    assert "DebugOnly" not in captured.err

def test_log_dir_created(tmp_path):
    log_dir = tmp_path / "logs"
    log_file = log_dir / "file.log"
    assert not log_dir.exists()
    setup_logging(str(log_file))
    assert log_dir.exists()
    assert log_file.exists()

def test_no_duplicate_handlers(tmp_path):
    log_file = tmp_path / "dup.log"
    setup_logging(str(log_file))
    logger = logging.getLogger()
    logger.info("First")
    setup_logging(str(log_file))
    logger.info("Second")
    for h in logger.handlers:
        h.flush()
    with open(log_file, "r") as f:
        lines = f.readlines()
    # Should only have one "First" and one "Second"
    assert sum("First" in l for l in lines) == 1
    assert sum("Second" in l for l in lines) == 1

def test_permission_error(monkeypatch, tmp_path):
    def raise_perm(*a, **kw):
        raise PermissionError("No permission")
    monkeypatch.setattr("logging.handlers.RotatingFileHandler.__init__", raise_perm)
    log_file = tmp_path / "fail.log"
    with pytest.raises(PermissionError):
        setup_logging(str(log_file))
import logging
import pytest
from utils.logging_utils import setup_logging

# Python


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
    assert "Hello Debug" not in captured.out
    assert "Hello Debug" not in captured.err
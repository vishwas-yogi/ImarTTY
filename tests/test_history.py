import os
import pytest
from utils.history import HistoryManager

@pytest.fixture
def history_manager(tmp_path):
    db_path = tmp_path / "test_history.db"
    return HistoryManager(db_path=str(db_path))

def test_add_and_get_recent(history_manager):
    history_manager.add_entry("echo hello", 0, "hello\n")
    history_manager.add_entry("ls", 0, "file1\nfile2\n")
    
    recent = history_manager.get_recent()
    assert len(recent) == 2
    assert recent[0][1] == "ls"  # Most recent first
    assert recent[1][1] == "echo hello"

def test_search(history_manager):
    history_manager.add_entry("git status", 0, "")
    history_manager.add_entry("git commit", 0, "")
    history_manager.add_entry("ls", 0, "")
    
    results = history_manager.search("git")
    assert len(results) == 2
    assert results[0][1] == "git commit"
    assert results[1][1] == "git status"

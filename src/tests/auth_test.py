import pytest
import bcrypt
import sqlite3
import sys
sys.path.append("src")
from unittest.mock import patch, MagicMock
from game.auth import AuthManager

@patch("game.auth.sqlite3.connect")
def test_create_user_table(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_conn

    auth = AuthManager()
    auth.create_user_table()

    mock_conn.execute.assert_called_once()
    assert "CREATE TABLE IF NOT EXISTS users" in mock_conn.execute.call_args[0][0]

@patch("game.auth.sqlite3.connect")
def test_register_user_success(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_conn

    auth = AuthManager()
    result = auth.register_user("testuser", "password")

    assert result is True
    mock_conn.execute.assert_called_once()

@patch("game.auth.sqlite3.connect")
def test_login_user_success(mock_connect):
    hashed = bcrypt.hashpw("password".encode(), bcrypt.gensalt()).decode("utf-8")
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (hashed,)
    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_cursor
    mock_connect.return_value.__enter__.return_value = mock_conn

    auth = AuthManager()
    result = auth.login_user("testuser", "password")

    assert result is True

@patch("game.auth.sqlite3.connect")
def test_login_user_fail(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_cursor
    mock_connect.return_value.__enter__.return_value = mock_conn

    auth = AuthManager()
    result = auth.login_user("testuser", "wrongpassword")

    assert result is False

@patch("game.auth.sqlite3.connect")
def test_get_user_id_found(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_cursor
    mock_connect.return_value.__enter__.return_value = mock_conn

    auth = AuthManager()
    user_id = auth.get_user_id("testuser")

    assert user_id == 1

@patch("game.auth.sqlite3.connect")
def test_get_user_id_not_found(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_cursor
    mock_connect.return_value.__enter__.return_value = mock_conn

    auth = AuthManager()
    user_id = auth.get_user_id("unknown")

    assert user_id is None

@patch("game.auth.sqlite3.connect")
def test_create_score_table(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_conn

    auth = AuthManager()
    auth.create_score_table()

    mock_conn.execute.assert_called_once()
    assert "CREATE TABLE IF NOT EXISTS scores" in mock_conn.execute.call_args[0][0]

@patch("game.auth.sqlite3.connect")
def test_save_score(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_conn

    auth = AuthManager()
    auth.get_user_id = MagicMock(return_value=1)
    auth.save_score("testuser", 5, 100, True)

    mock_conn.execute.assert_called_once()
    args = mock_conn.execute.call_args[0]
    assert args[0].strip().startswith("INSERT INTO scores")
    assert args[1] == (1, 5, 100, True)

@patch("game.auth.sqlite3.connect")
def test_get_user_scores(mock_connect):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(5, 100, True, "2025-01-01")]
    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_cursor
    mock_connect.return_value.__enter__.return_value = mock_conn

    auth = AuthManager()
    auth.get_user_id = MagicMock(return_value=1)
    scores = auth.get_user_scores("testuser")

    assert len(scores) == 1
    assert scores[0][0] == 5



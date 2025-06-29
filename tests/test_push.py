import pandas as pd
import pyodbc
import pytest

from core.db.push import bulk_insert_dataframe


class DummyCursor:
    def __init__(self) -> None:
        self.fast_executemany = False
        self.executed_sql = None
        self.executed_params = None

    def executemany(self, sql, params):
        self.executed_sql = sql
        self.executed_params = params


class DummyConnection:
    def __init__(self) -> None:
        self.cursor_obj = DummyCursor()
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


def test_bulk_insert_dataframe(monkeypatch):
    dummy_conn = DummyConnection()
    
    def fake_connect(conn_str):
        assert conn_str == "CONN_STR"
        return dummy_conn

    monkeypatch.setattr(pyodbc, "connect", fake_connect)

    df = pd.DataFrame({"id": [1, 2], "value": ["a", "b"]})
    schema = {"id": int, "value": str}
    bulk_insert_dataframe("CONN_STR", "dbo.test", df, expected_schema=schema)

    assert dummy_conn.cursor_obj.fast_executemany is True
    expected_sql = "INSERT INTO dbo.test (id,value) VALUES (?,?)"
    assert dummy_conn.cursor_obj.executed_sql == expected_sql
    assert dummy_conn.cursor_obj.executed_params == [(1, "a"), (2, "b")]
    assert dummy_conn.committed is True


def test_bulk_insert_dataframe_schema_validation(monkeypatch):
    dummy_conn = DummyConnection()

    def fake_connect(conn_str):
        return dummy_conn

    monkeypatch.setattr(pyodbc, "connect", fake_connect)

    df = pd.DataFrame({"id": [1, 2], "value": ["a", 2]})
    schema = {"id": int, "value": str}
    with pytest.raises(ValueError):
        bulk_insert_dataframe("CONN_STR", "dbo.test", df, expected_schema=schema)


def test_bulk_insert_dataframe_schema_file(monkeypatch, tmp_path):
    dummy_conn = DummyConnection()

    def fake_connect(conn_str):
        return dummy_conn

    monkeypatch.setattr(pyodbc, "connect", fake_connect)

    schema_path = tmp_path / "schema.json"
    schema_path.write_text('{"id": "int", "value": "str"}')

    df = pd.DataFrame({"id": [1, 2], "value": ["a", "b"]})
    bulk_insert_dataframe("CONN_STR", "dbo.test", df, schema_file=str(schema_path))

    assert dummy_conn.cursor_obj.fast_executemany is True
    expected_sql = "INSERT INTO dbo.test (id,value) VALUES (?,?)"
    assert dummy_conn.cursor_obj.executed_sql == expected_sql
    assert dummy_conn.cursor_obj.executed_params == [(1, "a"), (2, "b")]
    assert dummy_conn.committed is True


def test_bulk_insert_dataframe_rename(monkeypatch):
    dummy_conn = DummyConnection()

    def fake_connect(conn_str):
        return dummy_conn

    monkeypatch.setattr(pyodbc, "connect", fake_connect)

    df = pd.DataFrame({"old_id": [1, 2], "old_value": ["a", "b"]})
    rename_map = {"old_id": "id", "old_value": "value"}
    schema = {"id": int, "value": str}

    bulk_insert_dataframe(
        "CONN_STR",
        "dbo.test",
        df,
        expected_schema=schema,
        rename_map=rename_map,
    )

    expected_sql = "INSERT INTO dbo.test (id,value) VALUES (?,?)"
    assert dummy_conn.cursor_obj.executed_sql == expected_sql
    assert dummy_conn.cursor_obj.executed_params == [(1, "a"), (2, "b")]


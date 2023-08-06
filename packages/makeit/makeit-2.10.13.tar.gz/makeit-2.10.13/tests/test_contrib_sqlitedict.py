import dataclasses

import pytest

from makeit import DataclassTask, Target, Dependency, execute_on_change
from makeit.contrib.sqlitedict import SqliteDict, SqliteArtifact


def test_simple(tmp_path):
    path_to_db = tmp_path / "db.db"

    # Close properly
    with SqliteDict(path_to_db) as storage:
        a1 = SqliteArtifact("a1", storage)
        a1_ = SqliteArtifact("a1_", storage)

        a1.data = 123
        a1_.data = 123

    # Close without committing:
    storage = SqliteDict(path_to_db)
    SqliteArtifact("a2", storage).data = 12
    storage.close()

    # Close with exception
    with pytest.raises(Exception):
        with SqliteDict(path_to_db) as storage:
            a3 = SqliteArtifact("a3", storage)
            a3.data = ("Hello", "world")

            raise Exception("Done")

    # Check results
    with SqliteDict(path_to_db) as storage:
        a1 = SqliteArtifact("a1", storage)
        a1_ = SqliteArtifact("a1_", storage)
        a2 = SqliteArtifact("a2", storage)
        a3 = SqliteArtifact("a3", storage)

        assert a1.data == 123
        assert not a2.exists()
        assert a3.data == ("Hello", "world")

        assert a1.fingerprint() != a3.fingerprint()
        assert a1.fingerprint() == a1_.fingerprint()


@dataclasses.dataclass
class Generate(DataclassTask):
    out: SqliteArtifact | Target

    execution_cnt = 0

    def execute(self):
        self.out.data = "Generated"
        self.__class__.execution_cnt += 1


@dataclasses.dataclass
class Consume(DataclassTask):
    in_: SqliteArtifact | Dependency
    out: SqliteArtifact | Target

    execution_cnt = 0

    def execute(self):
        self.out.data = self.in_.data.upper()

        self.__class__.execution_cnt += 1


def test_sqlite_with_execute(tmp_path):
    path_to_db = tmp_path / "db.db"
    backend = tmp_path / "makeit.json"

    with SqliteDict(path_to_db) as storage:
        task1 = Generate(out=storage.artifact("out_generate"))

        execute_on_change([task1], backend=backend)

    assert Generate.execution_cnt == 1

    with SqliteDict(path_to_db) as storage:
        task2 = Consume(in_=storage.artifact("out_generate"), out=storage.artifact("out_consume"))

        execute_on_change([task2], backend=backend)

    assert Consume.execution_cnt == 1

    assert SqliteDict(path_to_db).artifact("out_consume").data == "GENERATED"

    print(task2)

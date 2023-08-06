import datetime
import hashlib
from makeit.core import Artifact

import sqlitedict


class SqliteDict(sqlitedict.SqliteDict):
    """ IMPORTANT change: we always commit on __exit__ """

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()

        super(SqliteDict, self).__exit__(exc_type, exc_val, exc_tb)

    def artifact(self, name: str):
        return SqliteArtifact(name, self)


class SqliteArtifact(Artifact):
    """
    This artifact corresponds to the data stored in the sqlite-database.

    Typical usage:

    with SqliteDict("path/to/db") as storage:
        a1 = storage.artifact("a1")  # this a1 is bound to the storage and not valid outside the `with` block
    """
    def __init__(self, name: str, storage: sqlitedict.SqliteDict):
        self._storage = storage
        self._name = name

    def fingerprint(self) -> str | None:
        raw = self._raw_data

        if isinstance(raw, str):
            raw = raw.encode('utf-8')

        return hashlib.md5(raw).hexdigest()

    def exists(self) -> bool:
        return self._name in self._storage

    def modification_time(self) -> datetime.datetime:
        raise NotImplementedError()

    @property
    def data(self):
        return self._storage[self._name]

    @data.setter
    def data(self, val):
        self._storage[self._name] = val

    @property
    def _raw_data(self):
        # copy from sqlitedict
        GET_ITEM = 'SELECT value FROM "%s" WHERE key = ?' % self._storage.tablename
        item = self._storage.conn.select_one(GET_ITEM, (self._name,))

        if item is None:
            raise KeyError(self._name)

        return item[0]

    def label(self) -> str:
        return f"{self.__class__.__name__}({self._storage}/{self._name})"

    def drop(self):
        del self._storage[self._name]

    def __repr__(self):
        return self.label()

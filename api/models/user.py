from typing import Any, Optional, TYPE_CHECKING, TypeVar

from sqlalchemy.sql.schema import MetaData
from sqlalchemy.sql.sqltypes import String
from api.models.repo import Repo, BaseModel

from sqlalchemy import Table, BigInteger, Column
from sqlalchemy.orm import mapper
import functools
import inspect


def mapped_table(table: Table):

    isprop = lambda p: isinstance(p, property)

    C = TypeVar("C")

    def wrap_class(model_class: C) -> C:
        if not TYPE_CHECKING:
            mapper(model_class, table)
        return model_class

    return wrap_class


metadata = MetaData()


@mapped_table(
    Table(
        "user",
        metadata,
        Column("id", BigInteger, primary_key=True),
        Column("name", String(50)),
    )
)
class User(BaseModel):

    # ideally we own the base model here for type checking purposes;
    # I think we'd have to do non-declarative bases for that;
    # in which case all references to User.property here need to be
    # replaced with User.mapper.property somehow
    def __init__(self, name: Optional[str] = None, **kwargs):
        self.name = name

    # finally we have classmethod model-specific wrappers that do higher-level stuff.
    # parameterizing the repo here lets us model-specific helpers pass through our own
    # typed interface, and allows for other mocking patterns around the higher-level repo object.

    # query helpers
    @classmethod
    def get_one_by_name(cls, repo: Repo, name: str):
        repo.query(cls).filter_by(name=name).first()

    # writes should also go through this interface, ie
    def save(self, repo: Repo):
        repo.insert(self)

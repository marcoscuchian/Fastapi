
from sqlalchemy import Table, Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from config.db import engine
import uuid

from config.db import meta, engine

Base = declarative_base()

client = Table("client", meta,
    Column("id", String(255), primary_key=True, unique=True, default=lambda: str(uuid.uuid4())),
    Column("name", String(255))
)
account = Table("accounts", meta,
    Column("id",String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True),
    Column("id_client",String(255), ForeignKey("client.id")),
    Column("balance",Float)
    )

motion = Table("motions", meta,
    Column("id",String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True),
    Column("id_account",String(36), ForeignKey("accounts.id")),
    Column("type",String(255)),
    Column("amount",Float),
    Column("date",Date),
    )


category = Table("categorys", meta,
    Column("id", String(36), primary_key=True, unique=True, default=lambda: str(uuid.uuid4())),
    Column("name", String(255))
)

categoryclient = Table("categorys_clients", meta,
Column("id_category", String(36), ForeignKey("categorys.id", name="fk_category_id")),
    Column("id_client", String(255), ForeignKey("client.id", name="fk_client_id"))
)
meta.create_all(engine)

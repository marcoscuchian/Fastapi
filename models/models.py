
from sqlalchemy import Table, Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from config.db import engine
import uuid

from config.db import meta, engine

Base = declarative_base()

clientes = Table("clientes", meta,
    Column("id_cliente", String(255), primary_key=True, unique=True, default=lambda: str(uuid.uuid4())),
    Column("nombre", String(255))
)
cuenta = Table("cuentas", meta,
    Column("id_cuenta",String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True),
    Column("id_cliente",String(255), ForeignKey("clientes.id_cliente")),
    Column("saldo",Float)
    )

movimiento = Table("movimientos", meta,
    Column("id_movimiento",String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True),
    Column("id_cuenta",String(36), ForeignKey("cuentas.id_cuenta")),
    Column("tipo",String(255)),
    Column("importe",Float),
    Column("fecha",Date),
    )


categoria = Table("categorias", meta,
    Column("id_categoria", String(36), primary_key=True, unique=True, default=lambda: str(uuid.uuid4())),
    Column("nombre", String(255))
)

categoriaCliente = Table("categorias_clientes", meta,
Column("id_categoria", String(36), ForeignKey("categorias.id_categoria", name="fk_categoria_id")),
    Column("id_cliente", String(255), ForeignKey("clientes.id_cliente", name="fk_cliente_id"))
)
meta.create_all(engine)

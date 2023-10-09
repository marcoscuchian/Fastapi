from sqlalchemy import create_engine, MetaData

engine  = create_engine("mysql+pymysql://root:123456789@localhost:3306/clientes")
meta = MetaData()
conn = engine.connect()



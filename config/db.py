from sqlalchemy import create_engine, MetaData

user = "your_uses"
password = "password"

engine  = create_engine(f"mysql+pymysql://{user}:{password}@localhost:3306/challengeBanza")
meta = MetaData()
conn = engine.connect()



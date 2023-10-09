from sqlalchemy import create_engine, MetaData

user = "Your user here"
password = "your password"

engine  = create_engine(f"mysql+pymysql://{user}:{password}@localhost:3306/clientes")
meta = MetaData()
conn = engine.connect()



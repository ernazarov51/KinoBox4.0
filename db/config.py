from utils.config import CF as conf

DBT=conf
DB=conf.DBC

TG=conf.TG

engine=f"postgresql+psycopg2://{DB.USER}:{DB.PASSWORD}@{DB.HOST}:{DB.PORT}/{DB.DATABASE}"


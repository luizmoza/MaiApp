
from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime

class cl_Feriado(app.base):
    Data:Mapped[datetime.datetime] = mapped_column(primary_key=True)
    Nome:Mapped[str] = mapped_column(primary_key=True)
    Tipo:Mapped[str] = mapped_column(primary_key=True)
    __tablename__ = "Feriado"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    
    def __init__(self,**kwargs): 
        self.Data = kwargs['Data'] if 'Data' in kwargs else None
        self.Nome = kwargs['Nome'] if 'Nome' in kwargs else None
        self.Tipo = kwargs['Tipo'] if 'Tipo' in kwargs else None

    def __repr__(self): return str(self.__dict__)
    def bulk(self,db,df):
        vv = False
        try:
            df.to_sql(self.__tablename__, db.engine, if_exists='append', index=False)
            vv = True
            db.statusquery = 'Executed'
        except Exception as e:
            db.statusquery = 'Failed Query: %s', repr(e)
        return vv 


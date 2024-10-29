from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime

class cl_Carteira(app.base):
    IDCarteira:Mapped[int]= mapped_column(primary_key=True,unique=True)
    DrawdownDias:Mapped[int]
    CGC:Mapped[str] 
    Data:Mapped[datetime.datetime]
    Bench:Mapped[str] 
    CotaLiberada:Mapped[bool]
    Batida:Mapped[bool]
    Liberado:Mapped[bool]
    PL:Mapped[float]
    Cota:Mapped[float]
    Var:Mapped[float]
    StressAlta:Mapped[float]
    StressBaixa:Mapped[float]
    Drawdown:Mapped[float]
    VolBench:Mapped[float]
    ColchaoLiq:Mapped[float]
    Top2Passivo:Mapped[float]
    Stress5:Mapped[float]
    Stress6:Mapped[float]
    Stress7:Mapped[float]
    Stress8:Mapped[float]
    Stress9:Mapped[float]
    Stress10:Mapped[float]
    Stress11:Mapped[float]
    Stress12:Mapped[float]
    Stress13:Mapped[float]
    Stress14:Mapped[float]
    Stress15:Mapped[float]
    Stress16:Mapped[float]
    VaR975:Mapped[float]
    VaR95:Mapped[float]
    Stress1:Mapped[float]
    Stress2:Mapped[float]
    Stress3:Mapped[float]
    Stress4:Mapped[float]
    CotaBruta:Mapped[float]
    __tablename__ = "Carteira"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    __pk__ = ['IDCarteira']
    __nn__ = ['CGC']
    __nnbl__ = ['Batida']
    __nnint__ = []
    __nndbl__ = []
    __nndt__ = ['Data']
    __unics__ = [] 
    __fks__ = {} 

    
    def __init__(self,**kwargs):
        self.IDCarteira = kwargs['IDCarteira'] if 'IDCarteira' in kwargs else None
        self.DrawdownDias = kwargs['DrawdownDias'] if 'DrawdownDias' in kwargs else None
        self.CGC = kwargs['CGC'] if 'CGC' in kwargs else None
        self.Data = kwargs['Data'] if 'Data' in kwargs else None
        self.Bench = kwargs['Bench'] if 'Bench' in kwargs else None
        self.CotaLiberada = kwargs['CotaLiberada'] if 'CotaLiberada' in kwargs else None
        self.Batida = kwargs['Batida'] if 'Batida' in kwargs else None
        self.Liberado = kwargs['Liberado'] if 'Liberado' in kwargs else None
        self.PL = kwargs['PL'] if 'PL' in kwargs else None
        self.Cota = kwargs['Cota'] if 'Cota' in kwargs else None
        self.Var = kwargs['Var'] if 'Var' in kwargs else None
        self.StressAlta = kwargs['StressAlta'] if 'StressAlta' in kwargs else None
        self.StressBaixa = kwargs['StressBaixa'] if 'StressBaixa' in kwargs else None
        self.Drawdown = kwargs['Drawdown'] if 'Drawdown' in kwargs else None
        self.VolBench = kwargs['VolBench'] if 'VolBench' in kwargs else None
        self.ColchaoLiq = kwargs['ColchaoLiq'] if 'ColchaoLiq' in kwargs else None
        self.Top2Passivo = kwargs['Top2Passivo'] if 'Top2Passivo' in kwargs else None
        self.Stress5 = kwargs['Stress5'] if 'Stress5' in kwargs else None
        self.Stress6 = kwargs['Stress6'] if 'Stress6' in kwargs else None
        self.Stress7 = kwargs['Stress7'] if 'Stress7' in kwargs else None
        self.Stress8 = kwargs['Stress8'] if 'Stress8' in kwargs else None
        self.Stress9 = kwargs['Stress9'] if 'Stress9' in kwargs else None
        self.Stress10 = kwargs['Stress10'] if 'Stress10' in kwargs else None
        self.Stress11 = kwargs['Stress11'] if 'Stress11' in kwargs else None
        self.Stress12 = kwargs['Stress12'] if 'Stress12' in kwargs else None
        self.Stress13 = kwargs['Stress13'] if 'Stress13' in kwargs else None
        self.Stress14 = kwargs['Stress14'] if 'Stress14' in kwargs else None
        self.Stress15 = kwargs['Stress15'] if 'Stress15' in kwargs else None
        self.Stress16 = kwargs['Stress16'] if 'Stress16' in kwargs else None
        self.VaR975 = kwargs['VaR975'] if 'VaR975' in kwargs else None
        self.VaR95 = kwargs['VaR95'] if 'VaR95' in kwargs else None
        self.Stress1 = kwargs['Stress1'] if 'Stress1' in kwargs else None
        self.Stress2 = kwargs['Stress2'] if 'Stress2' in kwargs else None
        self.Stress3 = kwargs['Stress3'] if 'Stress3' in kwargs else None
        self.Stress4 = kwargs['Stress4'] if 'Stress4' in kwargs else None
        self.CotaBruta = kwargs['CotaBruta'] if 'CotaBruta' in kwargs else None


 #################################################################################################################################################
 #################################################################Métodos Genéricos###############################################################
        
    def __repr__(self): return str(self.__dict__)
    
    def bulk(self,df):
        vv = False
        try:
            df.to_sql(self.__tablename__, self.__db__.engine, if_exists='append', index=False)
            vv = True
            self.__db__.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = f'Failed to query: {repr(e)}'
        return vv  

    def read(self, id):
        vv = True
        try:
            self.__db__.session.expire_all()
            record = self.__db__.session.get(self.__class__,id)
            self.__db__.statusquery = 'Executed'
            if record:
                for key, value in app.tk.ParseObjectDict(record).items():setattr(self, key, value)
            else:
                vv = False
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to query: {repr(e)}'
        return vv

    def get(self): # Usa os dados do próprio objeto
        vv = True
        id = getattr(self,self.__pk__[0])
        try:
            self.__db__.session.expire_all()
            record = self.__db__.session.get(self.__class__,id)
            self.__db__.statusquery = 'Executed'
            if record:
                for key, value in app.tk.ParseObjectDict(record).items():setattr(self, key, value)
            else:
                vv = False
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to query: {repr(e)}'
        return vv

    def create(self,data):
        vv = True
        try:
            newrecord = self.__class__(**data)
            newrecord.__db__.session.add(newrecord)
            newrecord.__db__.session.flush()
            id = getattr(newrecord,newrecord.__pk__[0])
            self.__db__.session.commit()
            setattr(self,self.__pk__[0],id)
            self.__db__.statusquery = 'Inserted successfully'
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to insert: {repr(e)}'
            if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def insert(self): # Usa os dados do próprio objeto
        vv = True
        try:
            self.__db__.session.add(self)
            self.__db__.session.flush()
            id = getattr(self,self.__pk__[0])
            self.__db__.session.commit()
            setattr(self,self.__pk__[0],id)
            self.__db__.statusquery = 'Inserted successfully'
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to insert: {repr(e)}'
            if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def update(self, id, updated_data):
        vv = True
        try:
            record = self.__db__.session.get(self.__class__,id)
            if record:
                for key, value in updated_data.items():setattr(record, key, value)
                self.__db__.session.commit()
                self.__db__.statusquery = 'Updated successfully'
            else:
                self.__db__.statusquery = 'Record not found'
                vv = False
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to update: {repr(e)}'
            if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def set(self): # Usa os dados do próprio objeto
        vv = True
        id = getattr(self,self.__pk__[0])
        data = app.tk.ParseObjectDict(self)
        try:
            record = self.__db__.session.get(self.__class__,id)
            if record:
                for key, value in data.items():setattr(record, key, value)
                self.__db__.session.commit()
                self.__db__.statusquery = 'Updated successfully'
            else:
                self.__db__.statusquery = 'Record not found'
                vv = False
        except Exception as e:
           vv = False
           self.__db__.statusquery = f'Failed to update: {repr(e)}'
           if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def delete(self, id):
        vv = True
        try:
            record = self.__db__.session.get(self.__class__,id)
            if record:
                self.__db__.session.delete(record)
                self.__db__.session.commit()
                self.__db__.statusquery = 'Deleted successfully'
            else:
                self.__db__.statusquery = 'Record not found'
                vv = False
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to delete: {repr(e)}'
            if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def remove(self): # Usa os dados do próprio objeto
        vv = True
        id = getattr(self,self.__pk__[0])
        try:
            record = self.__db__.session.get(self.__class__,id)
            if record:
                self.__db__.session.delete(record)
                self.__db__.session.commit()
                self.__db__.statusquery = 'Deleted successfully'
            else:
                self.__db__.statusquery = 'Record not found'
                vv = False
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to delete: {repr(e)}'
            if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def get_sample_fk(self):
        vv = True
        for k,v in self.__fks__.items():
            try:
                myQuery = """
                select top(1) """ + v + """ from """ + k + """
                """
                dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
                if len(dfresult)>0:
                    setattr(self,v,dfresult[v].iloc[0].item()) 
                    self.__db__.statusquery = 'Executed'
                else:
                    vv = False
                    self.__db__.statusquery = 'Table is empty'
            except Exception as e:
                vv = False  
                self.__db__.statusquery = 'Failed Query: %s', repr(e)
            return vv
        
#################################################################Métodos Génericos#############################################################
###############################################################################################################################################


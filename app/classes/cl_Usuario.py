from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
#

class cl_Usuario(app.base):
    __table_args__ = {'extend_existing': True}
    idUsuario:Mapped[int] = mapped_column(primary_key=True,unique=True)
    Nome:Mapped[str]
    WA:Mapped[str]
    UtilizaWa:Mapped[bool]
    Senha:Mapped[str]
    Email:Mapped[str]
    ChaveTrocaSenha:Mapped[str]
    __tablename__ = "Usuario"
    __db__ = app.db
    __pk__ = ['idUsuario']
    __nn__ = ['Nome','Email','Senha']
    __nnbl__ = []
    __nnint__ = []
    __nndbl__ = []
    __nndt__ = []
    __unics__ = []
    __fks__ = {} 


    def __init__(self,**kwargs):
        self.idUsuario = kwargs['idUsuario'] if 'idUsuario' in kwargs else None
        self.Nome = kwargs['Nome'] if 'Nome' in kwargs else None
        self.WA = kwargs['WA'] if 'WA' in kwargs else None
        self.UtilizaWa = kwargs['UtilizaWa'] if 'UtilizaWa' in kwargs else None
        self.Senha = kwargs['Senha'] if 'Senha' in kwargs else None
        self.Email = kwargs['Email'] if 'Email' in kwargs else None
        self.ChaveTrocaSenha = kwargs['ChaveTrocaSenha'] if 'ChaveTrocaSenha' in kwargs else None
 
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


    def load_by_Email(self,email):
        vv = True
        try:
            if self.get_id_by_email(email):
                record = self.__db__.session.get(cl_Usuario,self.idUsuario)
                data = app.tk.ParseObjectDict(record)
                for key, value in data.items():setattr(self, key, value)
                self.__db__.statusquery = 'Executed'
            else:
                vv = False
                self.__db__.statusquery = 'Not Executed'
        except Exception as e:
            self.__db__.statusquery = f'Failed to query: {repr(e)}'
            vv = False
        return vv              
   
    def get_id_by_email(self,email):
        vv = False
        try:
            myQuery = """
            select idUsuario from """ + self.__tablename__ + """
            where Email = '""" + email + """'
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                self.idUsuario = dfresult['idUsuario'].iloc[0].item()
                vv = True
            else:
                self.idUsuario = 0
            self.__db__.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = f'Failed to query: {repr(e)}'
            vv = False  
        return vv

    def get_id_by_auth(self,auth):
        vv = False
        try:
            myQuery = """
            select idUsuario from """ + self.__tablename__ + """
            where ChaveTrocaSenha = '""" + auth + """'
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                self.idUsuario = dfresult['idUsuario'].iloc[0].item()
                vv = True
            else:
                self.idUsuario = 0
            self.__db__.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = f'Failed to query: {repr(e)}'
            vv = False  
        return vv
    
    def Auth_napi(self,session):
            vv = True
            if 'Usuario_Email' not in session : vv = False 
            if 'Usuario_Id' not in session : vv = False
            if 'Usuario_Auth' not in session : vv = False
            if session['Usuario_Email'] == '' : vv = False       
            if session['Usuario_Id'] == '' : vv = False       
            if session['Usuario_Auth'] == '' : vv = False
            try:
                record = self.__db__.session.get(cl_Usuario,session['Usuario_Id']) 
                data = app.tk.ParseObjectDict(record)
                for key, value in data.items():setattr(self, key, value)
                if self.ChaveTrocaSenha != session['Usuario_Auth']:vv = False
                self.__db__.statusquery = 'Executed'
            except Exception as e:
                vv = False
                self.__db__.statusquery = f'Failed to query: {repr(e)}'
            return vv 

    def Auth_api(self,request):
            vv = True
            if 'idUsuario' not in request.form: vv = False
            if 'UsuarioAuth' not in request.form: vv = False
            try:
                self.idUsuario = request.form['idUsuario']
                record = self.__db__.session.get(cl_Usuario,self.idUsuario)
                data = app.tk.ParseObjectDict(record)
                for key, value in data.items():setattr(self, key, value)
                if self.ChaveTrocaSenha != app.request.form['UsuarioAuth']: 
                    vv = False
                    self.__db__.statusquery = 'Executed'
            except Exception as e:
                vv = False
                self.__db__.statusquery = f'Failed to query: {repr(e)}'
            return vv 

    def Auth_recover(self,session,auth):
            vv = True
            if self.get_id_by_auth(auth):
                try:
                    record = self.__db__.session.get(cl_Usuario,self.idUsuario)
                    record.ChaveTrocaSenha = app.tk.generate_guid()
                    self.__db__.session.commit()
                    session['Usuario_Email'] = record.Email
                    session['Usuario_Id'] = record.idUsuario
                    session['Usuario_Auth'] = record.ChaveTrocaSenha 
                    data = app.tk.ParseObjectDict(record)
                    for key, value in data.items():setattr(self, key, value)
                    self.__db__.statusquery = 'Executed'
                except Exception as e:
                    self.__db__.statusquery = f'Failed to query: {repr(e)}'
                    vv = False
            else:
                    vv = False
                    self.__db__.statusquery = 'Failed'
            return vv 

    def Auth_login(self,session,idusuario,senha):
            vv = True
            try:
                record = self.__db__.session.get(cl_Usuario,idusuario)
                if record.Senha == senha:
                    record.ChaveTrocaSenha = app.tk.generate_guid()
                    self.__db__.session.commit()
                    session['Usuario_Email'] = record.Email
                    session['Usuario_Id'] = record.idUsuario
                    session['Usuario_Auth'] = record.ChaveTrocaSenha
                    record = self.__db__.session.get(cl_Usuario,idusuario)
                    data = app.tk.ParseObjectDict(record)
                    for key, value in data.items():setattr(self, key, value)
                    self.__db__.statusquery = 'Executed'
                else:
                    vv = False
                    self.__db__.statusquery = 'Failed'
            except Exception as e:
                    vv = False
                    self.__db__.statusquery = f'Failed to query: {repr(e)}'
            return vv 
    
    def Reset_pwd(self,session,request):
            vv = True
            try:
                if self.get_id_by_email(request.form['Email']):
                    record = self.__db__.session.get(cl_Usuario,self.idUsuario)
                    data = app.tk.ParseObjectDict(record)
                    for key, value in data.items():setattr(self, key, value)
                    self.ChaveTrocaSenha = app.tk.generate_guid()
                    self.__db__.session.commit()
                    session['Usuario_Email'] = self.Email
                    session['Usuario_Id'] = self.idUsuario
                    session['Usuario_Auth'] = self.ChaveTrocaSenha
                    self.__db__.statusquery = 'Executed Reset pwd'
                if app.tkEmail.EnviaEmailRecover(self.Email,'Usuario/Cadastro?' + self.ChaveTrocaSenha) == False: 
                    vv = False
                    self.__db__.statusquery = 'Failed to Send Email'
            except Exception as e:
                vv = False
                self.__db__.statusquery = f'Failed to Send Email: {repr(e)}'
            return vv 
                    
        
import warnings
warnings.filterwarnings("ignore")
from flask import Flask
import pandas as pd
import copy as copy
import numpy as np
import os as os
import xml.etree.ElementTree as ET
import json as json
import codecs as codecs
import pathlib as pathlib
import urllib as urllib
import sqlalchemy as sa
import win32com.client as win32
from datetime import datetime as dt
from datetime import timedelta
from flask import request as request
from flask import session as session
from flask import Markup as Markup
import sys as sys
from sqlalchemy.orm import declarative_base as declarative_base

class FFlask(Flask):
    def __init__(self,__name__):
        Flask.__init__(self,__name__)
        self.enviroment = 'prd'
        self.path = os.getcwd()
        self.sep = r"\ ".replace(" ","")
        self.sept = r"/ ".replace(" ","")
        self.secret_key = "32165498798654654654"
        self.test_idUsuario = 1
        self.db = ''
        self.server = ''
        self.database = ''
        self.params = ''
        self.usr = ''
        self.pwd = ''
        self.base = ''
        self.engine = ''
        self.server = ''
        self.os = os    
        self.pd = pd    
        self.ET = ET    
        self.json = json    
        self.codecs = codecs    
        self.pathlib = pathlib 
        self.urllib = urllib   
        self.np = np    
        self.sa = sa    
        self.win32 = win32    
        self.tk = ''
        self.tkdtm = ''  
        self.tkEmail =''
        self.tkDict =''
        self.tkfm = ''
        self.tkstr = ''
        self.request = request
        self.session = session
        self.Markup = Markup
        self.dt = dt
        self.copy = copy
        self.timedelta = timedelta
        self.sys = sys
        self.defaultfotopath = r'../static/images/UserProfile/default.jpg'
        self.fotopath = r'../static/images/UserProfile/Profile'
        self.headerpath = r'\app\templates\Header.html'
        self.sidebarpath = r'\app\templates\SideBar.html'
        self.dtstr = '%Y-%m-%d'

app = FFlask(__name__)

#######################################################################################################################################
################################################### Moc Banco de Dados ################################################################

if app.enviroment == 'prd':
    app.server = r'10.245.243.5'
    app.database = 'MAI'
    app.usr = 'usr_appMai'
    app.pwd = '9962v3DrlKo0h6qR157ssetDGA'
    app.params = urllib.parse.quote_plus(r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + app.server + ";DATABASE=" + app.database + ";UID=" + app.usr + ";PWD=" + app.pwd + "")
    app.test_idUsuario = 1

elif app.enviroment == 'local':
    app.server = r'MOZA\SQLEXPRESS'
    app.database = 'MAI'
    app.usr = ''
    app.pwd = ''
    app.params = urllib.parse.quote_plus(r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + app.server + ";DATABASE=" + app.database + ";Trusted_Connection=yes;")
    app.test_idUsuario = 1

elif app.enviroment == 'local_surface':
    app.server = r'SURFACEMOZA\MAIAPP'
    app.database = 'MAI'
    app.usr = 'sa'
    app.pwd = '159951'
    app.params = urllib.parse.quote_plus(r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + app.server + ";DATABASE=" + app.database + ";UID=" + app.usr + ";PWD=" + app.pwd + "")
    app.test_idUsuario = 1

elif app.enviroment == 'hml':
    app.server = r'MAGDB04SQLVMHMG,4030'
    app.database = 'MAI'
    app.usr = ''
    app.pwd = ''
    app.params = urllib.parse.quote_plus(r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + app.server + ";DATABASE=" + app.database + ";Trusted_Connection=yes;")
    app.test_idUsuario = 1

elif app.enviroment == 'dsv':
    app.server = r'MAGDB04SQLVMDEV,4030'
    app.database = 'MAI'
    app.usr = ''
    app.pwd = ''
    app.params = urllib.parse.quote_plus(r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + app.server + ";DATABASE=" + app.database + ";Trusted_Connection=yes;")
    app.test_idUsuario = 1

else:
    app.server = r'MAGDB04SQLVMHMG,4030'
    app.database = 'MAI'
    app.usr = ''
    app.pwd = ''
    app.params = urllib.parse.quote_plus(r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=" + app.server + ";DATABASE=" + app.database + ";Trusted_Connection=yes;")
    app.test_idUsuario = 1
    
################################################### Moc Banco de Dados ################################################################
#######################################################################################################################################

app.engine = sa.create_engine(r"mssql+pyodbc:///?odbc_connect={}".format(app.params))   
app.base = declarative_base()
app.base.metadata.create_all(app.engine)

#######################################################################################################################################
####################################################### Iniciando  ####################################################################

from app.util.util_file_management import util_file_management as tkfm
from app.util.util_string import util_string as tkstr
from app.classes.cl_db import cl_db
from app.classes.cl_tk import cl_tk
from app.classes.cl_tkEmail import cl_tkEmail
from app.classes.cl_tkDict import cl_tkDict
from app.classes.cl_tkDatetime import cl_tkDatetime
app.tkfm = tkfm
app.tkstr = tkstr
app.db = cl_db()
app.tkEmail = cl_tkEmail()
app.tkDict = cl_tkDict()
app.tkdtm = cl_tkDatetime()
app.tk = cl_tk()
app.db.Session_Start()
print("Current Directory", app.path)
from app.controllers import Default
from app.controllers import Dashboard
from app.controllers import Usuario
from app.controllers import Recover
from app.controllers import Cadastro_CodRefCotistaFundo
from app.controllers import Cadastro_Corretora
from app.controllers import Cadastro_Cotista
from app.controllers import Cadastro_Distribuidor
from app.controllers import Cadastro_Emissor
from app.controllers import Cadastro_Estrategia
from app.controllers import Cadastro_Fundo
from app.controllers import Cadastro_Futuro
from app.controllers import Cadastro_Opcao
from app.controllers import Cadastro_Operacao
from app.controllers import Cadastro_Renda_Fixa
from app.controllers import Cadastro_Renda_Variavel
from app.controllers import Boletador_Passivo
from app.controllers import Boletador_Ativo

####################################################### Iniciando  ####################################################################
#######################################################################################################################################

from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Mov import cl_Mov
from app.classes.cl_Fundo import cl_Fundo
from app.classes.cl_CodRefCotistaFundo import cl_CodRefCotistaFundo
from flask import render_template as render_template
from flask import Markup as Markup
import json ##

@app.route("/Boletador/Ativo")
def BoletadorAtivo():

    Usuario = cl_Usuario(**{}) 
    if Usuario.Auth_napi(app.session) == False : render_template('Login.html')
    
    fotopath = app.defaultfotopath
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    if app.tkDict.LoadDictIDContraparte(''):
        if app.tkDict.LoadDictEstratFull(''):
            if app.tkDict.LoadDictMacroEstrat(''):
                if app.tkDict.LoadDictTraderID(''):
                    if app.tkDict.LoadDictRateio():
                        if app.tkDict.LoadDictListRateio():
                            if app.tkDict.LoadDictCGCFundoid(app.tkdtm.hoje):
                                if app.tkDict.LoadDictEstratID(''):
                                    if app.tkDict.LoadDictMacroEstratID(''):
                                        if app.tkDict.LoadDictCGCFundoidCGC(app.tkdtm.hoje):
                                            jsonData = {
                                                        'DictRateio': app.tkDict.DictRateio,
                                                        'DictListRateio': app.tkDict.DictListRateio,
                                                        'DictContraparte': app.tkDict.DictIDContraparte,
                                                        'DictEstrategias': app.tkDict.DictEstratFull,
                                                        'DictMacroEstrat': app.tkDict.DictMacroEstrat,
                                                        'DictMacroEstratID': app.tkDict.DictMacroEstratID,
                                                        'DictEstratID': app.tkDict.DictEstratID,
                                                        'DictTrader': app.tkDict.DictTrader,
                                                        'DictCGCFundoidCGC':app.tkDict.DictCGCFundoidCGC,
                                                        'DictCGCFundoid': app.tkDict.DictCGCFundoid
                                                        }
    return render_template('BoletadorAtivo.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           hoje = app.tkdtm.hoje.strftime('%Y-%m-%d'),
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Boletador/Ativo/Upsert",methods = ['POST'])
def BoletadorAtivoUpdate():
    if app.request.method == 'POST':
        try:
            
            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')

 
            Mov = cl_Mov(**{})


            if app.request.form['IDMov']!='-1':
                Mov.IDMov = app.request.form['IDMov']
                if not Mov.get(): 
                    return app.json.dumps({"resposta" : "Erro ao Gravar Ativo"}, ensure_ascii=False).encode('utf-8', 'ignore')



            Mov.idTrader = int(app.request.form['idTrader'])
            Mov.idCorretora = int(app.request.form['idCorretora'])
            Mov.idEstrategia = int(app.request.form['idEstrategia'])
            Mov.DataMov = app.request.form['DataMov']
            Mov.CGC = app.request.form['CGC']
            Mov.AliasAtivo = app.request.form['AliasAtivo']
            Mov.Qtd = (app.request.form['Qtd'])
            Mov.Pu = (app.request.form['Pu'])
            Mov.Taxa = (app.request.form['Taxa'])
            Mov.Corretagem = (app.request.form['Corretagem'])
            Mov.TipoCompromisso = app.request.form['TipoCompromisso']
            Mov.DataCompromisso = app.request.form['DataCompromisso']
            Mov.PuCompromisso = app.tkstr.brl_float_string_to_db(app.request.form['PuCompromisso'])
            Mov.Marcacao = app.request.form['Marcacao']
            Mov.UltimoAlterador = Usuario.Nome
            Mov.DataLog = app.tkdtm.hoje




            if app.request.form['IDMov']=='-1': 
                Mov.insert()
            else:
                Mov.set()

            return app.json.dumps({"resposta" : "Ativo Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')


@app.route("/Boletador/Ativo/Delete",methods = ['POST'])
def BoletadorAtivoDelete():
    if app.request.method == 'POST':
        try:
            
            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')
            
            Mov = cl_Mov(**{})
            Mov.IDMov = app.request.form['IDMov']
            if not Mov.get(): return app.json.dumps({"resposta" : "Erro Ao deletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
            Mov.remove()
            return app.json.dumps({"resposta" : "Deletado Com Sucesso!"}, ensure_ascii=False).encode('utf-8', 'ignore')
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao deletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Boletador/Ativo/Search",methods = ['POST'])
def BoletadorAtivoSeach():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictMov(app.request.form['Search'],app.request.form['DataIni'],app.request.form['DataFim'],app.request.form['idEstrategia'],app.request.form['idTrader'],Pag,nPerPag,app.request.form['CGC']):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictMov}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Boletador/Ativo/Load",methods = ['POST'])
def BoletadorAtivoLoad():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
                Mov = cl_Mov(**{})
                Mov.IDMov = app.request.form['IDMov']
                if not Mov.get(): return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: "}, ensure_ascii=False).encode('utf-8', 'ignore')
                
                return app.json.dumps({"resposta" : "Ok","Dados": Mov.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
            
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   

@app.route("/Boletador/Ativo/CarregaTiposAtivoPorGrupo",methods = ['POST'])
def BoletadorAtivoCarregaTiposAtivoPorGrupo():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')

                Mov = cl_Mov(**{}) 
                df = Mov.LoadListaAtivos(app.request)
                
                if len(df)>0:
                    return app.json.dumps({"resposta" : "Ok","Dados": df.to_dict('records') }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro na coleta da lista!"}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
            
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')     



@app.route("/Boletador/Ativo/DadosBuscarAtivo",methods = ['POST'])
def BoletadorAtivoDadosBuscarAtivo():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')

                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictBuscarAtivos(app.request.form['Search'],Pag,nPerPag,app.request.form['Grupo'],app.request.form['Tipo']):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictBuscarAtivos}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    



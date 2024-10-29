from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Passivo import cl_Passivo
from app.classes.cl_Cotista import cl_Cotista
from app.classes.cl_Fundo import cl_Fundo
from app.classes.cl_CodRefCotistaFundo import cl_CodRefCotistaFundo
from flask import render_template as render_template
from flask import Markup as Markup
import json

@app.route("/Boletador/Passivo")
def BoletadorPassivo():
    Usuario = cl_Usuario(**{}) 
    if Usuario.Auth_napi(app.session) == False : render_template('Login.html')
    fotopath = app.defaultfotopath
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    if app.tkDict.LoadDictIDFundoWithInterno(app.tkdtm.hoje):jsonData = {'ListaFundoInterno': app.tkDict.DictIDFundoWithInterno}
    return render_template('BoletadorPassivo.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           hoje = app.tkdtm.hoje.strftime('%Y-%m-%d'),
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
@app.route("/Boletador/Passivo/Insert",methods = ['POST'])
def BoletadorPassivoInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Passivo = cl_Passivo(**{})
            Fundo = cl_Fundo(**{})
            CodRefCotistaFundo = cl_CodRefCotistaFundo(**{})
            
            
            if Fundo.read(app.request.form['idFundo']):

                if CodRefCotistaFundo.read(app.request.form['idCodRefCotistaFundo']):


                    Passivo.idCodRefCotistaFundo = CodRefCotistaFundo.IDCodRefCotistaFundo
                    Passivo.idFundo = Fundo.IDFundo
                    Passivo.Tipo = app.request.form['Tipo']
                    Passivo.QtdCotas = app.tkstr.brl_float_string_to_db(app.request.form['QtdCotas'])
                    Passivo.Fin = app.tkstr.brl_float_string_to_db(app.request.form['Fin'])
                    Passivo.DataMovimentacao = app.request.form['DataMovimentacao']
                    Passivo.Criador = Usuario.Nome
                    if 'Aprovador' in app.request.form: Passivo.Aprovador = app.request.form['Aprovador']
                    
                    Passivo.DataLog = app.tkdtm.hoje
                else:
                    return app.json.dumps({"resposta" : "Erro ao gravar Passivo"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao gravar Passivo"}, ensure_ascii=False).encode('utf-8', 'ignore')

            if Passivo.insert(): 
                return app.json.dumps({"resposta" : "Passivo Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao gravar Passivo"}, ensure_ascii=False).encode('utf-8', 'ignore')
            
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Boletador/Passivo/Delete",methods = ['POST'])
def BoletadorPassivoDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Passivo = cl_Passivo(**{})
            if Passivo.read(app.request.form['IDPassivo']):
                Passivo.remove()
                return app.json.dumps({"resposta" : "Deletado Com Sucesso!"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro deletando!"}, ensure_ascii=False).encode('utf-8', 'ignore')

        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao deletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Boletador/Passivo/Search",methods = ['POST'])
def BoletadorPassivoSearch():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictPassivo(app.request.form['Search'],app.request.form['DataIni'],app.request.form['DataFim'],Pag,nPerPag,app.request.form['Tipo']):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictPassivo}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    


@app.route("/Boletador/Passivo/LoadCodigosCotista",methods = ['POST'])
def BoletadorPassivoLoadCodigosCotista():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                if app.tkDict.LoaddfListaPassivo(app.request.form['idFundo']):
                     dflist =  app.tkDict.dfListaPassivo[['Codigo','idCodRefCotistaFundo']].drop_duplicates(subset=['idCodRefCotistaFundo'], keep='last')
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.dfListaPassivo.to_dict('records'),"Lista":dflist.to_dict('records')}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    


@app.route("/Boletador/Passivo/Load",methods = ['POST'])
def BoletadorPassivoLoad():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Passivo = cl_Passivo(**{})
                if Passivo.read(app.request.form['IDPassivo']):
                    return app.json.dumps({"resposta" : "Ok","Dados": Passivo.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados" }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
            
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')     

@app.route("/Boletador/Passivo/AlteraContaCotista",methods = ['POST'])
def BoletadorAlteraContaCotista():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Cotista = cl_Cotista(**{})
                if Cotista.read(app.request.form['idCotista']):
                    Cotista.Banco = app.request.form['Banco']
                    Cotista.Conta = app.request.form['Conta']
                    Cotista.Digito = app.request.form['Agencia']
                    Cotista.set()
                    return app.json.dumps({"resposta" : "Ok"}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao gravar!"}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
            
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')               

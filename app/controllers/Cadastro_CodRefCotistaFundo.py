from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_CodRefCotistaFundo import cl_CodRefCotistaFundo
from app.classes.cl_Cotista import cl_Cotista

from flask import render_template as render_template
from flask import Markup as Markup

@app.route("/Cadastro/CodRefCotistaFundo")
def CadastroCodRefCotistaFundo():
    Usuario = cl_Usuario(**{}) 
    if Usuario.Auth_napi(app.session) == False : render_template('Login.html')
    fotopath = app.defaultfotopath
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    if app.tkDict.LoadDictDistribuidorSimples(""):
        if app.tkDict.LoadDictFundosDaCasa(app.tkdtm.hoje):
            jsonData = {
                        'ListaDistribuidorSimples':app.tkDict.DictDistribuidorSimples,
                        'ListaFundosDaCasa': app.tkDict.DictFundosDaCasa,
                        }
    return render_template('CadastroCodRefCotistaFundo.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/CodRefCotistaFundo/Update",methods = ['POST'])
def CadastroCodRefCotistaFundoUpdate():

    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                

            if app.request.form['Codigo'] == "": return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: É obrigatório preencher um código"}, ensure_ascii=False).encode('utf-8', 'ignore')
 
            CodRefCotistaFundo = cl_CodRefCotistaFundo(**{})
            
            
            if CodRefCotistaFundo.read(app.request.form['IDCodRefCotistaFundo']):
                
                                
                CodRefCotistaFundo.idCotista = app.request.form['idCotista']
                CodRefCotistaFundo.idFundo = app.request.form['idFundo']
                CodRefCotistaFundo.Codigo = app.request.form['Codigo']
                CodRefCotistaFundo.Administrador = app.request.form['Administrador']
                CodRefCotistaFundo.idDistribuidor = app.request.form['idDistribuidor']

                CodRefCotistaFundo.Tipo = app.request.form['Tipo']
                CodRefCotistaFundo.Criador = Usuario.Nome
                CodRefCotistaFundo.DataLog = app.tkdtm.hoje

                if CodRefCotistaFundo.set():
                    return app.json.dumps({"resposta" : "CodRefCotistaFundo Gravada com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    print(str(CodRefCotistaFundo.__db__.statusquery))
                    return app.json.dumps({"resposta" : "Erro ao Gravar"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Gravar"}, ensure_ascii=False).encode('utf-8', 'ignore')
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/CodRefCotistaFundo/Insert",methods = ['POST'])
def CadastroCodRefCotistaFundoInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
 
            if app.request.form['Codigo'] == "": return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: É obrigatório preencher um código"}, ensure_ascii=False).encode('utf-8', 'ignore')
            
            CodRefCotistaFundo = cl_CodRefCotistaFundo(**{})
            CodRefCotistaFundo.idCotista = app.request.form['idCotista']
            CodRefCotistaFundo.idFundo = app.request.form['idFundo']
            CodRefCotistaFundo.Codigo = app.request.form['Codigo']
            CodRefCotistaFundo.Administrador = app.request.form['Administrador']
            CodRefCotistaFundo.idDistribuidor = app.request.form['idDistribuidor']
            CodRefCotistaFundo.Tipo = app.request.form['Tipo']
            CodRefCotistaFundo.Criador = Usuario.Nome
            CodRefCotistaFundo.DataLog = app.tkdtm.hoje
            
            
            if CodRefCotistaFundo.insert():
                return app.json.dumps({"resposta" : "CodRefCotistaFundo Gravada com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Gravar"}, ensure_ascii=False).encode('utf-8', 'ignore')
            
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/CodRefCotistaFundo/Delete",methods = ['POST'])
def CadastroCodRefCotistaFundoDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            CodRefCotistaFundo = cl_CodRefCotistaFundo(**{})
            if CodRefCotistaFundo.read(app.request.form['IDCodRefCotistaFundo']):
                if CodRefCotistaFundo.remove():
                    return app.json.dumps({"resposta" : "Deletado Com Sucesso!"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao Deletar!"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                    return app.json.dumps({"resposta" : "Erro ao Deletar!"}, ensure_ascii=False).encode('utf-8', 'ignore')

        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao deletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/CodRefCotistaFundo/Search",methods = ['POST'])
def CadastroCodRefCotistaFundoSeach():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictCodRefCotistaFundo(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictCodRefCotistaFundo}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/CodRefCotistaFundo/Load",methods = ['POST'])
def CadastroCodRefCotistaFundoLoad():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                CodRefCotistaFundo = cl_CodRefCotistaFundo(**{})
                Cotista = cl_Cotista(**{})
 
                if CodRefCotistaFundo.read(app.request.form['IDCodRefCotistaFundo']):
                    if Cotista.read(CodRefCotistaFundo.idCotista):
                        CodRefCotistaFundo.NomeCotista = Cotista.Nome
                        return app.json.dumps({"resposta" : "Ok","Dados": CodRefCotistaFundo.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                    else:
                        return app.json.dumps({"resposta" : "Erro ao coletar dados do cotista"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                else:
                    return app.json.dumps({"resposta" : "Erro ao coletar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')                   

            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   


                
@app.route("/Cadastro/CodRefCotistaFundo/CarregaListaCotistasByCGC",methods = ['POST'])
def CadastroCodRefCotistaFundoCarregaListaCotistasByCGC():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                

                if app.tkDict.LoadDictCotistaByCGC(app.request.form['CGC']):
                        return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictCotistaByCGC}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Nenhum cotista foi encontrado"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

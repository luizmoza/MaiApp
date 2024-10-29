from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Cotista import cl_Cotista
from flask import render_template as render_template
from flask import Markup as Markup

@app.route("/Cadastro/Cotista")
def CadastroCotista():
    Usuario = cl_Usuario(**{}) 
    if Usuario.Auth_napi(app.session) == False : render_template('Login.html')
    fotopath = app.defaultfotopath
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    return render_template('CadastroCotista.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/Cotista/Update",methods = ['POST'])
def CadastroCotistaUpdate():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
 
            Cotista = cl_Cotista(**{})
            if Cotista.read(app.request.form['IDCotista']):
                Cotista.Nome = app.request.form['Nome']
                Cotista.CGC = app.request.form['CGC']
                Cotista.Tipo = app.request.form['Tipo']
                if Cotista.set():
                    return app.json.dumps({"resposta" : "Cotista Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao gravar"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao gravar"}, ensure_ascii=False).encode('utf-8', 'ignore')
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Cotista/Insert",methods = ['POST'])
def CadastroCotistaInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                

            Cotista = cl_Cotista(**{})
            Cotista.Nome = app.request.form['Nome']
            Cotista.CGC = app.request.form['CGC']
            Cotista.Tipo = app.request.form['Tipo']

            if Cotista.insert():
                return app.json.dumps({"resposta" : "Cotista Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao inserir"}, ensure_ascii=False).encode('utf-8', 'ignore')
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Cotista/Delete",methods = ['POST'])
def CadastroCotistaDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Cotista = cl_Cotista(**{})
            if Cotista.read(app.request.form['IDCotista']):
                if Cotista.remove():
                    return app.json.dumps({"resposta" : "Deletado Com Sucesso!"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao deletar"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao deletar"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao deletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Cotista/Search",methods = ['POST'])
def CadastroCotistaSeach():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictCotista(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictCotista}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/Cotista/Load",methods = ['POST'])
def CadastroCotistaLoad():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Cotista = cl_Cotista(**{})
                if Cotista.read(app.request.form['IDCotista']):
                    return app.json.dumps({"resposta" : "Ok","Dados": Cotista.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao carregar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                

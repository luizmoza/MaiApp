from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Corretora import cl_Corretora
from flask import render_template as render_template
from flask import Markup as Markup

@app.route("/Cadastro/Corretora")
def CadastroCorretora():
    Usuario = cl_Usuario(**{}) 
    if Usuario.Auth_napi(app.session) == False : render_template('Login.html')
    fotopath = app.defaultfotopath
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    return render_template('CadastroCorretora.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/Corretora/Update",methods = ['POST'])
def CadastroCorretoraUpdate():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
 
            Corretora = cl_Corretora(**{})
            if Corretora.read(app.request.form['IDCorretora']):
                Corretora.CNPJ = app.request.form['CNPJ']
                Corretora.Nome = app.request.form['Nome']
                Corretora.AliasMellon = app.request.form['AliasMellon']
                Corretora.AliasBradesco = app.request.form['AliasBradesco']
                Corretora.AliasItau = app.request.form['AliasItau']
                if Corretora.set():
                    return app.json.dumps({"resposta" : "Corretora Gravada com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao Gravar"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Gravar"}, ensure_ascii=False).encode('utf-8', 'ignore')
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Corretora/Insert",methods = ['POST'])
def CadastroCorretoraInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Corretora = cl_Corretora(**{})
            Corretora.CNPJ = app.request.form['CNPJ']
            Corretora.Nome = app.request.form['Nome']
            Corretora.AliasMellon = app.request.form['AliasMellon']
            Corretora.AliasBradesco = app.request.form['AliasBradesco']
            Corretora.AliasItau = app.request.form['AliasItau']
            if Corretora.insert():
                return app.json.dumps({"resposta" : "Corretora Gravada com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')      
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')
    

@app.route("/Cadastro/Corretora/Delete",methods = ['POST'])
def CadastroCorretoraDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Corretora = cl_Corretora(**{})
            if Corretora.read(app.request.form['IDCorretora']):
                if Corretora.remove():
                    return app.json.dumps({"resposta" : "Deletado Com Sucesso!"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao Deletar"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Deletar"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao deletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')
    

@app.route("/Cadastro/Corretora/Search",methods = ['POST'])
def CadastroCorretoraSeach():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictCorretora(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictCorretora}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/Corretora/Load",methods = ['POST'])
def CadastroCorretoraLoad():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Corretora = cl_Corretora(**{})
                Corretora.IDCorretora = app.request.form['IDCorretora']
                if Corretora.read(app.request.form['IDCorretora']):                   
                    return app.json.dumps({"resposta" : "Ok","Dados": Corretora.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao carregar os dados"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                    
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                

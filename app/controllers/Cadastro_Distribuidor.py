from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Distribuidor import cl_Distribuidor
from flask import render_template as render_template
from flask import Markup as Markup

@app.route("/Cadastro/Distribuidor")
def CadastroDistribuidor():
    Usuario = cl_Usuario(**{}) 
    if Usuario.Auth_napi(app.session) == False : render_template('Login.html')
    fotopath = app.defaultfotopath
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    return render_template('CadastroDistribuidor.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/Distribuidor/Update",methods = ['POST'])
def CadastroDistribuidorUpdate():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
 
            Distribuidor = cl_Distribuidor(**{})
            if Distribuidor.read(app.request.form['IDDistribuidor']):
                Distribuidor.Nome = app.request.form['Nome']
                Distribuidor.CGC = app.request.form['CGC']
                Distribuidor.RazaoSocial = app.request.form['RazaoSocial']
                if Distribuidor.set():
                    return app.json.dumps({"resposta" : "Distribuidor Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao gravar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')      
            else:
                return app.json.dumps({"resposta" : "Erro ao gravar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
                                    
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Distribuidor/Insert",methods = ['POST'])
def CadastroDistribuidorInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                

            Distribuidor = cl_Distribuidor(**{})
            Distribuidor.Nome = app.request.form['Nome']
            Distribuidor.CGC = app.request.form['CGC']
            Distribuidor.RazaoSocial = app.request.form['RazaoSocial']
            if Distribuidor.insert():
                return app.json.dumps({"resposta" : "Distribuidor Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Inserir dados"}, ensure_ascii=False).encode('utf-8', 'ignore')       

        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Distribuidor/Delete",methods = ['POST'])
def CadastroDistribuidorDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Distribuidor = cl_Distribuidor(**{})
            Distribuidor.IDDistribuidor = app.request.form['IDDistribuidor']
            if Distribuidor.read(app.request.form['IDDistribuidor']):
                if Distribuidor.remove():
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

@app.route("/Cadastro/Distribuidor/Search",methods = ['POST'])
def CadastroDistribuidorSeach():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictDistribuidor(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictDistribuidor}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/Distribuidor/Load",methods = ['POST'])
def CadastroDistribuidorLoad():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Distribuidor = cl_Distribuidor(**{})
                if Distribuidor.read(app.request.form['IDDistribuidor']):                   
                    return app.json.dumps({"resposta" : "Ok","Dados": Distribuidor.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao carregar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')                   

            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                

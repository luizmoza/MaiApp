from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Emissor import cl_Emissor
from flask import render_template as render_template
from flask import Markup as Markup

@app.route("/Cadastro/Emissor")
def CadastroEmissor():
    Usuario = cl_Usuario(**{}) 
    if Usuario.Auth_napi(app.session) == False : render_template('Login.html')
    fotopath = app.defaultfotopath
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    return render_template('CadastroEmissor.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/Emissor/Update",methods = ['POST'])
def CadastroEmissorUpdate():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
 
            Emissor = cl_Emissor(**{})
            if Emissor.read(app.request.form['IDEmissor']):
                
                
                Emissor.Rating  = app.request.form['Rating']
                Emissor.Agencia  = app.request.form['Agencia']
                Emissor.RatingMAI = app.request.form['RatingMAI']
                Emissor.Categoria = app.request.form['Categoria']
                Emissor.Grupo = app.request.form['Grupo']
                Emissor.Nome = app.request.form['Nome']
                Emissor.cgc = app.request.form['cgc']
                Emissor.AliasBradesco = app.request.form['AliasBradesco']
                Emissor.AliasItau = app.request.form['AliasItau']
                Emissor.AliasMellon = app.request.form['AliasMellon']
                Emissor.TipoCIA = app.request.form['TipoCIA']
                Emissor.CategoriaListagem = app.request.form['CategoriaListagem']
                Emissor.Nacional = app.tkstr.strtobool(app.request.form['Nacional'])
                Emissor.TipoEmissor = app.request.form['TipoEmissor']
                Emissor.RatingSeP = app.request.form['RatingSeP']
                Emissor.RatingMoodys = app.request.form['RatingMoodys']
                Emissor.RatingFitch = app.request.form['RatingFitch']
                
                
                if Emissor.set():
                    return app.json.dumps({"resposta" : "Emissor Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao Gravar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Gravar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Emissor/Insert",methods = ['POST'])
def CadastroEmissorInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Emissor = cl_Emissor(**{})
            Emissor.Rating  = app.request.form['Rating']
            Emissor.Agencia  = app.request.form['Agencia']
            Emissor.RatingMAI = app.request.form['RatingMAI']
            Emissor.Categoria = app.request.form['Categoria']
            Emissor.Grupo = app.request.form['Grupo']
            Emissor.Nome = app.request.form['Nome']
            Emissor.cgc = app.request.form['cgc']
            Emissor.AliasBradesco = app.request.form['AliasBradesco']
            Emissor.AliasItau = app.request.form['AliasItau']
            Emissor.AliasMellon = app.request.form['AliasMellon']
            Emissor.TipoCIA = app.request.form['TipoCIA']
            Emissor.CategoriaListagem = app.request.form['CategoriaListagem']
            Emissor.Nacional = app.tkstr.strtobool(app.request.form['Nacional'])
            Emissor.TipoEmissor = app.request.form['TipoEmissor']
            Emissor.RatingSeP = app.request.form['RatingSeP']
            Emissor.RatingMoodys = app.request.form['RatingMoodys']
            Emissor.RatingFitch = app.request.form['RatingFitch']
            
            if Emissor.insert():
                return app.json.dumps({"resposta" : "Emissor Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Inserir Dados!"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Emissor/Delete",methods = ['POST'])
def CadastroEmissorDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Emissor = cl_Emissor(**{})
            if Emissor.read(app.request.form['IDEmissor']):
                if Emissor.remove():
                    return app.json.dumps({"resposta" : "Deletado Com Sucesso!"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                   return app.json.dumps({"resposta" : "Erro ao deletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')       
            else:
                return app.json.dumps({"resposta" : "Erro ao deletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao deletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Emissor/Search",methods = ['POST'])
def CadastroEmissorSeach():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictEmissor(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictEmissor}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/Emissor/Load",methods = ['POST'])
def CadastroEmissorLoad():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Emissor = cl_Emissor(**{})
                if Emissor.read(app.request.form['IDEmissor']):                 
                    return app.json.dumps({"resposta" : "Ok","Dados": Emissor.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao carregar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                    
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                

from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_RV import cl_RV
from flask import render_template as render_template
from flask import Markup as Markup

@app.route("/Cadastro/RV")
def CadastroRV():
    Usuario = cl_Usuario(**{}) 
    if Usuario.Auth_napi(app.session) == False : render_template('Login.html')
    fotopath = app.defaultfotopath
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    if app.tkDict.LoadDictBolsas('',1,10000):
        if app.tkDict.LoadDictMoedas('',1,10000):
            if app.tkDict.LoadDictTipoRV(""):
                        if app.tkDict.LoadDictListaEmissor(""):
                            jsonData = {
                                        'ListaBolsa':app.tkDict.DictBolsas["Listaid"],
                                        'ListaMoeda': app.tkDict.DictMoedas["Listaid"],
                                        'ListaTipoMercadoriaRV': app.tkDict.DictTipoRV,
                                        'ListaDictEmissor': app.tkDict.DictListaEmissor,
                                        }
                            
    return render_template('CadastroRendaVariavel.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/RV/Update",methods = ['POST'])
def CadastroRVUpdate():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore') 

            RV = cl_RV(**{})
            if RV.read(app.request.form['IDRV']):
                RV.Alias = app.request.form['Alias']
                RV.Codigo = app.request.form['Codigo']
                RV.Isin = app.request.form['Isin']
                RV.QtdEmitida = app.tkstr.brl_float_string_to_db(app.request.form['QtdEmitida'])
                RV.Lote = app.tkstr.brl_float_string_to_db(app.request.form['Lote'])
                RV.idMoeda = app.request.form['IdMoeda']
                RV.idBolsa	 = app.request.form['IdBolsa']
                RV.idTipoRV = app.request.form['idTipoRV']
                RV.idEmissor = app.request.form['IdEmissor']
                RV.ETF = app.tkstr.strtobool(app.request.form['ETF'])
                if RV.set():
                    return app.json.dumps({"resposta" : "RV Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao gravar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao gravar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
                        
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/RV/Insert",methods = ['POST'])
def CadastroRVInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')
                        
            RV = cl_RV(**{})
            RV.Alias = app.request.form['Alias']
            RV.Codigo = app.request.form['Codigo']
            RV.Isin = app.request.form['Isin']
            RV.QtdEmitida = app.tkstr.brl_float_string_to_db(app.request.form['QtdEmitida'])
            RV.Lote = app.tkstr.brl_float_string_to_db(app.request.form['Lote'])
            RV.idMoeda = app.request.form['IdMoeda']
            RV.idBolsa	 = app.request.form['IdBolsa']
            RV.idTipoRV = app.request.form['idTipoRV']
            RV.idEmissor = app.request.form['IdEmissor']
            RV.ETF = app.tkstr.strtobool(app.request.form['ETF'])
            
            if RV.insert():
                return app.json.dumps({"resposta" : "RV Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao inserir dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/RV/Delete",methods = ['POST'])
def CadastroRVDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')            
            
            RV = cl_RV(**{})
            if RV.read(app.request.form['IDRV']):
                if RV.remove():
                    return app.json.dumps({"resposta" : "Deletado Com Sucesso!"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao Deletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Deletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao deletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/RV/Search",methods = ['POST'])
def CadastroRVSeach():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                

                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictRV(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictRV}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/RV/Load",methods = ['POST'])
def CadastroRVLoad():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                RV = cl_RV(**{})
                if RV.read(app.request.form['IDRV']):
                    return app.json.dumps({"resposta" : "Ok","Dados": RV.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "erro ao carregar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                            
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                

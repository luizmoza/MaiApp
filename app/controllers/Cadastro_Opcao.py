from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Opcao import cl_Opcao
from flask import render_template as render_template
from flask import Markup as Markup

@app.route("/Cadastro/Opcao")
def CadastroOpcao():
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
            if app.tkDict.LoadDictTipoMercadoriaOpcao(""):
                if app.tkDict.LoadDictIDTipoMercadoriaOpcao(""):
                    jsonData = {
                                'ListaBolsa':app.tkDict.DictBolsas["Listaid"],
                                'ListaMoeda': app.tkDict.DictMoedas["Listaid"],
                                'ListaTipoMercadoriaOpcao': app.tkDict.DictTipoMercadoriaOpcao,
                                'ListaIDTipoMercadoriaOpcao': app.tkDict.DictIDTipoMercadoriaOpcao
                                }
    return render_template('CadastroOpcao.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/Opcao/Update",methods = ['POST'])
def CadastroOpcaoUpdate():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
 
            Opcao = cl_Opcao(**{})
            if Opcao.read(app.request.form['IDOpcao']):
                Opcao.Alias = app.request.form['Alias']
                Opcao.Isin = app.request.form['Isin']
                Opcao.Codigo = app.request.form['Codigo']
                Opcao.PrecoExercicio = app.tkstr.brl_float_string_to_db(app.request.form['PrecoExercicio'])
                Opcao.IdMoedaPrecoExercicio = app.request.form['IdMoedaPrecoExercicio']
                Opcao.TipoOpcao = app.request.form['TipoOpcao']
                Opcao.TipoEstilo = app.request.form['TipoEstilo']
                Opcao.MultiplicadorContrato = app.tkstr.brl_float_string_to_db(app.request.form['MultiplicadorContrato'])
                Opcao.Quantidade = app.tkstr.brl_float_string_to_db(app.request.form['Quantidade'])
                Opcao.LoteAlocacao = app.tkstr.brl_float_string_to_db(app.request.form['LoteAlocacao'])
                Opcao.PremioPagoAntecip = app.tkstr.strtobool(app.request.form['PremioPagoAntecip'])
                Opcao.idBolsa = app.request.form['idBolsa']
                Opcao.idMoeda = app.request.form['idMoeda']
                Opcao.IdTipoMercadoriaOpcao = app.request.form['IdTipoMercadoriaOpcao']
                Opcao.DataVencimento = app.request.form['DataVencimento']
                Opcao.DatainicioNegociacao = app.request.form['DatainicioNegociacao']
                Opcao.DataConclusaoNegociacao = app.request.form['DataConclusaoNegociacao']
                Opcao.DataPosicaoAberto = app.request.form['DataPosicaoAberto']
                if Opcao.set():
                    return app.json.dumps({"resposta" : "Opcao Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao alterar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao alterar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Opcao/Insert",methods = ['POST'])
def CadastroOpcaoInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Opcao = cl_Opcao(**{})
            Opcao.Alias = app.request.form['Alias']
            Opcao.Isin = app.request.form['Isin']
            Opcao.Codigo = app.request.form['Codigo']
            Opcao.PrecoExercicio = app.tkstr.brl_float_string_to_db(app.request.form['PrecoExercicio'])
            Opcao.IdMoedaPrecoExercicio = app.request.form['IdMoedaPrecoExercicio']
            Opcao.TipoOpcao = app.request.form['TipoOpcao']
            Opcao.TipoEstilo = app.request.form['TipoEstilo']
            Opcao.MultiplicadorContrato = app.tkstr.brl_float_string_to_db(app.request.form['MultiplicadorContrato'])
            Opcao.Quantidade = app.tkstr.brl_float_string_to_db(app.request.form['Quantidade'])
            Opcao.LoteAlocacao = app.tkstr.brl_float_string_to_db(app.request.form['LoteAlocacao'])
            Opcao.PremioPagoAntecip = app.tkstr.strtobool(app.request.form['PremioPagoAntecip'])
            Opcao.idBolsa = app.request.form['idBolsa']
            Opcao.idMoeda = app.request.form['idMoeda']
            Opcao.IdTipoMercadoriaOpcao = app.request.form['IdTipoMercadoriaOpcao']
            Opcao.DataVencimento = app.request.form['DataVencimento']
            Opcao.DatainicioNegociacao = app.request.form['DatainicioNegociacao']
            Opcao.DataConclusaoNegociacao = app.request.form['DataConclusaoNegociacao']
            Opcao.DataPosicaoAberto = app.request.form['DataPosicaoAberto']
            if Opcao.insert():
                return app.json.dumps({"resposta" : "Opcao Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao inserir"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            app.db.Session_Close()
            app.db.Session_Start()
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Opcao/Delete",methods = ['POST'])
def CadastroOpcaoDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Opcao = cl_Opcao(**{})
            if Opcao.read(app.request.form['IDOpcao']):
                if Opcao.remove():
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

@app.route("/Cadastro/Opcao/Search",methods = ['POST'])
def CadastroOpcaoSeach():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictOpcao(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictOpcao}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/Opcao/Load",methods = ['POST'])
def CadastroOpcaoLoad():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Opcao = cl_Opcao(**{})
                if Opcao.read(app.request.form['IDOpcao']):
                    return app.json.dumps({"resposta" : "Ok","Dados": Opcao.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao carregar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')                                
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                

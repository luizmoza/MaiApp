from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Fundo import cl_Fundo
from flask import render_template as render_template
from flask import Markup as Markup

@app.route("/Cadastro/Fundo")
def CadastroFundo():
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
                    jsonData = {
                                'ListaBolsa':app.tkDict.DictBolsas["Listaid"],
                                'ListaMoeda': app.tkDict.DictMoedas["Listaid"],
                                }
    return render_template('CadastroFundo.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/Fundo/Update",methods = ['POST'])
def CadastroFundoUpdate():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
 
            Fundo = cl_Fundo(**{})
            if Fundo.read(app.request.form['IDFundo']):
                Fundo.CGC= app.request.form['CGC']		
                Fundo.Nome= app.request.form['Nome']		
                Fundo.AliasCota= app.request.form['AliasCota']		
                Fundo.Tipo = app.request.form['Tipo']		
                Fundo.RegraResgate = app.request.form['RegraResgate']		
                Fundo.RegraAplicacao = app.request.form['RegraAplicacao']		
                Fundo.Administrador = app.request.form['Administrador']	
                Fundo.DataInicioMai = app.request.form['DataInicioMai']
                Fundo.DataFimMai = app.request.form['DataFimMai']
                Fundo.Banco = app.request.form['Banco']	
                Fundo.Agencia = app.request.form['Agencia']	
                Fundo.Conta = app.request.form['Conta']	
                Fundo.CetipConta = app.request.form['CetipConta']	
                Fundo.CetipMiolo = app.request.form['CetipMiolo']	
                Fundo.Alias = app.request.form['Alias']	
                Fundo.ISIN = app.request.form['ISIN']	
                Fundo.idBolsa = app.request.form['IdBolsa']
                Fundo.idMoeda = app.request.form['IdMoeda']
                Fundo.Benchmark = app.request.form['Benchmark']
                Fundo.digito = app.request.form['Digito']
                Fundo.CetipDigito = app.request.form['CetipDigito']
                Fundo.TipoInvestidor = app.request.form['TipoInvestidor']
                Fundo.TipoCondominio = app.request.form['TipoCondominio']
                Fundo.SubTipo = app.request.form['SubTipo']
                Fundo.Segmento = app.request.form['Segmento']

                Fundo.Alavancagem = app.tkstr.brl_float_string_to_db( app.request.form['Alavancagem'])
                Fundo.TaxaPerformance = app.request.form['TaxaPerformance']
                Fundo.TaxaAdministracao = app.request.form['TaxaAdministracao']

                Fundo.FIC = app.tkstr.strtobool(app.request.form['FIC'])
                Fundo.IncentivoFiscal = app.tkstr.strtobool(app.request.form['IncentivoFiscal'])
                Fundo.Adaptado4661 = app.tkstr.strtobool(app.request.form['Adaptado4661'])
                Fundo.Adaptado3922 = app.tkstr.strtobool(app.request.form['Adaptado3922'])
                Fundo.Adaptado4444 = app.tkstr.strtobool(app.request.form['Adaptado4444'])
                Fundo.Abertura = app.tkstr.strtobool(app.request.form['Abertura'])
                Fundo.Interno = app.tkstr.strtobool(app.request.form['Interno'])
                Fundo.PassivoRestrito = app.tkstr.strtobool(app.request.form['PassivoRestrito'])
                Fundo.ETF = app.tkstr.strtobool(app.request.form['ETF'])
                Fundo.Derivativos = app.tkstr.strtobool(app.request.form['Derivativos'])
                Fundo.Descoberto = app.tkstr.strtobool(app.request.form['Descoberto'])
                Fundo.BenchmarkPlano = ''
                if Fundo.set():
                    return app.json.dumps({"resposta" : "Fundo Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao Gravar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')               
            else:
                return app.json.dumps({"resposta" : "Erro ao Gravar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')

        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Fundo/Insert",methods = ['POST'])
def CadastroFundoInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Fundo = cl_Fundo(**{})
            Fundo.CGC= app.request.form['CGC']		
            Fundo.Nome= app.request.form['Nome']		
            Fundo.AliasCota= app.request.form['AliasCota']		
            Fundo.Tipo = app.request.form['Tipo']		
            Fundo.RegraResgate = app.request.form['RegraResgate']		
            Fundo.RegraAplicacao = app.request.form['RegraAplicacao']		
            Fundo.Administrador = app.request.form['Administrador']	
            Fundo.DataInicioMai = app.request.form['DataInicioMai']
            Fundo.DataFimMai = app.request.form['DataFimMai']
            Fundo.Banco = app.request.form['Banco']	
            Fundo.Agencia = app.request.form['Agencia']	
            Fundo.Conta = app.request.form['Conta']	
            Fundo.CetipConta = app.request.form['CetipConta']	
            Fundo.CetipMiolo = app.request.form['CetipMiolo']	
            Fundo.Alias = app.request.form['Alias']	
            Fundo.ISIN = app.request.form['ISIN']	
            Fundo.idBolsa = app.request.form['IdBolsa']
            Fundo.idMoeda = app.request.form['IdMoeda']
            Fundo.Benchmark = app.request.form['Benchmark']
            Fundo.digito = app.request.form['Digito']
            Fundo.CetipDigito = app.request.form['CetipDigito']
            Fundo.TipoInvestidor = app.request.form['TipoInvestidor']
            Fundo.TipoCondominio = app.request.form['TipoCondominio']
            Fundo.SubTipo = app.request.form['SubTipo']
            Fundo.Segmento = app.request.form['Segmento']

            Fundo.Alavancagem = app.tkstr.brl_float_string_to_db( app.request.form['Alavancagem'])
            Fundo.TaxaPerformance = app.request.form['TaxaPerformance']
            Fundo.TaxaAdministracao =  app.request.form['TaxaAdministracao']

            Fundo.FIC = app.tkstr.strtobool(app.request.form['FIC'])
            Fundo.IncentivoFiscal = app.tkstr.strtobool(app.request.form['IncentivoFiscal'])
            Fundo.Adaptado4661 = app.tkstr.strtobool(app.request.form['Adaptado4661'])
            Fundo.Adaptado3922 = app.tkstr.strtobool(app.request.form['Adaptado3922'])
            Fundo.Adaptado4444 = app.tkstr.strtobool(app.request.form['Adaptado4444'])
            Fundo.Abertura = app.tkstr.strtobool(app.request.form['Abertura'])
            Fundo.Interno = app.tkstr.strtobool(app.request.form['Interno'])
            Fundo.PassivoRestrito = app.tkstr.strtobool(app.request.form['PassivoRestrito'])
            Fundo.ETF = app.tkstr.strtobool(app.request.form['ETF'])
            Fundo.Derivativos = app.tkstr.strtobool(app.request.form['Derivativos'])
            Fundo.Descoberto = app.tkstr.strtobool(app.request.form['Descoberto'])
            Fundo.BenchmarkPlano = ''
            
            if Fundo.insert():
                return app.json.dumps({"resposta" : "Fundo Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Inserir Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Fundo/Delete",methods = ['POST'])
def CadastroFundoDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Fundo = cl_Fundo(**{})
            if Fundo.read(app.request.form['IDFundo']):
                if Fundo.remove():
                    return app.json.dumps({"resposta" : "Deletado Com Sucesso!"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao Deletar Fundo"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Deletar Fundo"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao deletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Fundo/Search",methods = ['POST'])
def CadastroFundoSeach():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictFundos(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictFundos}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/Fundo/Load",methods = ['POST'])
def CadastroFundoLoad():
        if app.request.method == 'POST':
            try:
                
                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Fundo = cl_Fundo(**{})
                if Fundo.read(app.request.form['IDFundo']):
                    return app.json.dumps({"resposta" : "Ok","Dados": Fundo.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao carregar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                    
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                

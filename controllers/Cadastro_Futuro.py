from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Futuro import cl_Futuro
from flask import render_template as render_template
from flask import Markup as Markup

@app.route("/Cadastro/Futuro")
def CadastroFuturo():
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
            if app.tkDict.LoadDictTipoMercadoriaFuturo(""):
                    jsonData = {
                                'ListaBolsa':app.tkDict.DictBolsas["Listaid"],
                                'ListaMoeda': app.tkDict.DictMoedas["Listaid"],
                                'ListaTipoMercadoriaFuturo': app.tkDict.DictTipoMercadoriaFuturo,
                                }
    return render_template('CadastroFuturo.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/Futuro/Update",methods = ['POST'])
def CadastroFuturoUpdate():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
 
            Futuro = cl_Futuro(**{})
            if Futuro.read(app.request.form['IDFuturo']):
                Futuro.Alias = app.request.form['Alias']
                Futuro.CodIsin = app.request.form['CodIsin']
                Futuro.Codigo = app.request.form['Codigo']
                Futuro.CodVencimento = app.request.form['CodVencimento']
                Futuro.BaseData = app.request.form['BaseData']
                Futuro.NumeroPontosVencimento = app.tkstr.brl_float_string_to_db(app.request.form['NumeroPontosVencimento'])
                Futuro.TaxaConvertPreco = app.tkstr.brl_float_string_to_db(app.request.form['TaxaConvertPreco'])
                Futuro.MultiplicadorContrato = app.tkstr.brl_float_string_to_db(app.request.form['MultiplicadorContrato'])
                Futuro.Quantidade = app.tkstr.brl_float_string_to_db(app.request.form['Quantidade'])
                Futuro.LoteAlocacao = app.tkstr.brl_float_string_to_db(app.request.form['LoteAlocacao'])
                Futuro.idMoeda = app.request.form['IdMoeda']
                Futuro.idBolsa = app.request.form['IdBolsa']
                Futuro.DataVencimento = app.request.form['DataVencimento']
                Futuro.idTipoMercadoriaFuturo = app.request.form['idTipoMercadoriaFuturo']
                Futuro.DataConclusaoNegociacao = app.request.form['DataConclusaoNegociacao']
                
                if Futuro.set():
                    return app.json.dumps({"resposta" : "Futuro Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao gravar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao gravar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Futuro/Insert",methods = ['POST'])
def CadastroFuturoInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Futuro = cl_Futuro(**{})
            Futuro.Alias = app.request.form['Alias']
            Futuro.CodIsin = app.request.form['CodIsin']
            Futuro.Codigo = app.request.form['Codigo']
            Futuro.CodVencimento = app.request.form['CodVencimento']
            Futuro.BaseData = app.request.form['BaseData']
            Futuro.NumeroPontosVencimento = app.tkstr.brl_float_string_to_db(app.request.form['NumeroPontosVencimento'])
            Futuro.TaxaConvertPreco = app.tkstr.brl_float_string_to_db(app.request.form['TaxaConvertPreco'])
            Futuro.MultiplicadorContrato = app.tkstr.brl_float_string_to_db(app.request.form['MultiplicadorContrato'])
            Futuro.Quantidade = app.tkstr.brl_float_string_to_db(app.request.form['Quantidade'])
            Futuro.LoteAlocacao = app.tkstr.brl_float_string_to_db(app.request.form['LoteAlocacao'])
            Futuro.idMoeda = app.request.form['IdMoeda']
            Futuro.idBolsa = app.request.form['IdBolsa']
            Futuro.DataVencimento = app.request.form['DataVencimento']
            Futuro.idTipoMercadoriaFuturo = app.request.form['idTipoMercadoriaFuturo']
            Futuro.DataConclusaoNegociacao = app.request.form['DataConclusaoNegociacao']
            if Futuro.insert():
                return app.json.dumps({"resposta" : "Futuro Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao inserir dados: " + Futuro.__db__.statusquery }, ensure_ascii=False).encode('utf-8', 'ignore')

        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Futuro/Delete",methods = ['POST'])
def CadastroFuturoDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Futuro = cl_Futuro(**{})
            if Futuro.read(app.request.form['IDFuturo']):
                if Futuro.remove():
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

@app.route("/Cadastro/Futuro/Search",methods = ['POST'])
def CadastroFuturoSeach():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictFuturo(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictFuturo}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/Futuro/Load",methods = ['POST'])
def CadastroFuturoLoad():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Futuro = cl_Futuro(**{})
                if Futuro.read(app.request.form['IDFuturo']):
                    return app.json.dumps({"resposta" : "Ok","Dados": Futuro.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                    
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                

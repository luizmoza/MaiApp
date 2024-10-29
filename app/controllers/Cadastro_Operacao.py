from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Operacao import cl_Operacao
from flask import render_template as render_template
from flask import Markup as Markup

@app.route("/Cadastro/Operacao")
def CadastroOperacao():
    Usuario = cl_Usuario(**{}) 
    if Usuario.Auth_napi(app.session) == False : render_template('Login.html')
    fotopath = app.defaultfotopath
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    if app.tkDict.LoadDictEstrategias('',1,10000):jsonData = {'DictEstrategias':app.tkDict.DictEstrategias}
    return render_template('CadastroOperacao.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/Operacao/Update",methods = ['POST'])
def CadastroOperacaoUpdate():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
 
            Operacao = cl_Operacao(**{})
            Operacao.AliasOperacao = app.request.form['AliasOperacao']
            Operacao.CGC = app.request.form['CGC']

            if Operacao.Load(app.request.form['AliasOperacao'],app.request.form['CGC']) == False:
                return app.json.dumps({"resposta" : "Operacao Não Existe!"}, ensure_ascii=False).encode('utf-8', 'ignore')

            Operacao.Administrador = app.request.form['Administrador']
            Operacao.AliasAtivo = app.request.form['AliasAtivo']
            Operacao.Estrategia = app.request.form['Estrategia']
            Operacao.PuCompra	 = app.request.form['PuCompra']
            Operacao.TaxaCompra	 = app.request.form['TaxaCompra']
            Operacao.Marcacao = app.request.form['Marcacao']
            Operacao.Vencimento	 = app.request.form['Vencimento']
            Operacao.DataCompra	 = app.request.form['DataCompra']
            Operacao.MacroEstrategia = app.request.form['MacroEstrategia']
            Operacao.DataLog = app.tkdtm.hoje

            if Operacao.Update(Operacao.Administrador,Operacao.AliasAtivo,Operacao.Estrategia,Operacao.PuCompra,Operacao.TaxaCompra,Operacao.Marcacao,Operacao.Vencimento,Operacao.FormulaPrecificacao,Operacao.DataCompra,Operacao.PuVencimento,Operacao.TravaEdicao,Operacao.MacroEstrategia,Operacao.DataLog,Operacao.AliasOperacao,Operacao.CGC):           
                return app.json.dumps({"resposta" : "Operacao Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
               return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: "}, ensure_ascii=False).encode('utf-8', 'ignore')
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Operacao/Insert",methods = ['POST'])
def CadastroOperacaoInsert():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            
            Operacao = cl_Operacao(**{})
            Operacao.AliasOperacao = app.request.form['AliasOperacao']
            Operacao.CGC = app.request.form['CGC']

            if Operacao.Exists(app.request.form['AliasOperacao'],app.request.form['CGC']):
                return app.json.dumps({"resposta" : "Operacao Já Existe!"}, ensure_ascii=False).encode('utf-8', 'ignore')

            Operacao.Administrador = app.request.form['Administrador']
            Operacao.AliasAtivo = app.request.form['AliasAtivo']
            Operacao.Estrategia = app.request.form['Estrategia']
            Operacao.PuCompra	 = app.tkstr.brl_float_string_to_db(app.request.form['PuCompra'])
            Operacao.TaxaCompra	 = app.tkstr.brl_float_string_to_db(app.request.form['TaxaCompra'])
            Operacao.Marcacao = app.request.form['Marcacao']
            Operacao.Vencimento	 = app.request.form['Vencimento']
            Operacao.FormulaPrecificacao = ''
            Operacao.DataCompra	 = app.request.form['DataCompra']
            Operacao.PuVencimento = 0
            Operacao.TravaEdicao = False
            Operacao.MacroEstrategia = app.request.form['MacroEstrategia']
            Operacao.DataLog = app.tkdtm.hoje
            
            if Operacao.Insert(Operacao.Administrador,Operacao.AliasAtivo,Operacao.Estrategia,Operacao.PuCompra,Operacao.TaxaCompra,Operacao.Marcacao,Operacao.Vencimento,Operacao.FormulaPrecificacao,Operacao.DataCompra,Operacao.PuVencimento,Operacao.TravaEdicao,Operacao.MacroEstrategia,Operacao.DataLog,Operacao.AliasOperacao,Operacao.CGC):
                return app.json.dumps({"resposta" : "Operacao Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Gravar" + Operacao.__db__.statusquery }, ensure_ascii=False).encode('utf-8', 'ignore')
        
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/Operacao/Delete",methods = ['POST'])
def CadastroOperacaoDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                

            Operacao = cl_Operacao(**{})
            Operacao.AliasOperacao = app.request.form['AliasOperacao']
            Operacao.CGC = app.request.form['CGC']
            if Operacao.Exists(app.request.form['AliasOperacao'],app.request.form['CGC']):
                if Operacao.Delete():
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

@app.route("/Cadastro/Operacao/Search",methods = ['POST'])
def CadastroOperacaoSeach():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictOperacoes(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictOperacoes}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/Operacao/Load",methods = ['POST'])
def CadastroOperacaoLoad():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Operacao = cl_Operacao(**{})
                saliasop = app.request.form['IDOperacao'].split('#')
                Operacao.AliasOperacao = saliasop[1]
                Operacao.CGC = saliasop[0]

                if Operacao.Load(Operacao.AliasOperacao,Operacao.CGC) == False:
                    return app.json.dumps({"resposta" : "Operacao Não Existe!"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Ok","Dados": Operacao.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')

            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                

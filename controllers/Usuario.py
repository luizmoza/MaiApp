from app import app
from app.classes.cl_Usuario import cl_Usuario
from flask import render_template as render_template
from flask import Markup as Markup

#

@app.route("/Usuario/Cadastro")
def CadastroUsuario():
    if app.request.query_string != '':
        Usuario = cl_Usuario(**{})
        if Usuario.Auth_recover(app.session,str(app.request.query_string, encoding='utf-8')):        
            return render_template('CadastroUsuario.html',
                                Usuario_Email = app.session['Usuario_Email'],
                                Usuario_Id = str(app.session['Usuario_Id']),
                                Usuario_Auth = str(app.session['Usuario_Auth'])
                                )
        else:
            print(app.db.statusquery)
            return render_template('Login.html')
    else:
        return render_template('Login.html')
    
@app.route("/Usuario/GravaDados",methods = ['POST'])
def GravaDadosUsuario():
    if app.request.method == 'POST':
        try:
            Usuario = cl_Usuario(**{})
            Usuario.idUsuario = app.request.form['idUsuario']
            if Usuario.get():
                Usuario.Email = app.request.form['Email']
                Usuario.Nome = app.request.form['Nome']
                Usuario.Senha = app.request.form['Senha']
                if Usuario.set():
                    return app.json.dumps({"resposta" : "Usuário Gravado com Sucesso","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao Gravar Dados do Usuário","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Erro ao Gravar Dados do Usuário","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')
        except:
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados do Usuário","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')


@app.route("/Usuario/ManipulaFoto",methods = ['POST'])
def ManipulaFoto():
    Usuario = cl_Usuario(**{})
    Usuario.idUsuario = app.request.form['Usuario_Id']
    if app.request.method == 'POST':   
        if 'file' in app.request.files:
            try:
                f = app.request.files['file'] 
                ext = '.jpg'
                if app.tkstr.right(f.filename,4)=='.png': ext = '.png'
                if app.tkstr.right(f.filename,4) != '.png' and app.tkstr.right(f.filename,4) != '.jpg':
                    return  app.json.dumps({"resposta" : "Extensão do Arquivo Inválida. tente .jpg ou .png","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')  
                if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): 
                    app.tkfm.delete_file(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png')
                if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): 
                    app.tkfm.delete_file(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg')   
                f.save( app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  ext)  
                return  app.json.dumps({"resposta" : "Arquivo Salvo Com Sucesso","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')    
            except:
              return  app.json.dumps({"resposta" : "Erro ao Salvar Arquivo","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
          return  app.json.dumps({"resposta" : "Arquivo Inválido","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
      return  app.json.dumps({"resposta" : "Request Inválida","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')        

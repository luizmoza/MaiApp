from app import app
from flask import render_template as render_template
from app.classes.cl_Usuario import cl_Usuario
from flask import Markup as Markup

#

@app.route("/Recover")
def Recover():
    return render_template('Recover.html')
    
@app.route("/InciaRessetSenha",methods = ['POST'])
def InciaRessetSenha():
    if app.request.method == 'POST':
        Usuario = cl_Usuario(**{}) 
        if Usuario.Reset_pwd(app.session,app.request):
            return app.json.dumps({"resposta" : "Email Enviado!","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Erro ao Enviar Email!","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Usuário Invalido"}, ensure_ascii=False).encode('utf-8', 'ignore')
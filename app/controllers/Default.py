from app import app
from flask import render_template as render_template
from app.classes.cl_Usuario import cl_Usuario
from flask import Markup as Markup

#

@app.route("/index")
@app.route("/")
@app.route("/Login")
def index():
    return render_template('Login.html')

@app.route("/ValidaUsuarioLogin",methods = ['POST'])
def ValidaUsuarioLogin():
    if app.request.method == 'POST':
        Usuario = cl_Usuario(**{})
        if Usuario.get_id_by_email(app.request.form['Email']):
            if Usuario.Auth_login(app.session,Usuario.idUsuario,app.request.form['Senha']):
                return app.json.dumps({"resposta" : "Usuario Validado","Usuario_Id" : str(Usuario.idUsuario)}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                return app.json.dumps({"resposta" : "Senha Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Usuario não Existe"}, ensure_ascii=False).encode('utf-8', 'ignore')
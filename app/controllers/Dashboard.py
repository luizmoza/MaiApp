from app import app
from flask import render_template as render_template
from app.classes.cl_Usuario import cl_Usuario


@app.route("/Main")
def Main():
    vv = True
    if 'Usuario_Email' not in app.session : vv = False 
    if 'Usuario_Id' not in app.session : vv = False
    if 'Usuario_Auth' not in app.session : vv = False
    if vv == False :
        return render_template('Login.html')        
    else:
        if app.session['Usuario_Email'] == '' : return render_template('Login.html')        
        if app.session['Usuario_Id'] == '' : return render_template('Login.html')        
        if app.session['Usuario_Auth'] == '' : return render_template('Login.html') 
    
    Usuario = cl_Usuario(**{}) 
    if not Usuario.read(app.session['Usuario_Id']) : return render_template('Login.html')  
    
    fotopath = app.defaultfotopath 
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    return render_template('Main.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           User_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )

@app.route("/Overview")
def Overview():
    vv = True
    if 'Usuario_Email' not in app.session : vv = False 
    if 'Usuario_Id' not in app.session : vv = False
    if 'Usuario_Auth' not in app.session : vv = False
    if vv == False :
        return render_template('Login.html')        
    else:
        if app.session['Usuario_Email'] == '' : return render_template('Login.html')        
        if app.session['Usuario_Id'] == '' : return render_template('Login.html')        
        if app.session['Usuario_Auth'] == '' : return render_template('Login.html') 

    Usuario = cl_Usuario(**{}) 
    Usuario = Usuario.read(app.session['Usuario_Id']) 
    
    fotopath = app.defaultfotopath 
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()

    xls = app.pd.ExcelFile(app.tk.PathFileDashboard + app.sep + 'Dados_Exemplo.xlsx')
    df1 = app.pd.read_excel(xls, 'DataBase')
    df2 = app.pd.read_excel(xls, 'Aum')
    df3 = app.pd.read_excel(xls, 'Distrib')
    df4 = app.pd.read_excel(xls, 'StatusBatimento')
    xls.close()
    df1['Data'] = app.pd.to_datetime(df1['Data'],errors='coerce').dt.strftime('%Y-%m-%d')
    df2['Data'] = app.pd.to_datetime(df2['Data'],errors='coerce').dt.strftime('%Y-%m-%d')
    df4['Data'] = app.pd.to_datetime(df4['Data'],errors='coerce').dt.strftime('%Y-%m-%d')
    arr2 = [['Data','AUM','Num_Cotistas']]
    for index,row in df2.iterrows():arr2.append([row['Data'],row['AUM'],row['Num_Cotistas']])
    arr3 = [['Estratégia','Fin']]
    for index,row in df3.iterrows():arr3.append([row['Estratégia'],row['Fin']])
    arr4 = [['Data','Num_Fundos']]
    for index,row in df4.iterrows():arr4.append([row['Data'],row['Num_Fundos']])
    jsonData = {'DataBase': df1.to_dict('records'),'Aum': arr2,'Distrib': arr3,'StatusBatimento': arr4}
    return render_template('Overview.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = Usuario.Nome,
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           User_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )

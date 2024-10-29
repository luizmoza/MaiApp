from app import app
#
class cl_tkEmail:
    def __init__(self):
        self.server_path = 'https://localhost:5000'
        self.db = app.db
        self.conteudo = ''
        self.css = ''' 
                    <style>   
                    .email p {
                        font-size: 20px;
                        font-family: Arial, Helvetica, sans-serif;
                    }
                    </style>
                    '''
    def EnviaEmailRecover(self,UserEmail,link):
        vv = False
        outlook = app.win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = UserEmail
        mail.Subject = 'Recuperação de Senha'
        self.conteudo =  '<p> Segue link para recuperação de sua senha do MaiApp: </p><a href="' + self.server_path + app.sept + link + '">Clique Aqui!</a>'
        mail.HTMLBody = f'''
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    {self.css}
                </head>
                <body>
                    <section class="email">
                        {self.conteudo}
                    </section>
                </body>
            </html>
            '''        
        mail.Send()
        vv = True
        return vv
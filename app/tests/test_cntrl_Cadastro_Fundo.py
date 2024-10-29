import pytest
from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Fundo import cl_Fundo

class TestCntrlFundo:
    
    @pytest.fixture()
    def test_object(self):
        Usuario = cl_Usuario(**{})
        Usuario.idUsuario = app.test_idUsuario
        Usuario.get()
        return Usuario

    @pytest.fixture()
    def client(self): return app.test_client() 

    @pytest.mark.REQUEST
    def test_render(self,client,test_object):
        with client.session_transaction() as session:
            session['Usuario_Email'] = test_object.Email
            session['Usuario_Id'] = test_object.idUsuario
            session['Usuario_Auth'] = test_object.ChaveTrocaSenha
        response = client.get('/Cadastro/RF')
        assert response.status_code == 200

    @pytest.mark.REQUEST
    @pytest.mark.skipif(app.enviroment == 'prd',reason="isolamento")
    def test_request_setup_crudcycle(self,client,test_object):
        generic_object = cl_Fundo(**{})
        guid = app.tk.generate_guid()

        generic_object.CGC = guid	
        generic_object.Nome = guid	
        generic_object.AliasCota = guid			
        generic_object.Tipo = ''		
        generic_object.RegraResgate = ''			
        generic_object.RegraAplicacao = ''		
        generic_object.Administrador = ''	
        generic_object.DataInicioMai = ''	
        generic_object.DataFimMai = ''	
        generic_object.Banco = ''	
        generic_object.Agencia = ''	
        generic_object.Conta = ''	
        generic_object.CetipConta = ''		
        generic_object.CetipMiolo = ''		
        generic_object.Alias  = guid		
        generic_object.ISIN  = guid	
        generic_object.IdBolsa = '1'	
        generic_object.IdMoeda = '1'
        generic_object.Benchmark = '1'
        generic_object.Digito = '1'
        generic_object.CetipDigito = '1'
        generic_object.TipoInvestidor = '1'
        generic_object.TipoCondominio = '1'
        generic_object.SubTipo = '1'
        generic_object.Segmento = '1'
        generic_object.Alavancagem = '1'
        generic_object.TaxaPerformance = '1'
        generic_object.TaxaAdministracao = '1'
        generic_object.FIC = 'True'
        generic_object.IncentivoFiscal = 'True'
        generic_object.Adaptado4661 = 'True'
        generic_object.Adaptado3922 = 'True'
        generic_object.Adaptado4444 = 'True'
        generic_object.Abertura = 'True'
        generic_object.Interno = 'True'
        generic_object.PassivoRestrito = 'True'
        generic_object.ETF = 'True'
        generic_object.Derivativos = 'True'
        generic_object.Descoberto = 'True'
        
        dados = {}
        for k,v in app.tk.ParseNewObjectDict(generic_object).items(): dados[k] = v
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        response1 = client.post('/Cadastro/Fundo/Insert',content_type='multipart/form-data', data=dados)
        assert response1.status_code == 200
        assert app.json.loads(response1.data.decode('utf-8'))['resposta'] =='Fundo Gravado com Sucesso'
        generic_object.Alias = guid
        generic_object.get_id_by_CGC()
        dados = {}
        for k,v in app.tk.ParseObjectDict(generic_object).items(): dados[k] = v
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        response2 = client.post('/Cadastro/Fundo/Update',content_type='multipart/form-data', data=dados)
        assert response2.status_code == 200
        assert app.json.loads(response2.data.decode('utf-8'))['resposta'] =='Fundo Gravado com Sucesso'
        response3 = client.post('/Cadastro/Fundo/Load',content_type='multipart/form-data', data=dados)
        assert response3.status_code == 200
        assert app.json.loads(response3.data.decode('utf-8'))['resposta'] =='Ok'
        response4 = client.post('/Cadastro/Fundo/Delete',content_type='multipart/form-data', data=dados)
        assert response4.status_code == 200
        assert app.json.loads(response4.data.decode('utf-8'))['resposta'] =='Deletado Com Sucesso!'
        

    @pytest.mark.LOADERS
    def test_request_setup_search(self,test_object,client):
        dados = {}
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        dados['Pag'] = '1'
        dados['nPerPag'] = '10'
        dados['Search'] = ''
        responsesearch = client.post('/Cadastro/Fundo/Search',content_type='multipart/form-data', data=dados)
        assert responsesearch.status_code == 200
        assert app.json.loads(responsesearch.data.decode('utf-8'))['resposta'] == 'Ok'

        
        
    

import pytest
from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Opcao import cl_Opcao

class TestCntrlOpcao:
    
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
        generic_object = cl_Opcao(**{})
        guid = app.tk.generate_guid()

        generic_object.Alias = guid
        generic_object.Isin = guid
        generic_object.Codigo = guid
        generic_object.PrecoExercicio = '0'
        generic_object.IdMoedaPrecoExercicio = '1'
        generic_object.TipoOpcao = ''
        generic_object.TipoEstilo = ''
        generic_object.MultiplicadorContrato = '0'
        generic_object.Quantidade = '0'
        generic_object.LoteAlocacao = '0'
        generic_object.PremioPagoAntecip = False
        generic_object.idBolsa = '1'
        generic_object.idMoeda = '1'
        generic_object.IdTipoMercadoriaOpcao = '1'
        generic_object.DataVencimento = '2024-01-01'
        generic_object.DatainicioNegociacao = '2024-01-01'
        generic_object.DataConclusaoNegociacao = '2024-01-01'
        generic_object.DataPosicaoAberto = '2024-01-01'      
        
        dados = {}
        for k,v in app.tk.ParseNewObjectDict(generic_object).items(): dados[k] = v
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        response1 = client.post('/Cadastro/Opcao/Insert',content_type='multipart/form-data', data=dados)
        assert response1.status_code == 200
        assert app.json.loads(response1.data.decode('utf-8'))['resposta'] =='Opcao Gravado com Sucesso'
        generic_object.Alias = guid
        generic_object.get_id_alias()
        dados = {}
        for k,v in app.tk.ParseObjectDict(generic_object).items(): dados[k] = v
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        response2 = client.post('/Cadastro/Opcao/Update',content_type='multipart/form-data', data=dados)
        assert response2.status_code == 200
        assert app.json.loads(response2.data.decode('utf-8'))['resposta'] =='Opcao Gravado com Sucesso'
        response3 = client.post('/Cadastro/Opcao/Load',content_type='multipart/form-data', data=dados)
        assert response3.status_code == 200
        assert app.json.loads(response3.data.decode('utf-8'))['resposta'] =='Ok'
        response4 = client.post('/Cadastro/Opcao/Delete',content_type='multipart/form-data', data=dados)
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
        responsesearch = client.post('/Cadastro/Opcao/Search',content_type='multipart/form-data', data=dados)
        assert responsesearch.status_code == 200
        assert app.json.loads(responsesearch.data.decode('utf-8'))['resposta'] == 'Ok'

        
        
    

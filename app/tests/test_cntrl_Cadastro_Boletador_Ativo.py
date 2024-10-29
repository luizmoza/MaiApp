import pytest
from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Mov import cl_Mov

class TestCntrlPassivo:
    
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
        generic_object = cl_Mov(**{})
        guid = app.tk.generate_guid()
        generic_object.idTrader = '1'
        generic_object.idCorretora = '1'
        generic_object.idEstrategia = '1'
        generic_object.DataMov = "2024-01-01"
        generic_object.CGC = guid
        generic_object.AliasAtivo = guid
        generic_object.Qtd = '0'
        generic_object.Pu = '0'
        generic_object.Taxa = '0'
        generic_object.Corretagem = '0'
        generic_object.TipoCompromisso = guid
        generic_object.DataCompromisso = "2024-01-01"
        generic_object.PuCompromisso = '0'
        generic_object.Marcacao = guid
        generic_object.get_sample_fk()      
        dados = {}
        for k,v in app.tk.ParseNewObjectDict(generic_object).items(): dados[k] = v
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        dados['IDMov'] = '-1'
        response1 = client.post('/Boletador/Ativo/Upsert',content_type='multipart/form-data', data=dados)
        assert response1.status_code == 200
        assert app.json.loads(response1.data.decode('utf-8'))['resposta'] =='Ativo Gravado com Sucesso'
        generic_object.Alias = guid
        generic_object.get_id_TipoCompromisso()
        dados = {}
        for k,v in app.tk.ParseObjectDict(generic_object).items(): dados[k] = v
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        response2 = client.post('/Boletador/Ativo/Upsert',content_type='multipart/form-data', data=dados)
        assert response2.status_code == 200
        assert app.json.loads(response2.data.decode('utf-8'))['resposta'] =='Ativo Gravado com Sucesso'
        response3 = client.post('/Boletador/Ativo/Load',content_type='multipart/form-data', data=dados)
        assert response3.status_code == 200
        assert app.json.loads(response3.data.decode('utf-8'))['resposta'] =='Ok'
        response4 = client.post('/Boletador/Ativo/Delete',content_type='multipart/form-data', data=dados)
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
        dados['DataIni'] = '2000-01-01'
        dados['DataFim'] = app.tkdtm.hoje

        generic_object = cl_Mov(**{})
        generic_object.get_sample()      
        generic_object.get()
        dados['idEstrategia'] = generic_object.idEstrategia
        dados['idTrader'] = generic_object.idTrader
        dados['CGC'] = generic_object.CGC

        responsesearch = client.post('/Boletador/Ativo/Search',content_type='multipart/form-data', data=dados)
        assert responsesearch.status_code == 200
        assert app.json.loads(responsesearch.data.decode('utf-8'))['resposta'] == 'Ok'

        
        
    

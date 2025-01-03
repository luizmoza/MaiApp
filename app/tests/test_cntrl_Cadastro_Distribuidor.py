import pytest
from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Distribuidor import cl_Distribuidor

class TestCntrlDistribuidor:
    
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
        generic_object = cl_Distribuidor(**{})
        guid = app.tk.generate_guid()

        generic_object.Nome = guid
        generic_object.CGC = guid
        generic_object.RazaoSocial = guid
        
        dados = {}
        for k,v in app.tk.ParseNewObjectDict(generic_object).items(): dados[k] = v
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        response1 = client.post('/Cadastro/Distribuidor/Insert',content_type='multipart/form-data', data=dados)
        assert response1.status_code == 200
        assert app.json.loads(response1.data.decode('utf-8'))['resposta'] =='Distribuidor Gravado com Sucesso'
        generic_object.Alias = guid
        generic_object.get_id_by_Nome()
        dados = {}
        for k,v in app.tk.ParseObjectDict(generic_object).items(): dados[k] = v
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        response2 = client.post('/Cadastro/Distribuidor/Update',content_type='multipart/form-data', data=dados)
        assert response2.status_code == 200
        assert app.json.loads(response2.data.decode('utf-8'))['resposta'] =='Distribuidor Gravado com Sucesso'
        response3 = client.post('/Cadastro/Distribuidor/Load',content_type='multipart/form-data', data=dados)
        assert response3.status_code == 200
        assert app.json.loads(response3.data.decode('utf-8'))['resposta'] =='Ok'
        response4 = client.post('/Cadastro/Distribuidor/Delete',content_type='multipart/form-data', data=dados)
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
        responsesearch = client.post('/Cadastro/Distribuidor/Search',content_type='multipart/form-data', data=dados)
        assert responsesearch.status_code == 200
        assert app.json.loads(responsesearch.data.decode('utf-8'))['resposta'] == 'Ok'

        
        
    

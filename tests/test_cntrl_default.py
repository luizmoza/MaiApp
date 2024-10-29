import pytest
from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_RV import cl_RV

class TestCntrlDefault:
    
    @pytest.fixture()
    def test_object(self):
        Usuario = cl_Usuario(**{})
        Usuario.idUsuario = app.test_idUsuario
        Usuario.get()
        return Usuario

    @pytest.fixture()
    def client(self): return app.test_client() 
    
    @pytest.mark.REQUEST
    def test_index_route(self,client):
       assert client.get('/').status_code == 200
    
    @pytest.mark.LOADERS
    def test_request_setup_search(self,test_object,client):
        dados = {}
        dados['Email'] = test_object.Email
        dados['Senha'] = test_object.Senha
        responsesearch = client.post('/ValidaUsuarioLogin',content_type='multipart/form-data', data=dados)
        assert responsesearch.status_code == 200
        assert app.json.loads(responsesearch.data.decode('utf-8'))['resposta'] == "Usuario Validado"

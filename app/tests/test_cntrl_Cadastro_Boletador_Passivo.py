import pytest
from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Passivo import cl_Passivo

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
        generic_object = cl_Passivo(**{})
        guid = app.tk.generate_guid()

        generic_object.idCodRefCotistaFundo = '1'
        generic_object.idFundo = '1'
        generic_object.Tipo = ''
        generic_object.QtdCotas = '0'
        generic_object.Fin = '0'
        generic_object.DataMovimentacao = "2024-01-01"
        generic_object.Aprovador = guid

        generic_object.get_sample_fk()      
         
        dados = {}
        for k,v in app.tk.ParseNewObjectDict(generic_object).items(): dados[k] = v
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        response1 = client.post('/Boletador/Passivo/Insert',content_type='multipart/form-data', data=dados)
        assert response1.status_code == 200
        assert app.json.loads(response1.data.decode('utf-8'))['resposta'] =='Passivo Gravado com Sucesso'
        generic_object.Alias = guid
        generic_object.get_id_Aprovador()
        dados = {}
        for k,v in app.tk.ParseObjectDict(generic_object).items(): dados[k] = v
        dados['idUsuario'] = test_object.idUsuario
        dados['UsuarioEmail'] = test_object.Email
        dados['UsuarioAuth'] = test_object.ChaveTrocaSenha
        response3 = client.post('/Boletador/Passivo/Load',content_type='multipart/form-data', data=dados)
        assert response3.status_code == 200
        assert app.json.loads(response3.data.decode('utf-8'))['resposta'] =='Ok'
        response4 = client.post('/Boletador/Passivo/Delete',content_type='multipart/form-data', data=dados)
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
        dados['Tipo'] = ''
        responsesearch = client.post('/Boletador/Passivo/Search',content_type='multipart/form-data', data=dados)
        assert responsesearch.status_code == 200
        assert app.json.loads(responsesearch.data.decode('utf-8'))['resposta'] == 'Ok'

        
        
    

import sys
sys.path.append(r"../")
from app import app
import warnings
warnings.filterwarnings("ignore")

from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_Mov import cl_Mov
from app.classes.cl_Fundo import cl_Fundo

client = app.test_client() 


Usuario = cl_Usuario(**{})
Usuario.idUsuario = app.test_idUsuario
Usuario.get()
test_object = Usuario

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

import sys
sys.path.append(r"../")
from app import app

from app.classes.cl_Apontamento import cl_Apontamento
test_object = cl_Apontamento(**{})

test_unics = test_object.__unics__
test_nn = test_object.__nn__
test_nnbl = test_object.__nnbl__
test_nnint = test_object.__nnint__
test_nndbl = test_object.__nndbl__
test_nndt = test_object.__nndt__
test_pk = test_object.__pk__
test_unics = test_object.__unics__

for key in test_nn:setattr(test_object, key, app.tk.generate_guid())
for key in test_nnbl:setattr(test_object, key, False)
for key in test_nnint:setattr(test_object, key, 0)
for key in test_nndbl:setattr(test_object, key, 0)
for key in test_nndt:setattr(test_object, key, app.tkdtm.hoje)
for key in test_unics:setattr(test_object, key, app.tk.generate_guid())
vv0 = test_object.get_sample_fk()

print('Criando: ' + str(test_object.__dict__))
#vv1 = test_object.insert()
# id = getattr(test_object, test_pk[0])
# for key in test_unics:setattr(test_object, key, app.tk.generate_guid())

# setattr(test_object, 'CGC', '@#Teste2#@')

# vv2 = test_object.__db__.statusquery == 'Inserted successfully'
# dictaux = app.tk.ParseNewObjectDict(test_object)
# dict = {}
# for k,value in dictaux.items():
#     dict[k] = [value]
# print('Bulking: ' + str(dict))
# vv3 = test_object.bulk(app.pd.DataFrame.from_dict({'ERRO#':[0]}))
# for key in test_unics:setattr(test_object, key, app.tk.generate_guid())
# vv6 = test_object.bulk(app.pd.DataFrame.from_dict(dict))
# print('Deletando: ' + str(id))
# print('Deletando: ' + str(id+1))
# vv4 = test_object.delete(id)
# vv5 = test_object.delete(id+1)
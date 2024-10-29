import sys
import warnings
warnings.filterwarnings("ignore")
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

print()
Teste1 = app.tk.generate_guid()
Teste2 = app.tk.generate_guid()
for key in test_nn:setattr(test_object, key, Teste1)
for key in test_nnbl:setattr(test_object, key, False)
for key in test_nnint:setattr(test_object, key, 0)
for key in test_nndbl:setattr(test_object, key, 0)
for key in test_nndt:setattr(test_object, key, app.tkdtm.hoje)
for key in test_unics:setattr(test_object, key, Teste1)
vv0 = test_object.get_sample_fk()
print('Criando: ' + str(test_object.__dict__))
vv1 = test_object.insert()
vv2 = test_object.__db__.statusquery == 'Inserted successfully'
id = getattr(test_object, test_pk[0])
test_object = test_object.__class__(**{})
setattr(test_object, test_pk[0], id)



vv3 = test_object.get()


vv4 = test_object.__db__.statusquery == 'Executed'
vv5 = True
for key in test_nn: 
    if key not in test_unics: 
        if getattr(test_object, key) != Teste1: vv5 = False
for key in test_nnbl: 
    if key not in test_unics:     
        if getattr(test_object, key) != False: vv5 = False
for key in test_nnint: 
    if key not in test_unics: 
        if getattr(test_object, key) != 0: vv5 = False
for key in test_nndbl:
    if key not in test_unics: 
        if getattr(test_object, key) != 0: vv5 = False
for key in test_nndt: 
    if key not in test_unics: 
        if app.pd.to_datetime(getattr(test_object, key)) != app.pd.to_datetime(app.tkdtm.hoje): vv5 = False

        
        
for key in test_nn:setattr(test_object, key, Teste2)
for key in test_nnbl:setattr(test_object, key, True)
for key in test_nndbl:setattr(test_object, key, 1)
for key in test_nnint:setattr(test_object, key, 1)
for key in test_nndt:setattr(test_object, key, app.tkdtm.D_1)
for key in test_unics:setattr(test_object, key, Teste2)
vv0 = test_object.get_sample_fk()
print('Alterando: ' + str(test_object.__dict__))
vv6 = test_object.set()
vv7 = test_object.__db__.statusquery == 'Updated successfully'
id = getattr(test_object, test_pk[0])
test_object = test_object.__class__(**{})
setattr(test_object, test_pk[0], id)
vv8 = test_object.get()
vv9 = test_object.__db__.statusquery == 'Executed'
vv10 = True
for key in test_nn: 
    if key not in test_unics: 
        if getattr(test_object, key) != Teste2: vv10 = False
for key in test_nnbl: 
    if key not in test_unics:     
        if getattr(test_object, key) != True: vv10 = False
for key in test_nnint: 
    if key not in test_unics: 
        if getattr(test_object, key) != 1: vv10 = False
for key in test_nndbl:
    if key not in test_unics: 
        if getattr(test_object, key) != 1: vv10 = False
for key in test_nndt: 
    if key not in test_unics: 
        if app.pd.to_datetime(getattr(test_object, key)) != app.pd.to_datetime(app.tkdtm.D_1): vv5 = False
print('Deletando: ' + str(test_object.__dict__))
vv11 = test_object.remove()
vv12 = test_object.__db__.statusquery == 'Deleted successfully'
assert vv1 and vv2 and vv3 and vv4 and vv5 and vv6 and vv7 and vv8 and vv9 and vv10 and vv11 and vv12
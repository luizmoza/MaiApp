from app import app


from app.classes.cl_Opcao import cl_Opcao
import pytest


#Com prints
#python -m pytest -v -s
#Sem prints
#python -m pytest -v

class TestOpcao:

    @pytest.fixture()
    def test_object(self):return cl_Opcao(**{})
    @pytest.fixture()
    def test_unics(self,test_object): 
        if hasattr(test_object, '__unics__'): 
            return test_object.__unics__
        else:
            return []

    @pytest.fixture()
    def test_nn(self,test_object):
        if hasattr(test_object, '__nn__'): 
            return test_object.__nn__
        else:
            return []

    @pytest.fixture()
    def test_nnbl(self,test_object):
        if hasattr(test_object, '__nnbl__'): 
            return test_object.__nnbl__
        else:
            return []

    @pytest.fixture()
    def test_nndbl(self,test_object):
        if hasattr(test_object, '__nndbl__'): 
            return test_object.__nndbl__
        else:
            return []

    @pytest.fixture()
    def test_nndt(self,test_object):
        if hasattr(test_object, '__nndt__'): 
            return test_object.__nndt__
        else:
            return []

    @pytest.fixture()
    def test_nnint(self,test_object):
        if hasattr(test_object, '__nnint__'): 
            return test_object.__nnint__
        else:
            return []
        
    @pytest.fixture()
    def test_pk(self,test_object):
        if hasattr(test_object, '__pk__'): 
            return test_object.__pk__
        else:
            return []

    @pytest.fixture()
    def test_unics(self,test_object):
        if hasattr(test_object, '__unics__'): 
            return test_object.__unics__
        else:
            return []
        
    
    @pytest.mark.CRUD
    @pytest.mark.skipif(app.enviroment == 'prd',reason="isolamento")
    def test_crud_cycle1(self,test_object,test_nn,test_nnbl,test_nnint,test_nndbl,test_nndt,test_pk,test_unics):
        if len(test_pk)==1:
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
                    if app.pd.to_datetime(getattr(test_object, key)) != app.pd.to_datetime(app.tkdtm.D_1): vv10 = False
                    
            print('Deletando: ' + str(test_object.__dict__))
            vv11 = test_object.remove()
            vv12 = test_object.__db__.statusquery == 'Deleted successfully'
            assert vv1 and vv2 and vv3 and vv4 and vv5 and vv6 and vv7 and vv8 and vv9 and vv10 and vv11 and vv12
        else:
            assert True
                
    @pytest.mark.CRUD
    @pytest.mark.skipif(app.enviroment == 'prd',reason="isolamento")
    def test_crud_cycle2(self,test_object,test_nn,test_nnbl,test_nndbl,test_nndt,test_nnint,test_pk,test_unics):
        if len(test_pk)==1:
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
            vv1 = test_object.create(test_object.__dict__)
            vv2 = test_object.__db__.statusquery == 'Inserted successfully'
            id = getattr(test_object, test_pk[0])
            test_object = test_object.__class__(**{})
            setattr(test_object, test_pk[0], id)
            vv3 = test_object.read(id)
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
            vv6 = test_object.update(id,app.tk.ParseNewObjectDict(test_object))
            vv7 = test_object.__db__.statusquery == 'Updated successfully'
            id = getattr(test_object, test_pk[0])
            test_object = test_object.__class__(**{})
            setattr(test_object, test_pk[0], id)
            vv8 = test_object.read(id)
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
                    if app.pd.to_datetime(getattr(test_object, key)) != app.pd.to_datetime(app.tkdtm.D_1): vv10 = False
                    
            print('Deletando: ' + str(test_object.__dict__))
            vv11 = test_object.remove()
            vv12 = test_object.__db__.statusquery == 'Deleted successfully'
            assert vv1 and vv2 and vv3 and vv4 and vv5 and vv6 and vv7 and vv8 and vv9 and vv10 and vv11 and vv12
        else:
            assert True


    @pytest.mark.CRUD
    @pytest.mark.skipif(app.enviroment == 'prd',reason="isolamento")
    def test_crud_bulk(self,test_object,test_nn,test_nnbl,test_nndbl,test_nndt,test_nnint,test_pk,test_unics):
        if len(test_pk)==1:
            print()
            for key in test_nn:setattr(test_object, key, '@#Teste1#@')
            for key in test_nnbl:setattr(test_object, key, False)
            for key in test_nnint:setattr(test_object, key, 0)
            for key in test_nndbl:setattr(test_object, key, 0)
            for key in test_nndt:setattr(test_object, key, app.tkdtm.hoje)
            for key in test_unics:setattr(test_object, key, app.tk.generate_guid())
            vv0 = test_object.get_sample_fk()
            
            print('Criando: ' + str(test_object.__dict__))
            vv1 = test_object.insert()
            id = getattr(test_object, test_pk[0])
            for key in test_unics:setattr(test_object, key, app.tk.generate_guid())
            vv2 = test_object.__db__.statusquery == 'Inserted successfully'
            dictaux = app.tk.ParseNewObjectDict(test_object)
            dict = {}
            for k,value in dictaux.items():
                dict[k] = [value]
            print('Bulking: ' + str(dict))
            vv3 = test_object.bulk(app.pd.DataFrame.from_dict({'ERRO#':[0]}))
            for key in test_unics:setattr(test_object, key, app.tk.generate_guid())
            vv6 = test_object.bulk(app.pd.DataFrame.from_dict(dict))
            print('Deletando: ' + str(id))
            print('Deletando: ' + str(id+1))
            vv4 = test_object.delete(id)
            vv5 = test_object.delete(id+1)
            assert vv1 and vv2 and vv3==False and vv4 and vv5 and vv6
        else:
            assert True

    @pytest.mark.CRUD
    @pytest.mark.skipif(app.enviroment == 'prd',reason="isolamento")
    def test_crud_sessionbreak_1(self,test_object,test_nn,test_nnbl,test_nndbl,test_nndt,test_nnint,test_pk,test_unics):
        if len(test_pk)==1:
            print()
            for key in test_nn:setattr(test_object, key, '@#Teste1#@')
            for key in test_nnbl:setattr(test_object, key, False)
            for key in test_nnint:setattr(test_object, key, 0)            
            for key in test_nndbl:setattr(test_object, key, 0)
            for key in test_nndt:setattr(test_object, key, app.tkdtm.hoje)
            for key in test_unics:setattr(test_object, key, app.tk.generate_guid())
            vv0 = test_object.get_sample_fk()
            
            print('Criando: ' + str(test_object.__dict__))
            test_object.__db__.session = None 
            vv1 = test_object.insert()
            test_object.__db__.Session_Start()
            vv2 = test_object.insert()
            test_object.__db__.session = None 
            vv3 = test_object.set()
            test_object.__db__.Session_Start()
            vv4 = test_object.set()
            test_object.__db__.session = None 
            vv5 = test_object.remove()
            test_object.__db__.Session_Start()
            vv6 = test_object.remove()
            assert  vv1 == False and vv2 and vv3 == False and vv4 and vv5 == False and vv6
        else:
            assert True

    @pytest.mark.CRUD
    @pytest.mark.skipif(app.enviroment == 'prd',reason="isolamento")
    def test_crud_sessionbreak_2(self,test_object,test_nn,test_nnbl,test_nndbl,test_nndt,test_nnint,test_pk,test_unics):
        if len(test_pk)==1:
            print()
            for key in test_nn:setattr(test_object, key, '@#Teste1#@')
            for key in test_nnbl:setattr(test_object, key, False)
            for key in test_nnint:setattr(test_object, key, 0)            
            for key in test_nndbl:setattr(test_object, key, 0)
            for key in test_nndt:setattr(test_object, key, app.tkdtm.hoje)
            for key in test_unics:setattr(test_object, key, app.tk.generate_guid())
            vv0 = test_object.get_sample_fk()
            
            print('Criando: ' + str(test_object.__dict__))
            test_object.__db__.session = None 
            vv1 = test_object.create(test_object.__dict__)
            test_object.__db__.Session_Start()
            vv2 = test_object.create(test_object.__dict__)
            id = getattr(test_object, test_pk[0])
            test_object.__db__.session = None 
            vv3 = test_object.update(id,app.tk.ParseNewObjectDict(test_object))
            test_object.__db__.Session_Start()
            vv4 = test_object.update(id,app.tk.ParseNewObjectDict(test_object))
            test_object.__db__.session = None 
            vv5 = test_object.delete(id)
            test_object.__db__.Session_Start()
            vv6 = test_object.delete(id)
            assert  vv1 == False and vv2 and vv3 == False and vv4 and vv5 == False and vv6
        else:
            assert True
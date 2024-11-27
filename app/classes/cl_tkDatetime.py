from app import app


class cl_tkDatetime:
    def __init__(self):
        self.server_path = 'localhost:5000'
        self.db = app.db
        self.Feriados = self.load_dict_feriados()
        self.hoje = app.dt.strptime(app.dt.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
        self.D0 = self.date_after_work_days(self.date_after_work_days(self.hoje,-1),1)
        self.D_1 = self.date_after_work_days(self.hoje,-1)

    def load_dict_feriados(self):
            myQuery = """ select * from Feriado """
            return app.pd.read_sql_query(myQuery, self.db.engine)
                
    def is_holiday(self,Data,Tipo='Anbima'):
        if len(self.Feriados[self.Feriados['Tipo']==Tipo]) == 0:
            self.Feriados = self.load_dict_feriados()
            self.Feriados = self.Feriados[self.Feriados['Tipo']==Tipo]
        if type(Data) == type(app.dt.now()):
            if len(self.Feriados[self.Feriados['Data'] == app.pd.to_datetime(app.dt.strptime(Data.strftime('%Y-%m-%d'),'%Y-%m-%d')) ])>0: return True  
            else: return False
        elif len(Data)>1:
            df = app.pd.DataFrame(app.pd.Series(Data, name='Data'))
            df['Data']= app.pd.to_datetime(df['Data'],errors='coerce')
            df["InList"] = Data.isin(self.Feriados['Data'])
            return df["InList"]

    def date_after_work_days(self,Data,Dias,Tipo='Anbima'):
        i=0
        if isinstance(Data, app.pd.core.series.Series)==False:
            if isinstance(Data, str): Data = app.dt.strptime(Data, '%Y-%m-%d')
            if Dias == 0: return Data
            if type(Data) == type(app.dt.now()) :
                Sinal = Dias / abs(Dias)
                while abs(Dias) > 0:
                    DataAux = Data + app.timedelta(days=Sinal)
                    if DataAux.weekday() != 5 and DataAux.weekday() != 6 and self.is_holiday(DataAux,Tipo) == False: Dias = Dias - (Sinal * 1)
                    Data = Data + app.timedelta(days=Sinal)  
                return Data  
        else:
            if len(Data)>1:
                df = Data.to_frame("Data").copy()
                df['Dias'] = Dias 
                Sinal = Dias / abs(Dias)
                while abs(df['Dias'].sum()) > 0:
                    if i>100: app.sys.exit("Error message")
                    i=i+1
                    df.loc[df['Dias'] != 0, 'Data'] =  df['Data'] + app.timedelta(days=Sinal)
                    df.loc[df['Dias'] != 0, 'Dias'] =  df['Dias'] - (Sinal * 1)
                    df['day_of_week'] = df["Data"].dt.day_name()                                       
                    df.loc[df['day_of_week'] == 'Saturday', 'Sabado'] = True 
                    df.loc[df['day_of_week'] == 'Sunday', 'Domingo'] = True 
                    df.loc[self.is_holiday(df['Data'],Tipo) == True, 'Feriado'] = True 
                    df.loc[df['day_of_week'] != 'Saturday', 'Sabado'] = False 
                    df.loc[df['day_of_week'] != 'Sunday', 'Domingo'] = False
                    df.loc[self.is_holiday(df['Data'],Tipo) != True, 'Feriado'] = False 
                    df.loc[df['Sabado'] | df['Domingo'] | df['Feriado'], 'Dias'] = df['Dias'] + (Sinal * 1)
                return df["Data"]  


    def net_work_day(self,dataini,datafim):
        dataini = self.date_after_work_days(dataini,0)
        i=0
        while dataini<=datafim:
            i=i+1
            dataini = self.date_after_work_days(dataini,1)
        return i


    def backfoward_wd(self,data): return self.date_after_work_days(self.date_after_work_days(data,-1),1)
    def fowardback_wd(self,data): return self.date_after_work_days(self.date_after_work_days(data,1),-1)
    

    def last_workday_last_month(self,data):
        mes = int(data.strftime('%m'))
        ano = int(data.strftime('%Y'))
        return self.date_after_work_days(app.dt.strptime("01/" + app.tkstr.right('0'+str(mes),2) + "/" + str(ano), '%d/%m/%Y'), -1)

    def last_workday_month(self,data):
        mes = int(data.strftime('%m'))
        ano = int(data.strftime('%Y'))
        if mes == 12:
            mes = 1
            ano = ano +1
        else:
            mes = mes +1
        return self.date_after_work_days(app.dt.strptime("01/" + app.tkstr.right('0'+str(mes),2) + "/" + str(ano), '%d/%m/%Y'), -1)

    def first_workday_last_month(self,data):
        mes = int(data.strftime('%m'))
        ano = int(data.strftime('%Y'))
        if mes == 1:
            mes = 12
            ano = ano - 1
        else:
            mes = mes - 1
        return self.date_after_work_days(self.date_after_work_days(app.dt.strptime("01/" + app.tkstr.right('0'+str(mes),2) + "/" + str(ano), '%d/%m/%Y'), -1),1)

    def last_workday_year(self,data):
        ano = int(data.strftime('%Y'))
        return self.date_after_work_days(self.date_after_work_days(app.dt.strptime("31/12/" + str(ano), '%d/%m/%Y'), 1),-1)

    def first_workday_year(self,data):
        ano = int(data.strftime('%Y'))
        return self.date_after_work_days(self.date_after_work_days(app.dt.strptime("01/01/" + str(ano), '%d/%m/%Y'), -1), 1)   

    def first_workday_month(self,data):
        mes = int(data.strftime('%m'))
        ano = int(data.strftime('%Y'))
        return self.date_after_work_days(self.date_after_work_days(app.dt.strptime("01/" + app.tkstr.right('0'+str(mes),2) + "/" + str(ano), '%d/%m/%Y'), -1), 1)


    def is_valid_date(self,dia,mes,ano):
        try:
            newDate = app.dt(ano,mes,dia)
            return  True
        except ValueError:
            return  False

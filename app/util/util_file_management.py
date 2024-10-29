from app import app

class util_file_management:
    def file_exists(fname):
        return app.os.path.isfile(fname)
    def create_directory_if_not_exists(fname):
        app.pathlib(fname).mkdir(parents=True, exist_ok=True)
        return True
    def delete_file(fname):
        app.os.remove(fname)
    def export_df_to_csv_in_desktop(df):
        root = r'C:\Users'
        root = root + '\\' + app.os.getlogin()
        root = root + '\Desktop\export_dataframe.xlsx'
        df.to_csv (root, index = False, header=True,sep=';',decimal=',')
    def export_df_to_xlsx_in_desktop(df):
        root = r'C:\Users'
        root = root + '\\' + app.os.getlogin()
        root = root + '\Desktop\export_dataframe.xlsx'
        df.to_excel(root,index=False, sheet_name='export_dataframe', engine='xlsxwriter')
    def export_xml_without_enconding(Caminho,XmlTree): #Montar XML FAST SEM ENCODING PYTON
        with open(Caminho,"wb") as f: f.write(app.ET.tostring(XmlTree)) #XmlTree = ET.fromstring(XmlTreeString) #EX: Caminho = '.\\Extratos\ExtratoD1.xml'
        return True
    def export_xml_with_encoding(Caminho,XmlTree): #Montar XML FAST SEM ENCODING PYTON
        app.ET.ElementTree(XmlTree).write(Caminho,encoding="UTF-8",xml_declaration=True) #EX: '.\\Extratos\ExtratoD1.xml' #XmlTree = ET.fromstring(XmlTreeString)
        return True
    def last_modified_date_file(paths):
        return app.os.path.getmtime(paths)
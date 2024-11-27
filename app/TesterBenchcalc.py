import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.append(r"../")
from app import app

a = app.tk.CalculaIndiceAcumuladoFormula('BenchComposto(Ibovespa;100%;0)',app.dt.strptime('2024-10-31','%Y-%m-%d'),app.dt.strptime('2024-10-31','%Y-%m-%d'))
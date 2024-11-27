import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.append(r"../")
from app import app


D_1 = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
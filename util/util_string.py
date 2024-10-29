import datetime

class util_string:
    def left(s, amount): return s[:amount]
    def right(s, amount): return s[-amount:]
    def trim(s): return s.strip()  
    def mid(s, offset, amount):return s[offset:offset+amount]
    
    def Left(s, amount): return s[:amount]
    def Right(s, amount): return s[-amount:]

    def Instr( start, s, find):
        ret = s.find(find, start)
        if ret == -1:
            return 0
        else:
            return ret

    def Len(s):
        return len(s)

    def FormatCur( s):
        if not isinstance(s, (int, float)):
            s = float(s)
        return f"R${s:.2f}"

    def FormatPerc( s):
        if not isinstance(s, (int, float)):
            s = float(s)
        return f"{s * 100:.5f}%"

    def FormatFloatSql( s):
        if not isinstance(s, (int, float)):
            s = float(s)
        return f"R${s:.2f}"

    def ForceString( s):
        if isinstance(s, datetime.datetime):
            return s.strftime('%Y%m%d')
        else:
            return s

    def Isdate( s):
        try:
            datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False
    
    def clean_time_zone(mytime):
        try:
            mytime = str(mytime).split(".")[0]
        except ValueError:
            mytime = str(mytime).split(" ")[0] + " " + str(mytime).split(" ")[1]
            return mytime    
        
    def real_br_money_mask(my_value):
        a = 'R${:,.2f}'.format(float(my_value))
        b = a.replace(',','v')
        c = b.replace('.',',')
        return c.replace('v','.')  

    def brl_float_string_to_db(my_value):
        c = my_value.replace('.','')
        d = c.replace(',','.')
        return d.replace('v','.')  
    
    def real_br_perc_mask(my_value):
        a = '{:,.4f}%'.format(float(my_value)*100)
        b = a.replace(',','v')
        c = b.replace('.',',')
        if c[:3] == 'nan': return '0%'
        return c.replace('v','.')
    
    def month_by_number(v):
        if int(v) == int(1): return 'Jan'
        if int(v) == int(2): return 'Fev'
        if int(v) == int(3): return 'Mar'
        if int(v) == int(4): return 'Abr'
        if int(v) == int(5): return 'Mai'
        if int(v) == int(6): return 'Jun'
        if int(v) == int(7): return 'Jul'
        if int(v) == int(8): return 'Ago'
        if int(v) == int(9): return 'Set'
        if int(v) == int(10): return 'Out'
        if int(v) == int(11): return 'Nov'
        if int(v) == int(12): return 'Dez'
        return ''
    
    def strtobool (val):
        """Convert a string representation of truth to true (1) or false (0).
        True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
        are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
        'val' is anything else.
        """
        val = val.lower()
        if val in ('y', 'yes', 't', 'true', 'on', '1'):
            return 1
        elif val in ('n', 'no', 'f', 'false', 'off', '0'):
            return 0
        else:
            raise ValueError("invalid truth value %r" % (val,))
        
    def ValidDate (app,data):
        try:
            data = app.dt.strptime(data,'%Y-%m-%d')
            return True
        except:
            return False
    
    def FormatdfCNPJCol(df,col):
        df[col] = df[col].apply(lambda x: f'{x:.0f}')
        df[col] = '00000' + df[col]
        df[col] = df[col].str[-14:]
        return df.copy()
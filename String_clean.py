
from unidecode import unidecode
import unicodedata
from non_nfkd_map import NON_NFKD_MAP


def upper_string(df,col:str):
    df[col+'_regex']=df[col+'_regex'].astype(str).str.upper()


def title_string(df,col:str):
    df[col+'_regex']=df[col+'_regex'].astype(str).str.title()


def lower_string(df,col:str):
    df[col+'_regex']=df[col+'_regex'].astype(str).str.lower()    


def partition_str_com(df,col:str):
    df[col+'_regex']=df[col+'_regex'].astype(str).str.partition(',')[0]

def take_out_crop(df,col:str):
    take_out_Corporation=['company', 'incorporated', 'corporation', 'corp.', 'corp', 'inc','inc',      
    '& co.', '& co', 'inc.', 's.p.a.', 'n.v.', 'a.g.', 'ag', 'nuf', 's.a.', 's.f.',      
    'oao', 'co.', 'co','kabushiki kaisha','kk','k.k.','k.k']

    df[col+'_regex']=df[col+'_regex'].apply(lambda words:' '.join(word for word in str(words).split() if word not in take_out_Corporation))

def take_out_simply(df,col:str):
    df[col+'_regex']=df[col+'_regex'].replace('[^A-Za-z0-9]+',' ',regex=True)

def tran_unidecode(df,col:str):
    for i in range(0,len(df[col])):
        df[col+'_regex'] = [unidecode(x) for x in df[col+'_regex'][i].values]

def remove_accents(t):
    """based on https://stackoverflow.com/a/51230541"""
    nfkd_form = unicodedata.normalize('NFKD', t.casefold())
    return ''.join(
        NON_NFKD_MAP[c]
            if c in NON_NFKD_MAP
        else c
            for part in nfkd_form for c in part
            if unicodedata.category(part) != 'Mn'
        )





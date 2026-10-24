import math

def number(x, minimum=None, maximum=None):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x): raise ValueError('finite_number')
    if minimum is not None and x<minimum: raise ValueError('minimum')
    if maximum is not None and x>maximum: raise ValueError('maximum')
    return x

def integer(x, minimum=None, maximum=None):
    if isinstance(x,bool) or not isinstance(x,int): raise ValueError('integer')
    return number(x,minimum,maximum)

def identifier(x):
    if not isinstance(x,str) or not x.strip() or len(x)>200: raise ValueError('identifier')
    return x

def unique_ids(rows, key='id'):
    ids=[identifier(r[key]) for r in rows]
    if len(ids)!=len(set(ids)): raise ValueError('duplicate_id')
    return ids

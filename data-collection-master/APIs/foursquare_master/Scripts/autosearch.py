from api import venues_by_cityname
import json, re, os, random
from tqdm import tqdm

# how filenames were generated:
# 1. lowercase
# 2. (re) nonletters -> underscores
# 3. (re) multiple underscores -> single underscore

r_prefix = 'cache/'
w_prefix = 'cache/results/'

def pick_next():
    names = os.listdir(r_prefix)
    names.remove('results')
    return None if len(names) == 0 else random.choice(names)

def retrieve_q(fn):
    with open(fn, 'r') as fp:
        return fp.read()

def store_results(fn, ids):
    msg = 'invalid city name' if ids is None else '\n'.join(ids)
    with open(fn, 'w') as fp:
        fp.write(msg)

def check_off_list(fn):
    os.remove(fn)



def one_it(r_fn, w_fn):
    city = retrieve_q(r_fn)
    venues = venues_by_cityname(city)
    store_results(w_fn, venues)
    check_off_list(r_fn)

class VenueLookupIterator:
    def __iter__(self):
        return self
    def __next__(self):
        fn = pick_next()
        if fn is None:
            raise StopIteration
        else:
            r_fn = r_prefix + fn
            w_fn = w_prefix + fn
            try:
                one_it(r_fn, w_fn)
            except IsADirectoryError:
                print(f'No file name :: {str(fn)} <{type(fn)}>')

list(tqdm(VenueLookupIterator()))
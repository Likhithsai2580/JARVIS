from functools import lru_cache
import time
import languagemodels as lm

@lru_cache(maxsize=128)  # Adjust maxsize according to your memory constraints
def locallm(q):
    return lm.do(q)

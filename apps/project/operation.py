from .models import *

def pourcent(m):
    comp  = m.objects.filter(ok = 'True').count()
    total = m.objects.all().count()
    if comp == 0 or total == 0:
        p = 0
    else:
        p = "{:.2f}".format((100*comp)/total)
    
    print(comp, total, p)
    return p


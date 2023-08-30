ta = ('agence','appelant','nom','priorite','description','etat','date_debut','technicient',)
l = []
def tbb(fi):
    l.append(AjaxDatatableView.render_row_tools_column_def())
    for f in fi:
        t ={'name':f,'visible': True,}
        l.append(t)
    print(l)
    return l
tbb(ta)
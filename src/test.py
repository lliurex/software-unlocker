#!/usr/bin/env python3
from rebost import store
a=store.client()
a.disableFilters()
#a.restart()
print(a.execute("search","firefox"))

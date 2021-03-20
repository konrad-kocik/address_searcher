from nicelka import GoogleSearcher, KrkgwSearcher

kola = KrkgwSearcher()
kola.search()

google = GoogleSearcher(allow_indirect_matches=True)
google.search()

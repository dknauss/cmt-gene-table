import csv,json,os,urllib.request,urllib.parse,time
S=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','cache'); os.makedirs(S,exist_ok=True)
B='https://api-v3.monarchinitiative.org/v3/api'
def get(url,fn):
    p=os.path.join(S,fn)
    if os.path.exists(p): return json.load(open(p))
    for a in range(6):
        try:
            d=json.load(urllib.request.urlopen(url,timeout=60)); json.dump(d,open(p,'w')); return d
        except Exception as e:
            if getattr(e,'code',0) in range(400,500) and e.code!=429: raise SystemExit('fail (client error, not retrying) '+url+' '+str(e))
            print('retry',url,e); time.sleep(5*2**a)
    raise SystemExit('fail '+url)
rows=list(csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','clingen-cmt.csv'))))
mondos=set()
for r in rows:
    h=r['hgnc_id']
    for cat in ['Causal','Correlated']:
        d=get(f"{B}/association?subject={h}&category=biolink:{cat}GeneToDiseaseAssociation&limit=500",f"{h.replace(':','_')}_{cat}.json")
        for i in d['items']: mondos.add(i['object'])
    mondos.add(r['mondo_id'])
print(len(mondos))
for m in sorted(mondos):
    if m.startswith('MONDO:'): get(f"{B}/entity/{m}",f"ent_{m.replace(':','_')}.json")

import csv,json,re,collections
import os
S=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','cache')+os.sep
A='https://api-v3.monarchinitiative.org/v3/api/association?subject={}&category=biolink:{}GeneToDiseaseAssociation&limit=500'
ent=lambda m: json.load(open(S+'ent_'+m.replace(':','_')+'.json'))
def L(x): return x.upper()
def roman(s):
    r={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8}
    return str(r.get(s,s))
def convert(name, exact, related):
    """Return (list of short names, rule tag) or ([],None) if not a neuropathy subtype term."""
    n=name.strip().rstrip(';').strip()
    m=re.match(r'(?i)^(?:autosomal (?:dominant|recessive) )?Charcot-Marie-Tooth disease,? (?:(?:axonal|demyelinating),? )?(?:autosomal (?:dominant|recessive),? )?type (\w+)$',n)
    if m: return ['CMT'+L(m.group(1))],'CMT type'
    m=re.match(r'(?i)^Charcot-Marie-Tooth disease,? X-linked dominant (\d+)$',n)
    if m: return ['CMTX'+m.group(1)],'CMTX'
    m=re.match(r'(?i)^Charcot-Marie-Tooth disease,? (dominant|recessive) intermediate (\w)$',n)
    if m: return ['CMT'+('DI' if m.group(1).lower()=='dominant' else 'RI')+L(m.group(2))],'intermediate'
    m=re.match(r'(?i)^(?:hereditary sensory and autonomic neuropathy type|neuropathy, hereditary sensory and autonomic, type) (\w+)$',n)
    if m: return ['HSAN'+L(m.group(1))],'HSAN'
    m=re.match(r'(?i)^neuropathy, hereditary sensory, type (\w+)$',n)
    if m: return ['HSN'+L(m.group(1))],'HSN'
    m=re.match(r'(?i)^(?:hereditary motor and sensory neuropathy type|neuropathy, hereditary motor and sensory, type) (\w+)$',n)
    if m: return ['HMSN'+L(m.group(1))],'HMSN'
    m=re.match(r'(?i)^(?:neuronopathy, distal hereditary motor, type|distal hereditary motor neuropathy type) (\w+)$',n)
    if m: return ['dHMN'+L(m.group(1))],'dHMN type'
    m=re.match(r'(?i)^neuronopathy, distal hereditary motor, autosomal (dominant|recessive) (\d+)$',n)
    if m: return [('HMND' if m.group(1).lower()=='dominant' else 'HMNR')+m.group(2)],'dHMN AD/AR numbered (OMIM-style symbol)'
    if re.match(r'(?i)^hereditary neuropathy with liability to pressure palsies$',n): return ['HNPP'],'HNPP'
    if re.match(r'(?i)^Roussy-Levy syndrome$',n): return ['Roussy-Levy syndrome'],'eponym'
    m=re.match(r'(?i)^neuropathy, congenital hypomyelinating, (\d+)$',n)
    if m: return ['CHN'+m.group(1)],'CHN'
    # non-pattern primary names: accept exact synonyms of subtype form
    pat=re.compile(r'^(?:AR-|AR)?(?:CMT[0-9A-Z-]+|HSAN ?[0-9A-Z]+|HSN ?[0-9A-Z]+|HMSN ?[0-9A-Z]+|X-linked dHMN\d+|dHMN\d+[A-Z]?|SMARD1)$')
    syn=[s for s in exact if pat.match(s)]
    compact=[s for s in syn if ' ' not in s and not re.search(r'[IVX]{2,}$',s)]
    if compact: syn=compact
    if syn: return syn,'exact synonym'
    return [],None
EXTRA_SYN=re.compile(r'^(?:DSS|Dejerine-Sottas (?:syndrome|disease)|dHMN\d+[A-Z]?|X-linked dHMN\d+|SMARD1|dSMA\d+|HMN\d+[A-Z]?|HMNR\d+|DHMN\d+[A-Z]?|CMT[0-9A-Z]+)$')
GENERIC={'MONDO:0015626','MONDO:0018993','MONDO:0018995','MONDO:0018894','MONDO:0015364','MONDO:0020127','MONDO:0018776','MONDO:0015362'}
SPOT={
'PMP22':'consistent with expected CMT1A, CMT1E, HNPP, DSS/CMT3.',
'MPZ':'consistent with expected CMT1B, CMT2I, CMT2J, CMTDID, DSS, CHN.',
'MFN2':'REVIEW: MONDO names OMIM:609260 "type 2A2" (converted CMT2A2); the AD form is conventionally written CMT2A2A alongside AR CMT2A2B. Not overridden.',
'GJB1':'consistent with expected CMTX1.',
'GDAP1':'consistent with expected CMT4A, CMT2K, CMTRIA, CMT2H.',
'NEFL':'consistent with expected CMT1F, CMT2E, CMTDIG; CMT2B5 is an Orphanet-derived term (no OMIM xref).',
'SH3TC2':'consistent with expected CMT4C.',
'SBF2':'consistent with expected CMT4B2.',
'HSPB1':'consistent with expected CMT2F, dHMN2B.',
'SORD':'REVIEW: MONDO/OMIM classify SORD only as a distal HMN (HMNR8); SORD neuropathy is widely described as CMT2/dHMN in the literature but MONDO gives no lettered CMT designation. Not overridden.',
'SCN11A':'REVIEW: HSAN2D comes from correlated MONDO:0009459, a term usually tied to SCN9A; probably not a SCN11A subtype name.',
'FBLN5':'REVIEW: MONDO primary label "IIA 1H" looks malformed; CMT1H taken from its exact synonym.',
'HINT1':'REVIEW: ARCMT2-NM is an exact synonym of Gamstorp-Wohlfart syndrome (OMIM symbol NMAN, neuromyotonia and axonal neuropathy); not a conventional numbered CMT subtype.',
'KIF5A':'MONDO term is CMT2 (unlettered) due to KIF5A, Orphanet-derived; no subtype letter exists in MONDO.',
'SCO2':'MONDO term is AR axonal CMT (unlettered) due to copper metabolism defect, Orphanet-derived; no subtype letter in MONDO.',
'TRPV4':'consistent with expected CMT2C and AD congenital distal SMA (HMND8, related synonym HMN8); scapuloperoneal SMA left in notes.',
}
rows=list(csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','clingen-cmt.csv'))))
genes=collections.OrderedDict()
for r in rows: genes.setdefault(r['gene'],{'h':r['hgnc_id'],'cg':[]})['cg'].append(r['mondo_id'])
out=[];stats=collections.Counter()
for g,v in genes.items():
    h=v['h']; terms=collections.OrderedDict()
    for cat in ['Causal','Correlated']:
        for i in json.load(open(S+f"{h.replace(':','_')}_{cat}.json"))['items']:
            terms.setdefault(i['object'],set()).add(cat)
    for m in v['cg']: terms.setdefault(m,set()).add('ClinGen')
    recs=[];notes=[];nonneuro=[]
    for m,src in terms.items():
        if m in GENERIC: continue
        e=ent(m); nm=e['name']
        sh,rule=convert(nm,e.get('exact_synonym') or [],e.get('related_synonym') or [])
        if not sh:
            if re.search(r'(?i)neuropath|neuronopath|charcot|amyotroph|spinal muscular|nerve conduction',nm):
                notes.append(f'unconverted neuropathy-related MONDO term: {m} "{nm}"')
            else: nonneuro.append(nm)
            continue
        ex=e.get('exact_synonym') or []
        alts=[x for x in ex if re.match(r'^(dHMN\d+[A-Z]?|X-linked dHMN\d+|SMARD1|dSMA\d+)$',x)]
        if any('Dejerine-Sottas' in x for x in ex): alts.append('DSS')
        sup={x['id'] for x in e['node_hierarchy']['super_classes']}
        recs.append(dict(m=m,nm=nm,sh=sh+[a for a in alts if a not in sh],rule=rule,src=src,sup=sup,
            omim=[x for x in (e.get('xref') or []) if x.startswith('OMIM:')],rel=e.get('related_synonym') or []))
    allsup=set().union(*[r['sup'] for r in recs]) if recs else set()
    dropped=[r for r in recs if r['m'] in allsup and not r['omim']]
    recs=[r for r in recs if r not in dropped]
    if dropped: notes.append('dropped MONDO parent-group terms (no OMIM xref) in favour of their more specific subtypes: '+', '.join(f"{r['sh'][0]} ({r['m']})" for r in dropped))
    names=[];mon=[];omim=[];used_src=set()
    for r in recs:
        for x in r['sh']:
            if x not in names: names.append(x)
        mon.append(r['m']);omim+=r['omim'];used_src|=r['src']
        if r['rule']=='exact synonym': notes.append(f"{r['m']} \"{r['nm']}\" is not a subtype-pattern name; short form(s) taken from MONDO exact synonyms: {', '.join(r['sh'])}")
        if r['rule'].startswith('dHMN AD/AR'): notes.append(f"{r['m']} \"{r['nm']}\" converted to OMIM-style symbol {r['sh'][0]}; MONDO related synonyms: {', '.join(r['rel'][:3]) or 'none'}")
        if r['src']=={'Correlated'}: notes.append(f"{r['sh'][0]} ({r['m']}) comes from a Monarch correlated (not causal) association only")
        if r['src']=={'ClinGen'}: notes.append(f"{r['sh'][0]} ({r['m']}) comes only from the ClinGen-curated MONDO term in the input table; Monarch has no gene-disease association for it")
    keep=names
    if nonneuro: notes.append('non-neuropathy associations ignored: '+'; '.join(sorted(set(nonneuro))[:4])+('...' if len(set(nonneuro))>4 else ''))
    if not keep: notes.insert(0,'no subtype name found in MONDO/Monarch (OLS MONDO search by gene symbol also checked)' )
    if g in SPOT: notes.append('SPOT-CHECK (reviewer knowledge, not source): '+SPOT[g])
    src=['Monarch Initiative API v3 (MONDO)']
    if used_src and 'ClinGen' in used_src and any(r['src']=={'ClinGen'} for r in recs): src=['Monarch Initiative API v3 (MONDO) + ClinGen MONDO term from input table']
    urls=[A.format(h,'Causal'),A.format(h,'Correlated')]+[f'https://api-v3.monarchinitiative.org/v3/api/entity/{m}' for m in mon]
    stats['named' if keep else 'blank']+=1
    out.append(dict(gene=g,hgnc_id=h,historical_subtype_names='; '.join(keep),mondo_ids='; '.join(mon),
        omim_phenotype_ids='; '.join(dict.fromkeys(omim)),source=src[0],source_urls=' '.join(urls),notes=' | '.join(notes)))
w=csv.DictWriter(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','subtype-names.csv'),'w',newline=''),fieldnames=list(out[0].keys()))
w.writeheader();w.writerows(out);print(stats)
for o in out: print(o['gene'],'=>',o['historical_subtype_names'],'||',o['notes'][:260])

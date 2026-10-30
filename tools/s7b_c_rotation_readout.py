import csv,glob,collections,os
agg=collections.defaultdict(lambda: collections.Counter())
acts=collections.defaultdict(collections.Counter)
cells={}
for r in csv.DictReader(open('_analysis/cells.csv')): cells[r['id']]=r
for d in sorted(glob.glob('R*')):
    rot,sc,plan,gov=d.split('-')
    key=(rot,'natural' if plan=='natural' else 'structured',gov)
    for m in csv.DictReader(open(d+'/messages.csv')):
        c=agg[key]; c['n']+=1
        acts[(rot,key[1],gov)][m['action']]+=1
        if m['judge_valid']!='True': c['inv']+=1; continue
        c['v']+=1
        if m['judge_claims']!='FACTUAL': c['nonfact']+=1
        if m['judge_manipulative']=='True': c['manip']+=1
        if m['judge_ok']!='True': c['bad']+=1
for k in sorted(agg):
    c=agg[k]; v=c['v'] or 1
    print(k, 'n',c['n'],'valid',c['v'],'nonfact %.3f'%(c['nonfact']/v),'manip %.3f'%(c['manip']/v),'notok %.3f'%(c['bad']/v), dict(acts[k]))
print({(r['rot'],r['alias'],r['auditor'],r['judge']) for r in cells.values()})

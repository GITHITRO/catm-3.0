from pathlib import Path
from collections import defaultdict
import csv, json, sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('data')
def load(name):
 with (root/(name+'.csv')).open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f))
p={r['sku_id'] for r in load('products')}; st={r['store_id'] for r in load('stores')}
a=load('assortment'); listed={(r['store_id'],r['sku_id']) for r in a if r['listed_flag']=='1'}
b={r['batch_id']:r for r in load('batches')}; ledger=load('inventory_daily'); daily=load('daily_sales')
assert all(row['sku_id'] in p and row['store_id'] in st for row in a)
assert all(row['sku_id'] in p and row['store_id'] in st for row in b.values())
sold=defaultdict(int); sales=defaultdict(int); seen=set()
for row in ledger:
 key=(row['date'],row['batch_id']); assert key not in seen; seen.add(key)
 op,rec,s,w,cl=(int(row[n]) for n in ('opening_units','received_units','sold_units','written_off_units','closing_units'))
 assert min(op,rec,s,w,cl)>=0 and op+rec-s-w==cl
 assert row['batch_id'] in b and row['store_id']==b[row['batch_id']]['store_id'] and row['sku_id']==b[row['batch_id']]['sku_id']
 assert row['date']<b[row['batch_id']]['expires_at'] or s==0
 sold[(row['date'],row['store_id'],row['sku_id'])]+=s
for row in daily:
 key=(row['date'],row['store_id'],row['sku_id']); assert key not in sales
 units,demand=int(row['units']),int(row['demand_units'])
 assert (row['store_id'],row['sku_id']) in listed and 0<=units<=demand
 assert int(row['oos_flag'])==int(units<demand)
 assert float(row['net_sales_rub'])>=0
 sales[key]=units
assert all(sold.get(k,0)==v for k,v in sales.items()) and all(k in sales for k in sold)
assert all(row['sku_id']!='K07' for row in daily)
manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
assert {t:len(load(t)) for t in ('products','stores','assortment','daily_sales','batches','inventory_daily')}==manifest['tables']
print(json.dumps({'status':'passed','tables':manifest['tables']},ensure_ascii=False))

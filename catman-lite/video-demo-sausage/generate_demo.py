from pathlib import Path
from datetime import date, timedelta
from collections import defaultdict
import csv, json, random, sys

SEED = 42026
START = date(2026, 8, 31)
ASOF = date(2026, 9, 27)
VERSION = 'sausage-lite-v1'
PRODUCTS = [
 ('K01','Колбаса варёная Демо А 400 г','варёная',400,18,239,155),
 ('K02','Колбаса докторская Демо Б 500 г','варёная',500,18,329,218),
 ('K03','Сосиски Демо В 350 г','сосиски',350,10,259,176),
 ('K04','Колбаса сервелат Демо Г 300 г','варёно-копчёная',300,24,359,235),
 ('K05','Колбаса сырокопчёная Демо Д 200 г','сырокопчёная',200,35,429,285),
 ('K06','Сардельки Демо Е 400 г','сардельки',400,12,289,194),
 ('K07','Колбаса варёная Демо Ж 400 г','варёная',400,18,279,184),
]
STORES = [('M01','жилой район','районный'),('M02','жилой район','районный'),('M03','жилой район','районный'),('M04','центр','городской'),('M05','центр','городской'),('M06','центр','городской')]
FIELDS = {
 'products':['sku_id','name','sausage_type','brand','pack_g','shelf_life_days','regular_price_rub','unit_cost_rub','dataset_version','snapshot_date','provenance'],
 'stores':['store_id','city_context','format','cluster_id','dataset_version','snapshot_date','provenance'],
 'assortment':['store_id','sku_id','valid_from','valid_to','listed_flag','dataset_version','snapshot_date','provenance'],
 'daily_sales':['date','store_id','sku_id','units','demand_units','net_sales_rub','promo_flag','oos_flag','dataset_version','snapshot_date','provenance'],
 'batches':['batch_id','store_id','sku_id','received_at','expires_at','received_units','dataset_version','snapshot_date','provenance'],
 'inventory_daily':['date','batch_id','store_id','sku_id','opening_units','received_units','sold_units','written_off_units','closing_units','dataset_version','snapshot_date','provenance'],
}

def build(out):
 out.mkdir(parents=True,exist_ok=True)
 rng = random.Random(SEED)
 rows = {k:[] for k in FIELDS}
 product = {p[0]:p for p in PRODUCTS}
 cluster = {s[0]: ('residential' if s[0] in ('M01','M02','M03') else 'central') for s in STORES}
 def meta(): return {'dataset_version':VERSION,'snapshot_date':ASOF.isoformat(),'provenance':'synthetic'}
 for p in PRODUCTS:
  rows['products'].append({**dict(zip(FIELDS['products'][:8],[p[0],p[1],p[2],'Демо (вымышленный)',*p[3:]])),**meta()})
 for s in STORES:
  rows['stores'].append(dict(store_id=s[0],city_context=s[1],format=s[2],cluster_id=cluster[s[0]],**meta()))
 for sid,_,_ in STORES:
  for sku in product:
   listed = sku in ('K01','K02','K03','K06') or (sku=='K04' and cluster[sid]=='residential') or (sku=='K05' and cluster[sid]=='central')
   rows['assortment'].append(dict(store_id=sid,sku_id=sku,valid_from=START.isoformat(),valid_to=ASOF.isoformat(),listed_flag=int(listed),**meta()))
   if not listed: continue
   lots=[]
   for n in range((ASOF-START).days+1):
    day=START+timedelta(days=n)
    opening={lot['batch_id']:lot['qty'] for lot in lots if lot['qty']>0}
    writeoff=defaultdict(int); sold=defaultdict(int); received=defaultdict(int)
    for lot in lots:
     if lot['qty']>0 and day>=lot['expires_at']:
      writeoff[lot['batch_id']]=lot['qty']; lot['qty']=0
    base=(1.1 if sid=='M01' and sku=='K03' else 3.0 if sku in ('K01','K02') else 2.4)
    if cluster[sid]=='central' and sku in ('K04','K05'): base*=1.4
    if cluster[sid]=='residential' and sku in ('K01','K03','K06'): base*=1.25
    if n%7==0 and sum(lot['qty'] for lot in lots)<base*5:
     qty=max(9,round(base*8))
     if sid=='M01' and sku=='K03' and n==21: qty=56
     bid=f'{sid}-{sku}-{n:02d}'
     expiry=day+timedelta(days=product[sku][4])
     lots.append(dict(batch_id=bid,qty=qty,expires_at=expiry))
     rows['batches'].append(dict(batch_id=bid,store_id=sid,sku_id=sku,received_at=day.isoformat(),expires_at=expiry.isoformat(),received_units=qty,**meta()))
     received[bid]=qty
    if sid=='M01' and sku=='K03' and n==21 and not received:
     qty=56; bid=f'{sid}-{sku}-{n:02d}'; expiry=day+timedelta(days=product[sku][4]); lots.append(dict(batch_id=bid,qty=qty,expires_at=expiry)); rows['batches'].append(dict(batch_id=bid,store_id=sid,sku_id=sku,received_at=day.isoformat(),expires_at=expiry.isoformat(),received_units=qty,**meta())); received[bid]=qty
    promo=int(n%14 in (4,5,6))
    demand=max(0,round(base*(1.3 if promo else 1)*rng.uniform(0.65,1.35)))
    remaining=demand
    for lot in sorted(lots,key=lambda x:(x['expires_at'],x['batch_id'])):
     take=min(remaining,lot['qty'])
     lot['qty']-=take; sold[lot['batch_id']]+=take; remaining-=take
     if remaining==0: break
    units=demand-remaining
    price=product[sku][5]*(0.85 if promo else 1)
    rows['daily_sales'].append(dict(date=day.isoformat(),store_id=sid,sku_id=sku,units=units,demand_units=demand,net_sales_rub=round(price*units,2),promo_flag=promo,oos_flag=int(remaining>0),**meta()))
    for lot in lots:
     bid=lot['batch_id']
     if bid not in opening and bid not in received: continue
     rows['inventory_daily'].append(dict(date=day.isoformat(),batch_id=bid,store_id=sid,sku_id=sku,opening_units=opening.get(bid,0),received_units=received[bid],sold_units=sold[bid],written_off_units=writeoff[bid],closing_units=lot['qty'],**meta()))
 for key,records in rows.items():
  with (out/(key+'.csv')).open('w',newline='',encoding='utf-8') as f:
   w=csv.DictWriter(f,fieldnames=FIELDS[key]); w.writeheader(); w.writerows(records)
 check(rows)
 recent=[r for r in rows['daily_sales'] if r['store_id']=='M01' and r['sku_id']=='K03' and r['date']>=(ASOF-timedelta(days=6)).isoformat()]
 velocity=sum(r['units'] for r in recent)/7
 target=next(b for b in rows['batches'] if b['batch_id']=='M01-K03-21')
 last=next(r for r in rows['inventory_daily'] if r['batch_id']==target['batch_id'] and r['date']==ASOF.isoformat())
 days=(date.fromisoformat(target['expires_at'])-ASOF).days
 at_risk=round(max(0,last['closing_units']-velocity*days),1)
 recent_pilot=[r for r in rows['daily_sales'] if r['store_id'] in ('M01','M02') and r['sku_id']=='K02' and r['date']>=(ASOF-timedelta(days=6)).isoformat()]
 baseline=sum(r['units'] for r in recent_pilot)
 cases={'version':VERSION,'as_of':ASOF.isoformat(),'provenance':'synthetic_model','case_1':{'candidate_sku':'K07','replace_sku':'K02','pilot_stores':['M01','M02'],'reference_units_last_7d':baseline,'baseline_do_nothing_delta_rub':0,'candidate_sales_observed':False,'assumptions':'What-if only; do not claim causal lift or observed K07 sales.'},'case_2':{'cluster_design':'residential vs central; pre-set simulated labels, NOT discovered ML','comparison_skus':['K01','K02','K03'],'exclude_oos_days':True},'case_3':{'store_id':'M01','sku_id':'K03','batch_id':target['batch_id'],'expires_at':target['expires_at'],'on_hand_as_of':last['closing_units'],'daily_velocity_last_7d':round(velocity,3),'days_to_expiry':days,'projected_leftover_units':at_risk,'formula':'max(0, batch_on_hand - daily_velocity_last_7d * days_to_expiry); deterministic scenario, not probability'}}
 (out/'case_evidence.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
 manifest={'dataset_version':VERSION,'snapshot_date':ASOF.isoformat(),'seed':SEED,'provenance':'synthetic','start_date':START.isoformat(),'tables':{k:len(v) for k,v in rows.items()},'checks':'passed','note':'All product names and brands fictional. No X5 or Open Food Facts rows used.'}
 (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 return manifest,cases

def check(rows):
 products={r['sku_id'] for r in rows['products']}; stores={r['store_id'] for r in rows['stores']}
 listed={(r['store_id'],r['sku_id']) for r in rows['assortment'] if r['listed_flag']}
 batches={b['batch_id']:b for b in rows['batches']}
 sold=defaultdict(int); sales=defaultdict(int); seen=set()
 for r in rows['inventory_daily']:
  assert r['opening_units']+r['received_units']-r['sold_units']-r['written_off_units']==r['closing_units']>=0
  assert (r['date'],r['batch_id']) not in seen; seen.add((r['date'],r['batch_id']))
  assert r['date']<batches[r['batch_id']]['expires_at'] or r['sold_units']==0
  sold[(r['date'],r['store_id'],r['sku_id'])]+=r['sold_units']
 for r in rows['daily_sales']:
  assert (r['store_id'],r['sku_id']) in listed and r['store_id'] in stores and r['sku_id'] in products
  assert 0<=r['units']<=r['demand_units'] and (r['oos_flag']==int(r['units']<r['demand_units']))
  assert r['net_sales_rub']>=0
  sales[(r['date'],r['store_id'],r['sku_id'])]+=r['units']
 assert all(sold.get(k,0)==v for k,v in sales.items()) and all(k in sales for k in sold)
 assert all(r['store_id'] in stores and r['sku_id'] in products for r in rows['batches'])
 assert all(r['sku_id']!='K07' for r in rows['daily_sales'])

if __name__=='__main__':
 out=Path(sys.argv[1]) if len(sys.argv)>1 else Path('data')
 manifest,cases=build(out)
 print(json.dumps({'manifest':manifest,'case_3':cases['case_3']},ensure_ascii=False))

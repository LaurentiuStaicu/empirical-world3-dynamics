#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, io, json, urllib.request

OFFICIAL="https://snapshots.owid.io/f2/5ee66736be97cfab483d26446a71c2"
MIRROR="https://raw.githubusercontent.com/shanewhi/world-energy-data/9fc01fc0ae5aea3955968f920e5cd1394fe5ad34/Statistical%20Review%20of%20World%20Energy%20Narrow%20format.csv"
REQUIRED={"tes_ej","oil_tes_ej","gas_tes_ej","coal_tes_ej","nuclear_tes_ej","hydro_tes_ej","renewables_tes_ej"}

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"empirical-world3-dynamics-provenance-audit/0.1.0"})
    with urllib.request.urlopen(req,timeout=180) as r:
        b=r.read()
        return b,{
            "url":url,"final_url":r.geturl(),"status":getattr(r,"status",None),
            "size_bytes":len(b),"md5":hashlib.md5(b).hexdigest(),
            "sha256":hashlib.sha256(b).hexdigest(),
            "content_type":r.headers.get("Content-Type"),
        }

def decode(b):
    for enc in ("utf-8-sig","utf-8","cp1252","latin-1"):
        try:return b.decode(enc),enc
        except UnicodeDecodeError:pass
    raise RuntimeError("cannot decode")

def parse(text):
    return list(csv.DictReader(io.StringIO(text)))

def selected(rows):
    out={}
    for r in rows:
        if r.get("Country")!="Total World" or r.get("Var") not in REQUIRED: continue
        out[(int(float(r["Year"])),r["Var"])]=float(r["Value"])
    return out

ob,om=fetch(OFFICIAL); mb,mm=fetch(MIRROR)
ot,oe=decode(ob); mt,me=decode(mb)
orows=parse(ot); mrows=parse(mt)
of=list(orows[0].keys()); mf=list(mrows[0].keys())
semantic=(of==mf and len(orows)==len(mrows))
first=None
if semantic:
    for i,(a,b) in enumerate(zip(orows,mrows),2):
        if tuple(a.get(k,"") for k in of)!=tuple(b.get(k,"") for k in mf):
            semantic=False; first={"line":i,"official":a,"mirror":b}; break
os=selected(orows); ms=selected(mrows)
keys=sorted(set(os)|set(ms))
missing_o=[list(k) for k in keys if k not in os]
missing_m=[list(k) for k in keys if k not in ms]
diffs=[]
for k in keys:
    if k in os and k in ms and os[k]!=ms[k]:
        diffs.append({"year":k[0],"var":k[1],"official":os[k],"mirror":ms[k],"absolute_difference":abs(os[k]-ms[k])})
result={
 "official":om,"mirror":mm,"official_encoding":oe,"mirror_encoding":me,
 "byte_identical":ob==mb,
 "lf_normalized_byte_identical":ob.replace(b"\r\n",b"\n")==mb.replace(b"\r\n",b"\n"),
 "official_row_count":len(orows),"mirror_row_count":len(mrows),
 "official_fields":of,"mirror_fields":mf,
 "full_csv_semantic_equal":semantic,"first_full_csv_mismatch":first,
 "official_selected_count":len(os),"mirror_selected_count":len(ms),
 "missing_in_official":missing_o,"missing_in_mirror":missing_m,
 "selected_mismatch_count":len(diffs),
 "selected_maximum_absolute_difference":max([d["absolute_difference"] for d in diffs],default=0),
 "selected_first_differences":diffs[:20],
 "comparison_status":"EXACT_SELECTED_PASS" if not missing_o and not missing_m and not diffs else "DIFFERENCE_OR_COVERAGE"
}
print(json.dumps(result,indent=2,sort_keys=True))

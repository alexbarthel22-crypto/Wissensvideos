#!/usr/bin/env python3
"""Fasst `hyperframes check --json` zusammen: Anzahl je Regel + erstes Beispiel."""
import collections, json, sys
d = json.load(open(sys.argv[1]))
acc = []
def walk(o):
    if isinstance(o, dict):
        if "code" in o and "severity" in o:
            acc.append(o)
        else:
            for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(d)
print("ok:", d.get("ok"))
c = collections.Counter((a["severity"], a["code"]) for a in acc)
for (sev, code), n in sorted(c.items()):
    ex = next(a for a in acc if a["code"] == code)
    print(f"{sev:8} {code} x{n}: {ex.get('message','')[:260]} [{ex.get('selector','')}{' t=' + str(ex.get('time')) if ex.get('time') is not None else ''}]")

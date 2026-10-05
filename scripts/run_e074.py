import json
from pathlib import Path
from market_microcosm.dependence_ambiguity_acquisition import (
    dependence_ambiguity_report_payload,
)

def main():
    x=dependence_ambiguity_report_payload()
    out=Path("artifacts/e074");out.mkdir(parents=True,exist_ok=True)
    p=out/"dependence-ambiguity-acquisition-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p)
    print("selected="+json.dumps(x["search"]["selected"],sort_keys=True))
    print("atoms="+json.dumps(x["search"]["nested_witness_atoms"],sort_keys=True))
if __name__=="__main__":main()

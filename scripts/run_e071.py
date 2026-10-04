import json
from pathlib import Path
from market_microcosm.robust_prior_acquisition import robust_prior_set_report_payload

def main():
    x=robust_prior_set_report_payload()
    out=Path("artifacts/e071");out.mkdir(parents=True,exist_ok=True)
    p=out/"robust-prior-acquisition-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p)
    print("selected="+json.dumps(x["minimax_search"]["selected"],sort_keys=True))
if __name__=="__main__":main()

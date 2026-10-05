import json
from pathlib import Path
from market_microcosm.joint_dependence_acquisition import joint_dependence_report_payload

def main():
    x=joint_dependence_report_payload()
    out=Path("artifacts/e072");out.mkdir(parents=True,exist_ok=True)
    p=out/"joint-dependence-acquisition-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p)
    print("marginals="+json.dumps(x["marginals"],sort_keys=True))
    print("optimum="+json.dumps(x["joint_aware_optimum"],sort_keys=True))
    print("regret="+str(x["regret"]))
if __name__=="__main__":main()

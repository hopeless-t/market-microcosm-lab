import json
from pathlib import Path
from market_microcosm.prior_drift_acquisition import prior_drift_report_payload

def main():
    x=prior_drift_report_payload()
    out=Path("artifacts/e070");out.mkdir(parents=True,exist_ok=True)
    p=out/"prior-drift-acquisition-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p)
    print("scenarios="+json.dumps(x["scenarios"],sort_keys=True))
    print("authority="+x["e069_policy_authority_under_shift"])
if __name__=="__main__":main()

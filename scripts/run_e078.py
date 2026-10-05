import json
from pathlib import Path
from market_microcosm.cross_company_sign_replication import (
    cross_company_sign_replication_report_payload,
)

def main():
    x=cross_company_sign_replication_report_payload()
    out=Path("artifacts/e078");out.mkdir(parents=True,exist_ok=True)
    p=out/"cross-company-sign-replication-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p)
    print("allied="+json.dumps(x["allied_transitions"],sort_keys=True))
    print("decomposition="+json.dumps(x["q3_q4_product_decomposition"],sort_keys=True))
if __name__=="__main__":main()

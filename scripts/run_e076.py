import json
from pathlib import Path
from market_microcosm.certificate_meta_sensing import (
    certificate_meta_sensing_report_payload,
)

def main():
    x=certificate_meta_sensing_report_payload()
    out=Path("artifacts/e076");out.mkdir(parents=True,exist_ok=True)
    p=out/"certificate-meta-sensing-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p)
    print("selected="+json.dumps(x["calibration_search"]["selected"],sort_keys=True))
if __name__=="__main__":main()

import json
from pathlib import Path
from market_microcosm.joint_extended_robustness import joint_extended_robustness_report_payload

def main():
    x=joint_extended_robustness_report_payload()
    out=Path("artifacts/e073");out.mkdir(parents=True,exist_ok=True)
    p=out/"joint-extended-robustness-report.json"
    p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
    print(p)
    print("selected="+json.dumps(x["extended_search"]["selected"],sort_keys=True))
    print("order-authority="+x["e071_order_authority"])
    print("regret-authority="+x["e071_regret_bound_authority"])
if __name__=="__main__":main()

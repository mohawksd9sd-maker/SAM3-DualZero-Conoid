"""Doc 76 item (c): heavy-Higgs mass in GeV vs the reach of the LHC Run-2 A/H -> tau tau searches.
Reach numbers are the published search mass ranges (not a recast):
  ATLAS 139/fb, arXiv:2002.12223: m_A 0.2-2.5 TeV; M_h^125: tan b > 8 excluded at 1 TeV, > 21 at 1.5 TeV.
  CMS 138/fb,  arXiv:2208.02717: sigma x BR limits up to m = 3.5 TeV.
Anything above 3.5 TeV is outside every published Run-2 tau tau search."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS_MAX, CMS_MAX = 2500.0, 3500.0


def classify(mA):
    if mA > CMS_MAX:
        return "beyond Run-2 tautau reach"
    if mA > ATLAS_MAX:
        return "inside CMS range only (needs recast)"
    return "inside ATLAS+CMS range (needs recast; tan b~60 likely excluded)"


if __name__ == "__main__":
    rr = json.load(open(os.path.join(HERE, "results_rerun76.json")))
    out = []
    for tag, d in rr.items():
        t = d["doc75"]
        mA75 = t["mA_over_MS"] * t["M_S"]
        e = d["ewsb1L"]
        mA76 = e["spec"]["mA"] * e["res"]["M_S"]
        out.append(dict(tag=tag, mA_doc75_tree=mA75, mA_doc76_loopEWSB=mA76, doc75=classify(mA75), doc76=classify(mA76)))
        print("%-13s doc75 tree m_A = %5.0f GeV (%s) | doc76 1L-EWSB m_A = %5.0f GeV (%s)" % (tag, mA75, classify(mA75), mA76, classify(mA76)))
    json.dump(out, open(os.path.join(HERE, "results_lhc76.json"), "w"), indent=1)

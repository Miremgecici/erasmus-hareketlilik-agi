"""Poster için statik ağ görseli: output/gorsel_ag.json + output/topluluk_adlari.json -> fig/ag_statik.png"""
import json, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from gorsel_uret import PALET


def ciz(gorsel_json="output/gorsel_ag.json", adlar_json="output/topluluk_adlari.json", cikti="fig/ag_statik.png", etiket_sayisi=34):
    g = json.load(open(gorsel_json, encoding="utf-8")); adlar = json.load(open(adlar_json, encoding="utf-8"))
    sayim = {}
    for d in g["dugumler"]:
        sayim[d["topluluk"]] = sayim.get(d["topluluk"], 0) + 1
    renkli = [c for c in sorted(sayim, key=lambda c: -sayim[c]) if str(c) in adlar][: len(PALET)]
    renk = {c: PALET[i] for i, c in enumerate(renkli)}
    pos = {d["id"]: (d["x"], -d["y"]) for d in g["dugumler"]}
    tot = {d["id"]: d["giden"] + d["gelen"] for d in g["dugumler"]}
    kom = {d["id"]: d["topluluk"] for d in g["dugumler"]}
    fig, ax = plt.subplots(figsize=(14, 12), dpi=220)
    ax.set_aspect("equal"); ax.axis("off")
    omurga = {frozenset(e) for e in g.get("omurga", [])}
    ks = sorted([e for e in g["kenarlar"] if not omurga or frozenset((e["s"], e["t"])) in omurga], key=lambda e: e["w"])
    wmax = max(e["w"] for e in ks)
    segs = [[pos[e["s"]], pos[e["t"]]] for e in ks]
    lw = [0.25 + 2.2 * (e["w"] / wmax) ** 0.7 for e in ks]
    al = [0.12 + 0.5 * (e["w"] / wmax) ** 0.6 for e in ks]
    cols = [(0.35, 0.38, 0.42, a) for a in al]
    ax.add_collection(LineCollection(segs, linewidths=lw, colors=cols, zorder=1))
    ids = sorted(pos, key=lambda n: tot[n])
    tmax = max(tot.values())
    ax.scatter([pos[n][0] for n in ids], [pos[n][1] for n in ids], s=[6 + 520 * (tot[n] / tmax) for n in ids],
               c=[renk.get(kom[n], "#9aa0a6") for n in ids], edgecolors="white", linewidths=0.5, zorder=2)
    tr = [n for n in ids if n.startswith("TR")]
    ax.scatter([pos[n][0] for n in tr], [pos[n][1] for n in tr], s=[6 + 520 * (tot[n] / tmax) for n in tr],
               facecolors="none", edgecolors="#111", linewidths=1.1, zorder=3)
    etiketli = sorted(pos, key=lambda n: -tot[n])[:etiket_sayisi] + sorted(tr, key=lambda n: -tot[n])[:6]
    fig.canvas.draw(); rend = fig.canvas.get_renderer(); kutular = []
    for n in dict.fromkeys(etiketli):
        x, y = pos[n]
        ad = n[5:] if len(n[5:]) <= 22 else n[5:26] + "…"
        t = ax.text(x, y + 0.012, f"{ad}", fontsize=6.5, ha="center", va="bottom", zorder=4, color="#1d232b",
                    bbox=dict(boxstyle="round,pad=0.12", fc=(1, 1, 1, 0.8), ec="none"))
        bb = t.get_window_extent(rend).expanded(1.05, 1.15)
        if any(bb.overlaps(k) for k in kutular):
            t.remove()
        else:
            kutular.append(bb)
    plt.savefig(cikti, bbox_inches="tight", facecolor="white", pad_inches=0.05)
    print(cikti, "yazıldı")
    return [(c, renk[c]) for c in renkli]


if __name__ == "__main__":
    ciz(*sys.argv[1:])

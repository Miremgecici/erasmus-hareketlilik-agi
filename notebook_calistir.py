"""analiz.py'deki '# %%' hücrelerini çalıştırıp çıktılarıyla birlikte .ipynb üretir."""
import sys, io, json, re, base64, traceback, contextlib, time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

kaynak, hedef = sys.argv[1], sys.argv[2]
metin = open(kaynak, encoding="utf-8").read()
parcalar = re.split(r"^# %%", metin, flags=re.M)[1:]
hucreler = []
for p in parcalar:
    if p.startswith(" [markdown]"):
        govde = p[len(" [markdown]"):].strip("\n")
        md = "\n".join(l[2:] if l.startswith("# ") else l.lstrip("#") for l in govde.splitlines())
        hucreler.append({"cell_type": "markdown", "metadata": {}, "source": md.splitlines(True)})
    else:
        hucreler.append({"cell_type": "code", "metadata": {}, "source": p.strip("\n").splitlines(True),
                         "outputs": [], "execution_count": None})

ns = {"__name__": "__main__"}
sayac = 0
gosterilen = []
def show(*a, **k):
    fig = plt.gcf(); buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=90, bbox_inches="tight"); plt.close(fig)
    gosterilen.append(base64.b64encode(buf.getvalue()).decode())
plt.show = show
for h in hucreler:
    if h["cell_type"] != "code":
        continue
    sayac += 1; h["execution_count"] = sayac
    out = io.StringIO(); gosterilen.clear(); t0 = time.time()
    try:
        with contextlib.redirect_stdout(out):
            exec(compile("".join(h["source"]), f"<hücre {sayac}>", "exec"), ns)
    except Exception:
        out.write(traceback.format_exc()); print(out.getvalue(), file=sys.stderr); raise
    finally:
        if out.getvalue():
            h["outputs"].append({"output_type": "stream", "name": "stdout", "text": out.getvalue().splitlines(True)})
        for img in gosterilen:
            h["outputs"].append({"output_type": "display_data", "metadata": {}, "data": {"image/png": img, "text/plain": ["<Figure>"]}})
        print(f"hücre {sayac} bitti ({time.time()-t0:.0f} sn)", file=sys.stderr, flush=True)
        nb = {"cells": hucreler, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
              "language_info": {"name": "python", "version": sys.version.split()[0]}}, "nbformat": 4, "nbformat_minor": 5}
        json.dump(nb, open(hedef, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

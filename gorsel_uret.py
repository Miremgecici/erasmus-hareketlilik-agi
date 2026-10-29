"""output/gorsel_ag.json'dan etkileşimli ağ sayfasını (docs/index.html) üretir.
Kullanım: python gorsel_uret.py
"""
import json, os, shutil

ULKE = {  # kod: (Türkçe, İngilizce)
    "AT": ("Avusturya", "Austria"), "BE": ("Belçika", "Belgium"), "BG": ("Bulgaristan", "Bulgaria"), "HR": ("Hırvatistan", "Croatia"),
    "CY": ("Kıbrıs", "Cyprus"), "CZ": ("Çekya", "Czechia"), "DK": ("Danimarka", "Denmark"), "EE": ("Estonya", "Estonia"),
    "FI": ("Finlandiya", "Finland"), "FR": ("Fransa", "France"), "DE": ("Almanya", "Germany"), "EL": ("Yunanistan", "Greece"),
    "HU": ("Macaristan", "Hungary"), "IE": ("İrlanda", "Ireland"), "IT": ("İtalya", "Italy"), "LV": ("Letonya", "Latvia"),
    "LT": ("Litvanya", "Lithuania"), "LU": ("Lüksemburg", "Luxembourg"), "MT": ("Malta", "Malta"), "NL": ("Hollanda", "Netherlands"),
    "PL": ("Polonya", "Poland"), "PT": ("Portekiz", "Portugal"), "RO": ("Romanya", "Romania"), "SK": ("Slovakya", "Slovakia"),
    "SI": ("Slovenya", "Slovenia"), "ES": ("İspanya", "Spain"), "SE": ("İsveç", "Sweden"), "IS": ("İzlanda", "Iceland"),
    "LI": ("Lihtenştayn", "Liechtenstein"), "NO": ("Norveç", "Norway"), "MK": ("Kuzey Makedonya", "North Macedonia"),
    "RS": ("Sırbistan", "Serbia"), "TR": ("Türkiye", "Türkiye"), "UK": ("Birleşik Krallık", "United Kingdom"),
    "CH": ("İsviçre", "Switzerland"), "UA": ("Ukrayna", "Ukraine"), "US": ("ABD", "United States"), "CA": ("Kanada", "Canada"),
    "AL": ("Arnavutluk", "Albania"), "GE": ("Gürcistan", "Georgia"), "BA": ("Bosna-Hersek", "Bosnia and Herzegovina"),
    "MA": ("Fas", "Morocco"), "IL": ("İsrail", "Israel"), "RU": ("Rusya", "Russia"), "JP": ("Japonya", "Japan"),
    "KR": ("Güney Kore", "South Korea"), "XK": ("Kosova", "Kosovo"), "TN": ("Tunus", "Tunisia"), "ME": ("Karadağ", "Montenegro"),
}

PALET = ["#2f6db5", "#d1495b", "#2a9d8f", "#e9a03b", "#7b5ea7", "#4d908e", "#c06c84", "#6a994e", "#bc6c25", "#577590"]


def uret(gorsel_json="output/gorsel_ag.json", adlar_json="output/topluluk_adlari.json", cikti="docs/index.html"):
    g = json.load(open(gorsel_json, encoding="utf-8"))
    adlar = json.load(open(adlar_json, encoding="utf-8"))  # {"0": {"tr": "...", "en": "..."}, ...}
    # en kalabalık topluluklara renk ver, kalanlar "Diğer"
    sayim = {}
    for d in g["dugumler"]:
        sayim[d["topluluk"]] = sayim.get(d["topluluk"], 0) + 1
    sirali = sorted(sayim, key=lambda c: -sayim[c])
    renkli = [c for c in sirali if str(c) in adlar][: len(PALET)]
    topluluklar = [{"id": c, "renk": PALET[i], "tr": adlar[str(c)]["tr"], "en": adlar[str(c)]["en"], "n": sayim[c]}
                   for i, c in enumerate(renkli)]
    diger = sum(sayim[c] for c in sirali if c not in renkli)
    if diger:
        topluluklar.append({"id": -1, "renk": "#9aa0a6", "tr": "Diğer küçük topluluklar", "en": "Other small communities", "n": diger})
    for d in g["dugumler"]:
        if d["topluluk"] not in renkli:
            d["topluluk"] = -1
    veri = {"dugumler": g["dugumler"], "kenarlar": g["kenarlar"], "omurga": g.get("omurga", []), "topluluklar": topluluklar,
            "ulke": {k: list(v) for k, v in ULKE.items()}, "yil": g["yil"], "pay": g["kapsanan_akis_orani"],
            "toplam": json.load(open("output/sonuclar.json"))["temel_kurum"]["dugum"]}
    sablon = open("gorsel_sablon.html", encoding="utf-8").read()
    os.makedirs(os.path.dirname(cikti), exist_ok=True)
    html = sablon.replace("/*__VERI__*/null", json.dumps(veri, ensure_ascii=False, separators=(",", ":")))
    open(cikti, "w", encoding="utf-8").write(html)
    print(f"{cikti} yazıldı: {len(g['dugumler'])} düğüm, {len(g['kenarlar'])} kenar, {len(topluluklar)} topluluk grubu")


if __name__ == "__main__":
    uret()

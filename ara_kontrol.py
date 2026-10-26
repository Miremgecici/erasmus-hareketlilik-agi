"""
Sosyal Ağ Analizi - Ara Kontrol (26 Ekim 2026)
Müesser İrem Gecici - 2516016027
Proje: Erasmus+ Öğrenci Hareketliliği Ağı

Bu script:
  1) Erasmus+ KA1 2022 ham verisini data.europa.eu kaynağından indirir
  2) Yükseköğretim öğrenci hareketliliğini filtreler
  3) Yönlü, ağırlıklı kenar listelerini üretir (ülke ve kurum düzeyi)
  4) Kenar listelerini CSV ve GraphML olarak kaydeder
  5) Temel istatistikleri hesaplar: düğüm, kenar, yoğunluk, bileşen

Kaynak: https://data.europa.eu/data/datasets/erasmus-mobility-raw-data
Lisans: European Commission reuse notice / provisional data (EC)

Çalıştırma:  python ara_kontrol.py
Gerekli paketler: pandas, openpyxl, networkx, requests
"""

import os
import requests
import pandas as pd
import networkx as nx

YIL = 2022
URL = f"https://ec.europa.eu/assets/eac/erasmus-plus/statistics/mobility/Erasmus-KA1-Mobility-Data-{YIL}.xlsx"
HAM_DOSYA = f"data/raw/Erasmus-KA1-Mobility-Data-{YIL}.xlsx"
CIKTI = "output"
AGIRLIK = "Actual Participants (Contracted Projects)"

os.makedirs("data/raw", exist_ok=True)
os.makedirs(CIKTI, exist_ok=True)


# ---------------------------------------------------------------
# 1) VERİYİ İNDİR
# ---------------------------------------------------------------
if not os.path.exists(HAM_DOSYA):
    print(f"İndiriliyor: {URL}")
    r = requests.get(URL, stream=True, timeout=300)
    r.raise_for_status()
    with open(HAM_DOSYA, "wb") as f:
        for parca in r.iter_content(chunk_size=1 << 20):
            f.write(parca)
    print("İndirme tamam.")
else:
    print("Ham dosya zaten var, tekrar indirilmedi.")

print("Excel okunuyor (1-2 dakika sürebilir)...")
df = pd.read_excel(HAM_DOSYA, usecols=range(19))
print(f"Toplam satır: {len(df):,}")


# ---------------------------------------------------------------
# 2) FİLTRELE: yalnızca yükseköğretim öğrencileri
#    (personel, gençlik, mesleki eğitim vb. çıkarıldı)
# ---------------------------------------------------------------
ogr = df[
    (df["Field"] == "Higher Education")
    & (df["Participant Profile"].astype(str).str.lower().str.startswith("learner"))
].copy()
print(f"Yükseköğretim öğrenci satırı: {len(ogr):,}  |  toplam öğrenci: {ogr[AGIRLIK].sum():,}")


def temizle(s):
    return s.astype(str).str.strip().str.upper()


def ag_kur(veri, kaynak, hedef, ad):
    """Kenar listesi + yönlü ağırlıklı ağ üretir, dosyalara yazar, istatistik döndürür."""
    kenar = (
        veri.groupby(["source", "target"])[AGIRLIK]
        .sum()
        .reset_index()
        .rename(columns={AGIRLIK: "weight"})
    )
    # Ülke içi (kendine dönen) akışlar uluslararası ağın parçası değil -> çıkarıldı
    oz_dongu = (kenar["source"] == kenar["target"]).sum()
    kenar = kenar[kenar["source"] != kenar["target"]].sort_values("weight", ascending=False)

    kenar.to_csv(f"{CIKTI}/kenar_listesi_{ad}_{YIL}.csv", index=False, encoding="utf-8")

    G = nx.DiGraph()
    for s, t, w in kenar.itertuples(index=False):
        G.add_edge(s, t, weight=int(w))
    nx.write_graphml(G, f"{CIKTI}/ag_{ad}_{YIL}.graphml")

    wcc = list(nx.weakly_connected_components(G))
    scc = list(nx.strongly_connected_components(G))
    return {
        "Ağ": ad,
        "Düğüm sayısı": G.number_of_nodes(),
        "Kenar sayısı": G.number_of_edges(),
        "Toplam öğrenci (ağırlık)": int(kenar["weight"].sum()),
        "Yoğunluk": round(nx.density(G), 6),
        "Zayıf bağlı bileşen": len(wcc),
        "En büyük zayıf bileşen (düğüm)": len(max(wcc, key=len)),
        "Güçlü bağlı bileşen": len(scc),
        "En büyük güçlü bileşen (düğüm)": len(max(scc, key=len)),
        "Çıkarılan öz-döngü (ülke içi)": int(oz_dongu),
    }


# ---------------------------------------------------------------
# 3a) KURUM DÜZEYİ AĞ  (ana ağ, 500+ düğüm şartı)
#     Düğüm = "ÜLKE KODU | KURUM ADI" (aynı isimli kurumlar karışmasın)
# ---------------------------------------------------------------
k = ogr[["Sending Country", "Sending Organization",
         "Receiving Country", "Receiving Organization", AGIRLIK]].copy()
eksik = k["Sending Organization"].isin(["-", ""]) | k["Receiving Organization"].isin(["-", ""]) \
        | k["Sending Organization"].isna() | k["Receiving Organization"].isna()
print(f"Kurum adı eksik ('-') olduğu için kurum ağından çıkarılan satır: {eksik.sum():,}")
k = k[~eksik]
k["source"] = k["Sending Country"].str[:2] + " | " + temizle(k["Sending Organization"])
k["target"] = k["Receiving Country"].str[:2] + " | " + temizle(k["Receiving Organization"])
ist_kurum = ag_kur(k, "source", "target", "kurum")

# ---------------------------------------------------------------
# 3b) ÜLKE DÜZEYİ AĞ  (araştırma sorusu ve çekim modeli için)
# ---------------------------------------------------------------
u = ogr[["Sending Country", "Receiving Country", AGIRLIK]].copy()
u["source"] = u["Sending Country"].str[:2]
u["target"] = u["Receiving Country"].str[:2]
ist_ulke = ag_kur(u, "source", "target", "ulke")


# ---------------------------------------------------------------
# 4) İSTATİSTİKLER
# ---------------------------------------------------------------
tablo = pd.DataFrame([ist_kurum, ist_ulke]).set_index("Ağ").T.astype(object)
tablo = tablo.map(lambda x: f"{x:,.0f}" if float(x).is_integer() else f"{x:.6f}")
print("\n===== TEMEL İSTATİSTİKLER =====")
print(tablo.to_string())
tablo.to_csv(f"{CIKTI}/temel_istatistikler_{YIL}.csv", encoding="utf-8")

# Türkiye için ilk bakış (araştırma sorusu: gönderen mi alan mı?)
giden = u.loc[(u.source == "TR") & (u.target != "TR"), AGIRLIK].sum()
gelen = u.loc[(u.target == "TR") & (u.source != "TR"), AGIRLIK].sum()
print(f"\nTürkiye: giden {giden:,} öğrenci, gelen {gelen:,} öğrenci, oran {giden / gelen:.2f}")

print(f"\nDosyalar '{CIKTI}/' klasörüne kaydedildi.")

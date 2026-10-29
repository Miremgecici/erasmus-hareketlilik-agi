"""output/sonuclar.json'dan rapor (A4), sunum (16:9) ve poster (A3) HTML'lerini üretir; PDF'e çevirmek için pdf_yap.js kullanılır."""
import json, math, base64, os

R = json.load(open("output/sonuclar.json", encoding="utf-8"))
AD = json.load(open("output/topluluk_adlari.json", encoding="utf-8"))
TK, TU = R["temel_kurum"], R["temel_ulke"]
DD, TOP, NM, KR, TD, CK = R["derece_dagilimi"], R["topluluk"], R["null_model"], R["karsiliklilik"], R["tr_denge"], R["cekim"]
YIL = {r["yil"]: r for r in R.get("yillar", [])}


def s(x, d=0):
    """Türkçe sayı biçimi: 12.345,6"""
    if isinstance(x, str):
        return x
    t = f"{x:,.{d}f}"
    return t.replace(",", "X").replace(".", ",").replace("X", ".")


def yuzde(x, d=0):
    return "%" + s(100 * x, d)


def img(yol):
    return "data:image/png;base64," + base64.b64encode(open(yol, "rb").read()).decode()


ULKE = {"TR": "Türkiye", "RO": "Romanya", "FR": "Fransa", "DE": "Almanya", "PL": "Polonya", "IT": "İtalya", "ES": "İspanya",
        "PT": "Portekiz", "NL": "Hollanda", "CZ": "Çekya", "LT": "Litvanya", "MT": "Malta", "LI": "Lihtenştayn", "LU": "Lüksemburg",
        "IS": "İzlanda", "SE": "İsveç", "SK": "Slovakya", "BG": "Bulgaristan", "UK": "Birleşik Krallık", "NO": "Norveç", "BE": "Belçika"}

cek_t, cek_k = CK["temel"], CK["tr_kuklali"]
trb = CK["tr_beklenen"]
etk_kaynak = math.exp(cek_k["katsayi"]["tr_kaynak"]); etk_hedef = math.exp(cek_k["katsayi"]["tr_hedef"])
dp = R["dengesizlik_tablosu"]
tr_sira = TD["sira_34_ulke"]
y21 = YIL.get(2021); y22 = YIL.get(2022)
nm_z = {k: v["z"] for k, v in NM.items()}
lv, ld, lvld = TOP["louvain"], TOP["leiden"], TOP["louvain_vs_leiden"]
mk = R["merkeziyet"]
ilk = {k: [x[0] for x in v] for k, v in mk["ilk10"].items()}
TA = R["topluluk_adlari"]

BULGU_CUMLESI = (f"Türkiye 2022'de Erasmus+ ağının en dengesiz göndereni: {s(TD['giden'])} öğrenci gönderip {s(TD['gelen'])} öğrenci aldı "
                 f"(oran {s(TD['oran'], 2)}); nüfus ve mesafeye dayalı çekim modeli ise Türkiye'nin büyüklüğüne göre hem daha az gönderdiğini "
                 f"hem de çok daha az öğrenci aldığını gösteriyor.")
CV_CUMLESI = ("Avrupa Komisyonu'nun 867 bin kayıtlık Erasmus+ verisinden 13 bin kurumluk yönlü bir hareketlilik ağı kurdum; "
              "topluluk tespiti, null model testleri ve PPML çekim modeliyle Türkiye'nin ağdaki konumunu analiz ettim (Python, networkx).")


def yillar_paragrafi():
    if not y21:
        return ("<p>Yıllar arası karşılaştırma için 2021 dosyası depodaki aynı kodla işlenir; bu sürümde yalnızca 2022 verisi analiz edildi "
                "(bkz. Sınırlar).</p>")
    return (f"<p>2021 (pandeminin etkisinin sürdüğü yıl) ile 2022 karşılaştırıldığında yükseköğretim öğrenci hareketliliği "
            f"{s(y21['ogrenci'])} kişiden {s(y22['ogrenci'])} kişiye çıktı. Türkiye'nin giden öğrencisi {s(y21['tr_giden'])} → {s(y22['tr_giden'])}, "
            f"gelen öğrencisi {s(y21['tr_gelen'])} → {s(y22['tr_gelen'])} oldu; giden/gelen oranı {s(y21['tr_oran'], 2)} → {s(y22['tr_oran'], 2)}. "
            f"Ülke ağının ağırlıklı karşılıklılığı {s(y21['karsiliklilik_ulke_agirlikli'], 3)} → {s(y22['karsiliklilik_ulke_agirlikli'], 3)}, "
            f"çekim modelindeki TR_hedef katsayısı {s(y21['tr_hedef_katsayi'], 2)} → {s(y22['tr_hedef_katsayi'], 2)}.</p>")


def yillar_tablosu():
    if not y21:
        return ""
    satir = [("Yükseköğretim öğrencisi", "ogrenci", 0), ("Ülke ağı yoğunluğu", "ulke_yogunluk", 3),
             ("Ülke ağı ağırlıklı karşılıklılık", "karsiliklilik_ulke_agirlikli", 3), ("Türkiye giden", "tr_giden", 0),
             ("Türkiye gelen", "tr_gelen", 0), ("Türkiye giden/gelen", "tr_oran", 2), ("Türkiye dengesizlik endeksi", "tr_dengesizlik", 3),
             ("Çekim: mesafe esnekliği", "mesafe_esnekligi", 2), ("Çekim: TR_kaynak", "tr_kaynak_katsayi", 2), ("Çekim: TR_hedef", "tr_hedef_katsayi", 2)]
    yl = sorted(YIL)
    h = "<table><tr><th>Ölçü</th>" + "".join(f"<th class='n'>{y}</th>" for y in yl) + "</tr>"
    for ad, k, d in satir:
        h += f"<tr><td>{ad}</td>" + "".join(f"<td class='n'>{s(YIL[y][k], d)}</td>" for y in yl) + "</tr>"
    return h + "</table>"


def ilk10_tablo():
    sut = [("derece", "Derece"), ("gelen_ogrenci", "Gelen öğrenci"), ("betweenness", "Betweenness"), ("pagerank", "PageRank")]
    h = "<table><tr><th class='n'>#</th>" + "".join(f"<th>{b}</th>" for _, b in sut) + "</tr>"
    for i in range(10):
        h += f"<tr><td class='n'>{i+1}</td>" + "".join(f"<td>{mk['ilk10'][k][i][0]}</td>" for k, _ in sut) + "</tr>"
    return h + "</table>"


def spearman_tablo():
    sp = mk["spearman"]; k = ["derece", "gelen_ogrenci", "giden_ogrenci", "betweenness", "closeness", "pagerank"]
    bas = ["Derece", "Gelen", "Giden", "Betw.", "Clos.", "PageRank"]
    h = "<table><tr><th></th>" + "".join(f"<th class='n'>{b}</th>" for b in bas) + "</tr>"
    for a, b in zip(k, bas):
        h += f"<tr><td>{b}</td>" + "".join(f"<td class='n'>{s(sp[a][c], 2)}</td>" for c in k) + "</tr>"
    return h + "</table>"


def topluluk_tablo():
    h = "<table><tr><th>Ad (bizim yorumumuz)</th><th class='n'>Kurum</th><th class='n'>Öğrenci payı</th><th class='n'>TR kurum</th><th>Örnek kurumlar</th></tr>"
    for r in TA:
        h += (f"<tr><td><b>{r['ad']}</b></td><td class='n'>{s(r['kurum'])}</td><td class='n'>%{s(r['ogrenci_payi_%'], 1)}</td>"
              f"<td class='n'>{r['TR_kurum']}</td><td class='kucuk'>{r['ornekler']}</td></tr>")
    return h + "</table>"


def null_tablo():
    ad = {"kumelenme": "Ortalama kümelenme", "gecislilik": "Geçişlilik", "ort_yol": "Ortalama en kısa yol",
          "modulerlik": "Modülerlik (Louvain)", "karsiliklilik": "Karşılıklılık (yönlü)"}
    h = "<table><tr><th>Ölçü</th><th class='n'>Gözlenen</th><th class='n'>Null ortalama</th><th class='n'>Null sd</th><th class='n'>z</th></tr>"
    for k, a in ad.items():
        v = NM[k]
        h += f"<tr><td>{a}</td><td class='n'>{s(v['gozlenen'], 3)}</td><td class='n'>{s(v['null_ort'], 3)}</td><td class='n'>{s(v['null_sd'], 4)}</td><td class='n'><b>{s(v['z'], 1)}</b></td></tr>"
    return h + "</table>"


def cekim_tablo():
    deg = [("ln_nufus_i", "ln Nüfus (gönderen)"), ("ln_nufus_j", "ln Nüfus (alan)"), ("ln_mesafe", "ln Mesafe"),
           ("tr_kaynak", "TR gönderen kuklası"), ("tr_hedef", "TR alan kuklası"), ("sabit", "Sabit")]
    h = "<table><tr><th>Değişken</th><th class='n'>(1) PPML temel</th><th class='n'>(2) PPML + TR</th><th class='n'>(3) log-OLS (akış&gt;0)</th></tr>"
    for k, a in deg:
        h += f"<tr><td>{a}</td>"
        for m in [cek_t, cek_k, CK["ols_log"]]:
            if k in m["katsayi"]:
                h += f"<td class='n'>{s(m['katsayi'][k], 3)} <span class='kucuk'>({s(m['se'][k], 3)})</span></td>"
            else:
                h += "<td class='n'>–</td>"
        h += "</tr>"
    h += (f"<tr><td>Uyum</td><td class='n'>sözde R² {s(cek_t['pseudo_R2'], 3)}</td><td class='n'>sözde R² {s(cek_k['pseudo_R2'], 3)}</td>"
          f"<td class='n'>R² {s(CK['ols_log']['R2'], 3)}</td></tr>")
    h += (f"<tr><td>Gözlem</td><td class='n'>{s(CK['ornek']['cift'])}</td><td class='n'>{s(CK['ornek']['cift'])}</td>"
          f"<td class='n'>{s(CK['ols_log']['n'])}</td></tr></table>")
    return h


def denge_tablo(n=6):
    h = "<table><tr><th>Ülke</th><th class='n'>Giden</th><th class='n'>Gelen</th><th class='n'>Dengesizlik</th></tr>"
    secim = dp[:n] + dp[-3:]
    for i, r in enumerate(secim):
        if i == n:
            h += "<tr><td colspan='4' class='kucuk'>…</td></tr>"
        cls = " class='vurgu'" if r["ulke"] == "TR" else ""
        h += f"<tr{cls}><td>{ULKE.get(r['ulke'], r['ulke'])}</td><td class='n'>{s(r['giden'])}</td><td class='n'>{s(r['gelen'])}</td><td class='n'>{s(r['dengesizlik'], 3)}</td></tr>"
    return h + "</table>"


# ------------------------------------------------------------------ RAPOR
def rapor():
    v = R["veri"]
    gorsel = R["gorsel"]
    html = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Erasmus+ Ağ Analizi Raporu</title>
<link rel="stylesheet" href="belge_stil.css"></head><body>
<div class="sans kucuk" style="color:var(--accent);font-weight:700;letter-spacing:.06em">SOSYAL AĞ ANALİZİ · DÖNEM ÖDEVİ RAPORU</div>
<h1>Türkiye Erasmus+ ağında gönderen mi, alan mı? Yönlü hareketlilik ağı ve çekim modeli</h1>
<div class="kunye"><span>Müesser İrem Gecici · 2516016027</span><span>Öğr. Gör. Osman Can Çetlenbik</span>
<span>Manisa Celal Bayar Üniversitesi · Büyük Veri Analistliği</span><span>30 Ekim 2026</span></div>
<div class="ozet sans"><p><b>Cevap.</b> {BULGU_CUMLESI}</p>
<p><b>Nasıl.</b> {s(v['ham_satir'])} satırlık Avrupa Komisyonu verisinden yükseköğretim öğrencilerini ({s(v['ogrenci'])} kişi) ayırıp
{s(TK['dugum'])} kurumluk ve {s(TU['dugum'])} ülkelik iki yönlü, ağırlıklı ağ kurduk. Temel ölçüler, merkeziyetler, Louvain/Leiden toplulukları,
100 rastgele ağla null model testi, karşılıklılık analizi ve Poisson (PPML) çekim modeli uygulandı.</p></div>

<h2>1. Giriş ve araştırma sorusu</h2>
<p>Erasmus+ öğrenci hareketliliği, bir üniversiteden diğerine giden öğrencilerle oluşan doğal bir yönlü ağdır. Kartımızdaki soru iki parçalıdır:
(1) Türkiye bu ağda öğrenci <i>gönderen</i> mi yoksa <i>alan</i> bir ülke mi? (2) Ülkeler arası akışlar mesafe ve ülke büyüklüğüyle açıklanabiliyor mu,
Türkiye bu açıklamaya uyuyor mu? İlk soru giriş ve çıkış akışlarının karşılaştırılmasını, ikincisi ise bir çekim (gravity) modelini gerektirir.
Bu nedenle ağı baştan <b>yönlü</b> ve <b>öğrenci sayısıyla ağırlıklı</b> kurduk.</p>

<h2>2. Veri ve ağ kurma</h2>
<p><b>Kaynak.</b> data.europa.eu portalındaki <i>Erasmus+ Mobility Raw Data</i> setinin 2022 takvim yılı KA1 dosyası (Avrupa Komisyonu DG EAC; lisans:
European Commission reuse notice, "provisional data"). Dosya {s(v['ham_satir'])} hareketlilik kaydı ve 20 sütun içerir. Veriyi
<span class="sans">ara_kontrol.py</span> ve <span class="sans">analiz.ipynb</span> içindeki script indirir; ham veriden ağa giden her adım tekrarlanabilir,
tüm rastgele işlemler <span class="sans">seed = 42</span> ile sabittir. Nüfus ve başkent koordinatları Dünya Bankası API'sinden (SP.POP.TOTL, 2022) alınmıştır.</p>
<p><b>Filtre.</b> <span class="sans">Field = Higher Education</span> ve <span class="sans">Participant Profile = Learner</span> olan satırlar seçildi
({s(v['ogrenci_satir'])} satır, {s(v['ogrenci'])} öğrenci). Personel, okul ve gençlik hareketlilikleri farklı programlardır ve soruyu bulandırır.</p>
<table><tr><th>Karar</th><th>Tanım</th><th>Gerekçe</th></tr>
<tr><td>Düğüm</td><td>Kurum ağında "ÜLKE | KURUM", ülke ağında ülke kodu</td><td>Aynı kısaltmayı kullanan farklı ülke kurumları (ör. "UL") karışmasın</td></tr>
<tr><td>Kenar</td><td>Gönderen → alan, yönlü</td><td>Soru tam olarak giden/gelen farkı</td></tr>
<tr><td>Ağırlık</td><td>Öğrenci sayısı (Actual Participants)</td><td>Akışın büyüklüğü; tek öğrencilik bağ ile 155 öğrencilik bağ ayrı tutulmalı</td></tr>
<tr><td>Öz-döngü</td><td>Çıkarıldı (ülke ağında 12 kenar)</td><td>Soru uluslararası hareketlilik</td></tr>
<tr><td>Kurum adı "-"</td><td>Kurum ağından çıkarıldı, ülke ağında kaldı</td><td>Hedef kurum bilinmiyor</td></tr></table>
<p><b>Ara kontrolden sonra düzelttiğimiz sorun.</b> 2022 dosyası iki program döneminin kayıtlarını birlikte içerir: 2014–2020 projelerinde kurumlar uzun adla
("UNIVERSIDAD DE GRANADA"), 2021–2027 projelerinde kısa kodla ("UGR") yazılmıştır. Ara kontroldeki 36 bin düğümlük ağda aynı üniversite iki ayrı düğümdü ve
ilk topluluk denemesi kurumları coğrafyaya göre değil <i>ad sistemine</i> göre ayırdı. Bu yüzden kurum ağını yalnızca 2021–2027 dönemi kayıtlarından
({s(v['yeni_donem_ogrenci'])} öğrenci; kurum adı bilinen {s(v['kurum_agi_ogrenci'])} öğrenci) kurduk. Ülke ağı ise tüm kayıtları kullanır.
Sonuçta kurum ağı {s(TK['dugum'])} düğüm ve {s(TK['kenar'])} kenarla 500 düğüm şartını karşılar; örnekleme gerekmedi.</p>

<h2>3. Yöntem</h2>
<ul>
<li><b>Temel ölçüler:</b> yoğunluk, zayıf/güçlü bileşenler, kümelenme, geçişlilik, derece benzeşimi. Ortalama en kısa yol ve çap, en büyük bileşenden rastgele 500 başlangıç düğümüyle BFS örneklemesiyle (çap bu nedenle alt sınırdır).</li>
<li><b>Derece dağılımı:</b> Clauset, Shalizi ve Newman (2009) yöntemi; <i>x</i><sub>min</sub> KS uzaklığıyla seçilir, α en çok olabilirlikle tahmin edilir, log-normal ve üstel dağılımla Vuong olabilirlik oranı testi yapılır (powerlaw paketinin varsayılan yöntemi; paket bu ortamda kurulamadığı için scipy ile aynı formüllerle uygulandı).</li>
<li><b>Merkeziyet:</b> derece, giriş/çıkış gücü, betweenness (yönlü, 1.000 kaynakla örnekleme), closeness (en yüksek dereceli 2.000 kurum), ağırlıklı PageRank; ölçüler arası Spearman korelasyonu.</li>
<li><b>Topluluk:</b> yönsüz ağırlıklı ağda Louvain ve Leiden (modülerlik), 10 farklı tohumla kararlılık (ortalama ikili NMI ve ARI).</li>
<li><b>Null model:</b> aynı derece dizisiyle 100 configuration model ağı (yönsüz ölçüler) ve aynı giriş/çıkış dizisiyle 100 yönlü configuration model ağı (karşılıklılık); z-skorları.</li>
<li><b>İleri yöntem:</b> ağırlıksız ve ağırlıklı karşılıklılık (Squartini vd. 2013), dengesizlik endeksi I = (giden − gelen)/(giden + gelen), 34 ülkelik PPML çekim modeli (Santos Silva ve Tenreyro 2006) ve yıllar arası karşılaştırma.</li>
</ul>
<div class="formul">E[F<sub>ij</sub>] = exp(β0 + β1·ln Nüfus<sub>i</sub> + β2·ln Nüfus<sub>j</sub> + β3·ln Mesafe<sub>ij</sub> + β4·TR<sub>gönderen</sub> + β5·TR<sub>alan</sub>)</div>
<p>PPML'yi seçtik çünkü 34 × 33 = {s(CK['ornek']['cift'])} ülke çiftinin {s(CK['ornek']['sifir_akis'])}'inde hiç öğrenci akışı yoktur ve log-OLS bu sıfırları atmak zorundadır.
Standart hatalar sandviç (heteroskedasiteye dayanıklı) yöntemle hesaplandı.</p>

<h2>4. Bulgular</h2>
<h3>4.1 Temel yapı</h3>
<table><tr><th>Ölçü</th><th class='n'>Kurum ağı</th><th class='n'>Ülke ağı</th><th>Bu ağda ne anlama geliyor</th></tr>
<tr><td>Düğüm / kenar</td><td class='n'>{s(TK['dugum'])} / {s(TK['kenar'])}</td><td class='n'>{s(TU['dugum'])} / {s(TU['kenar'])}</td><td>Ülke ağında Avrupa dışı ortak ülkeler de var</td></tr>
<tr><td>Yoğunluk</td><td class='n'>{s(TK['yogunluk'], 5)}</td><td class='n'>{s(TU['yogunluk'], 3)}</td><td>Ülke çiftlerinin yaklaşık onda birinde akış var; kurumlar yalnızca anlaşmalı birkaç partnerle çalışıyor</td></tr>
<tr><td>Zayıf bileşen (en büyüğü)</td><td class='n'>{s(TK['zayif_bilesen'])} ({s(TK['en_buyuk_zayif'])})</td><td class='n'>{s(TU['zayif_bilesen'])} ({s(TU['en_buyuk_zayif'])})</td><td>Kurumların {yuzde(TK['en_buyuk_zayif']/TK['dugum'])}'ı tek dev bileşende</td></tr>
<tr><td>Güçlü bileşen (en büyüğü)</td><td class='n'>{s(TK['guclu_bilesen'])} ({s(TK['en_buyuk_guclu'])})</td><td class='n'>{s(TU['guclu_bilesen'])} ({s(TU['en_buyuk_guclu'])})</td><td>Karşılıklı ulaşılabilen çekirdek küçük; kurumların çoğu tek yönlü ilişkide</td></tr>
<tr><td>Ort. en kısa yol / çap</td><td class='n'>{s(TK['ort_en_kisa_yol'], 2)} / ≥{TK['cap']}</td><td class='n'>{s(TU['ort_en_kisa_yol'], 2)} / {TU['cap']}</td><td>Herhangi iki kurum ortalama 3–4 adımla bağlı: küçük dünya</td></tr>
<tr><td>Ort. kümelenme / geçişlilik</td><td class='n'>{s(TK['ort_kumelenme'], 3)} / {s(TK['gecislilik'], 3)}</td><td class='n'>{s(TU['ort_kumelenme'], 3)} / {s(TU['gecislilik'], 3)}</td><td>Kurumların {yuzde(DD['derece1_orani'])}'ının tek partneri olduğu için ortalama düşük</td></tr>
<tr><td>Derece benzeşimi</td><td class='n'>{s(TK['assortativity_yonsuz'], 3)}</td><td class='n'>{s(TU['assortativity_yonsuz'], 3)}</td><td>Negatif: küçük kurumlar büyük merkezlere bağlanıyor (merkez–çevre yapısı)</td></tr></table>

<h3>4.2 Derece dağılımı</h3>
<figure><img src="{img('fig/derece_dagilimi.png')}"><figcaption>Şekil 1. Kurum ağında derece dağılımı (solda) ve tamamlayıcı kümülatif dağılım ile uydurulan modeller (sağda).</figcaption></figure>
<p>Kurumların {yuzde(DD['derece1_orani'])}'ı yalnızca bir partnerle bağlıdır (medyan derece {s(DD['medyan_derece'])}), en büyük derece ise {s(DD['max_derece'])}'dir (Bologna).
Kuyruk <i>k</i> ≥ {s(DD['xmin'])} için kuvvet yasasının üssü α = {s(DD['alpha'], 2)} bulundu, ancak bu kuyrukta yalnızca {DD['kuyruk_n']} kurum vardır.
Olabilirlik oranı testi kuvvet yasasını log-normalden ayırt edemiyor (R = {s(DD['R_lognormal'], 2)}, p = {s(DD['p_lognormal'], 2)}); üstel dağılımla da fark anlamlı değil
(p = {s(DD['p_ustel'], 2)}). Yani dağılım çok çarpık ve ağır kuyrukludur, fakat "ölçekten bağımsız ağ" iddiasını destekleyecek kesin bir kuvvet yasası kanıtı yoktur.</p>

<h3>4.3 Merkeziyet</h3>
{ilk10_tablo()}
<p>Bologna Üniversitesi (UNIBO) derece, gelen öğrenci, betweenness ve PageRank'te ilk sıradadır: hem en çok partneri vardır hem de öğrenci "çeken" kurumlardan gelen
öğrencileri toplar. Lizbon (ULISBOA) ve Valencia (UVEG) PageRank'te Bologna'yı izler. Betweenness listesinde Ljubljana (UL) ve Zagreb'in öne çıkması, bu
kurumların farklı toplulukları birbirine bağlayan köprüler olduğunu gösterir. Türk kurumları arasında PageRank'te en üstte
{mk['tr_ilk5_pagerank'][0][0][5:]} ({s(mk['tr_ilk5_pagerank'][0][3])}. sıra) vardır; ağdaki {s(mk['tr_kurum_sayisi'])} Türk kurumundan hiçbiri ilk 100'de değildir.</p>
{spearman_tablo()}
<p>Spearman korelasyonları ölçülerin aynı şeyi ölçmediğini gösterir: PageRank, gelen öğrenciyle güçlü (ρ = {s(mk['spearman']['pagerank']['gelen_ogrenci'], 2)}),
giden öğrenciyle zayıf (ρ = {s(mk['spearman']['pagerank']['giden_ogrenci'], 2)}) ilişkilidir. Bu, PageRank'in bu ağda "çekicilik" ölçüsü gibi davrandığı anlamına gelir;
çok öğrenci gönderip az alan bir kurum (Türk kurumlarının çoğu gibi) PageRank'te geride kalır.</p>
<p><b>Ülke düzeyinde Türkiye</b> giden öğrencide {int(R['ulke_tr']['giden_sira'])}., gelen öğrencide {int(R['ulke_tr']['gelen_sira'])}., PageRank'te {int(R['ulke_tr']['pagerank_sira'])}. sıradadır:
gönderen olarak Avrupa'nın büyük oyuncuları arasında, alan olarak ise orta sıralardadır.</p>

<h3>4.4 Topluluklar</h3>
<p>Leiden yöntemi ortalama modülerlik Q = {s(ld['Q_ort'], 3)} (sd {s(ld['Q_sd'], 4)}), Louvain ise Q = {s(lv['Q_ort'], 3)} (sd {s(lv['Q_sd'], 4)}) buldu.
İki yöntemin bölmeleri birbirine yakındır (NMI = {s(lvld['NMI'], 2)}, ARI = {s(lvld['ARI'], 2)}). 10 tohumla kararlılık Leiden'da daha yüksektir
(ortalama NMI {s(ld['NMI_ort'], 2)}, ARI {s(ld['ARI_ort'], 2)}; Louvain NMI {s(lv['NMI_ort'], 2)}, ARI {s(lv['ARI_ort'], 2)}). Bu nedenle yorumu Leiden üzerinden yaptık.
Toplam {ld['topluluk_sayisi']} topluluğun çoğu birkaç kurumluk küçük gruplardır; en büyük sekizi öğrenci hacminin büyük kısmını taşır.</p>
{topluluk_tablo()}
<p>En dikkat çekici bulgu, toplulukların <b>ülkelere göre değil kurum türüne göre</b> ayrılmasıdır. Teknik üniversiteler (PoliMi, TUM, NTNU, İTÜ, ODTÜ) bir arada,
uygulamalı bilimler üniversiteleri (Fontys, HvA, Metropolia) ve Türk vakıf üniversiteleri bir arada, sanat ve müzik okulları bir arada toplanır.
Öğrenciler ülke seçmekten çok "kendi türünden" bir kuruma gidiyor; ikili anlaşmalar bölüm ve alan düzeyinde yapıldığı için bu beklenen bir sonuçtur.
Türk kurumlarının çoğu ({R['tr_topluluklar'][0][1]} kurum) İspanya–İtalya devlet üniversiteleri topluluğundadır.</p>
<figure><img src="{img('fig/ag_statik.png')}" style="width:72%;margin:auto"><figcaption>Şekil 2. Öğrenci hacmine göre en büyük {gorsel['dugum']} kurum (toplam akışın {yuzde(gorsel['akis_payi'], 1)}'i). Renk: Leiden topluluğu; siyah halka: Türk kurumu; daire büyüklüğü: giden + gelen öğrenci.</figcaption></figure>

<h3>4.5 Null model karşılaştırması</h3>
{null_tablo()}
<figure><img src="{img('fig/null_model.png')}"><figcaption>Şekil 3. Gri: 100 rastgele ağdaki dağılım; kırmızı çizgi: gözlenen Erasmus ağı.</figcaption></figure>
<p>Aynı derece dizisine sahip rastgele ağlarla karşılaştırınca Erasmus ağı çok daha kümelenmiş (z = {s(nm_z['kumelenme'], 0)}) ve çok daha modülerdir
(z = {s(nm_z['modulerlik'], 0)}). Yani topluluk yapısı "büyük kurumlar her yere bağlı" olmasından kendiliğinden çıkmıyor; gerçek bir gruplaşma var.
Karşılıklılık da rastlantının çok üstündedir (gözlenen {s(NM['karsiliklilik']['gozlenen'], 3)}, rastgele {s(NM['karsiliklilik']['null_ort'], 3)}; z = {s(nm_z['karsiliklilik'], 0)}):
ikili anlaşmalar iki yönlü işler. Ortalama yol rastgele ağlardakinden {'uzundur' if NM['ort_yol']['gozlenen'] > NM['ort_yol']['null_ort'] else 'kısadır'}
(z = {s(nm_z['ort_yol'], 1)}); bu da toplulukların kendi içine kapanmasının bedelidir. Null model olmasaydı yüksek modülerliğin yalnızca derece dağılımından
kaynaklanıp kaynaklanmadığını söyleyemezdik.</p>

<h3>4.6 Karşılıklılık ve giriş/çıkış dengesizliği</h3>
<p>Kurum ağında kenarların {yuzde(KR['kurum_agirliksiz'], 1)}'i karşılıklıdır (A→B varken B→A da var), öğrenci akışının {yuzde(KR['kurum_agirlikli'], 1)}'i ise
karşılıklı kısma düşer. Ülke ağında bu oranlar {yuzde(KR['ulke_agirliksiz'], 1)} ve {yuzde(KR['ulke_agirlikli'], 1)}'dir: ülkeler arasında değişim büyük ölçüde iki yönlü,
kurumlar arasında ise çoğunlukla tek yönlüdür.</p>
<div class="iki"><div>{denge_tablo()}</div><div><figure style="margin-top:0"><img src="{img('fig/dengesizlik.png')}"><figcaption>Şekil 4. 34 ülkenin dengesizlik endeksi. Kırmızı: Türkiye.</figcaption></figure></div></div>
<p><b>Türkiye 34 ülke arasında en dengesiz gönderendir</b> (I = {s(TD['dengesizlik'], 3)}, {tr_sira}. sıra): {s(TD['giden'])} öğrenci gönderip {s(TD['gelen'])} öğrenci almıştır;
net {s(TD['net_giden'])} öğrenci "ihraç" etmiştir. İkinci sıradaki Romanya'nın endeksi {s(dp[1]['dengesizlik'], 3)}'tür. En güçlü alan ülkeler Malta, Lihtenştayn ve Lüksemburg'dur.
Türkiye'nin en büyük partnerleri Almanya ve Polonya'dır; Polonya'ya {s(R['tr_partnerler'][1]['giden'])} öğrenci gidip yalnızca {s(R['tr_partnerler'][1]['gelen'])} öğrenci gelmiştir.</p>

<h3>4.7 Çekim modeli</h3>
{cekim_tablo()}
<figure><img src="{img('fig/cekim_modeli.png')}"><figcaption>Şekil 5. Solda mesafe ve akış; sağda temel modelin beklediği ve gerçekleşen akış (kırmızı: Türkiye'den giden, mavi: Türkiye'ye gelen).</figcaption></figure>
<p>Temel model nüfus ve mesafeyle akışların büyük kısmını açıklar (sözde R² = {s(cek_t['pseudo_R2'], 2)}). Gönderen ülkenin nüfusu %1 arttığında beklenen akış yaklaşık
%{s(cek_t['katsayi']['ln_nufus_i'], 2)}, alan ülkenin nüfusu %1 arttığında %{s(cek_t['katsayi']['ln_nufus_j'], 2)} artar; mesafe %1 arttığında akış %{s(-cek_t['katsayi']['ln_mesafe'], 2)} azalır.
Avrupa içinde mesafenin etkisi, ticaret çekim modellerinde sık görülen −1 civarındaki değerlere göre zayıftır; bunun nedenini bu veriyle test edemiyoruz.</p>
<p><b>Türkiye modele uymaz.</b> Temel model, nüfusu {s(84.98, 1)} milyonla örneklemin en büyük ülkesi olan Türkiye'nin {s(trb['giden_beklenen'])} öğrenci göndermesini ve
{s(trb['gelen_beklenen'])} öğrenci almasını bekler; gerçekte {s(trb['giden_gercek'])} öğrenci gönderip {s(trb['gelen_gercek'])} öğrenci almıştır. TR kuklaları eklenince
gönderen katsayısı {s(cek_k['katsayi']['tr_kaynak'], 2)} (beklenenin {s(etk_kaynak, 2)} katı), alan katsayısı {s(cek_k['katsayi']['tr_hedef'], 2)} (beklenenin {s(etk_hedef, 2)} katı) çıkar ve
ikisi de anlamlıdır (z = {s(cek_k['z']['tr_kaynak'], 1)} ve {s(cek_k['z']['tr_hedef'], 1)}). Yani Türkiye büyüklüğüne göre ağa <i>az bağlıdır</i>; bu eksiklik alan tarafında çok daha
büyük olduğu için net gönderen konumuna düşer. Kuklalar eklenince mesafe katsayısı {s(cek_k['katsayi']['ln_mesafe'], 2)}'ye iner: temel modeldeki mesafe etkisinin bir kısmı,
hem uzak hem de az öğrenci alan Türkiye'den kaynaklanmaktadır.</p>

<h3>4.8 Yıllar arası değişim</h3>
{yillar_paragrafi()}
{yillar_tablosu()}

<h2>5. Tartışma</h2>
<p>Araştırma sorusunun ilk kısmının cevabı açıktır: Türkiye Erasmus ağında net bir gönderendir ve bu konumda 34 ülke arasında birinci sıradadır. İkinci kısmın cevabı
"büyük ölçüde evet, Türkiye için hayır"dır. Nüfus ve mesafe Avrupa içi akışların çoğunu açıklar, ancak Türkiye hem gönderen hem alan olarak bu büyüklükteki bir ülkeden
beklenenin çok altındadır. Çekim modelinde yer almayan etkenler (kişi başı gelir ve hibe miktarının yaşam maliyetine oranı, öğretim dili, vize ve akademik takvim) bu farkı
açıklamaya aday değişkenlerdir. Ağ yapısı tarafında, toplulukların kurum türüne göre oluşması Türk kurumlarının da kendi türlerindeki Avrupa kurumlarıyla bağ kurduğunu,
ancak alan tarafında bu bağların zayıf kaldığını gösterir. Bu bulgular ilişki gösterir; ağ verisinden nedensellik çıkarılamaz.</p>

<h2>6. Sınırlar</h2>
<ul>
<li><b>Ad sistemi:</b> Kurum ağı yalnızca 2021–2027 dönemi kayıtlarını kullanır ({s(v['kurum_agi_ogrenci'])} / {s(v['ogrenci'])} öğrenci). Aynı dönemde de bazı kurumlar hem kodla hem uzun adla yazılmıştır (ör. "METU" ve "MIDDLE EAST TECHNICAL UNIVERSITY"); bu küçük çiftlemeler düzeltilmedi.</li>
<li><b>Geçici veri:</b> Dosyalar "provisional data" etiketlidir; 2022 takvim yılı iki akademik yılın parçalarını içerir.</li>
<li><b>Örnekleme:</b> Ortalama yol, çap, betweenness ve closeness örneklemeyle hesaplandı; çap bir alt sınırdır.</li>
<li><b>Null model:</b> Configuration model ağırlık taşımaz; karşılaştırma ağırlıksız yapı üzerindedir.</li>
<li><b>Çekim modeli:</b> Yalnızca nüfus, başkentler arası mesafe ve Türkiye kuklaları kullanıldı; gelir, dil ve kontenjan gibi değişkenler yoktur. Örneklem 34 ülkedir.</li>
<li><b>Topluluk adları</b> bizim yorumumuzdur; algoritma ad vermez.</li>
{'' if y21 else '<li><b>Yıllar:</b> 2021 dosyası bu sürümde analize eklenemedi.</li>'}
</ul>

<h2>Kaynakça</h2>
<div class="kaynak">
<p>Avrupa Komisyonu, DG EAC (2024). <i>Erasmus+ Mobility Raw Data</i>. data.europa.eu. https://data.europa.eu/data/datasets/erasmus-mobility-raw-data</p>
<p>Blondel, V. D., Guillaume, J.-L., Lambiotte, R., Lefebvre, E. (2008). Fast unfolding of communities in large networks. <i>Journal of Statistical Mechanics</i>, P10008.</p>
<p>Clauset, A., Shalizi, C. R., Newman, M. E. J. (2009). Power-law distributions in empirical data. <i>SIAM Review</i>, 51(4), 661–703.</p>
<p>Dünya Bankası (2024). World Development Indicators: Population, total (SP.POP.TOTL). https://data.worldbank.org</p>
<p>Hagberg, A., Schult, D., Swart, P. (2008). Exploring network structure, dynamics, and function using NetworkX. <i>Proceedings of SciPy 2008</i>.</p>
<p>Santos Silva, J. M. C., Tenreyro, S. (2006). The log of gravity. <i>The Review of Economics and Statistics</i>, 88(4), 641–658.</p>
<p>Squartini, T., Picciolo, F., Ruzzenenti, F., Garlaschelli, D. (2013). Reciprocity of weighted networks. <i>Scientific Reports</i>, 3, 2729.</p>
<p>Traag, V. A., Waltman, L., van Eck, N. J. (2019). From Louvain to Leiden: guaranteeing well-connected communities. <i>Scientific Reports</i>, 9, 5233.</p>
<p>Vuong, Q. H. (1989). Likelihood ratio tests for model selection and non-nested hypotheses. <i>Econometrica</i>, 57(2), 307–333.</p>
</div>
<p class="kucuk" style="margin-top:5mm"><b>Yapay zekâ beyanı.</b> Kodun yazımında, analizlerin çalıştırılmasında ve bu raporun taslağında yapay zekâ asistanı (Claude) kullanılmıştır.
Veri kaynağı, yöntem seçimleri ve yorumlar tarafımdan gözden geçirilmiştir. Kod ve veri: github.com/Miremgecici/erasmus-hareketlilik-agi</p>
</body></html>"""
    open("rapor.html", "w", encoding="utf-8").write(html)
    print("rapor.html yazıldı")


if __name__ == "__main__":
    rapor()

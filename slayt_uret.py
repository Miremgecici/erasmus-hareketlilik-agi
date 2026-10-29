"""Sunum (16:9, 10 slayt) ve A3 poster HTML'lerini sonuclar.json'dan üretir."""
import io, base64, json, math
from PIL import Image
from rapor_uret import R, AD, TK, TU, DD, TOP, NM, KR, TD, CK, YIL, s, yuzde, mk, TA, BULGU_CUMLESI

def kucuk(yol, gen=1600):
    im = Image.open(yol).convert("RGB")
    if im.width > gen:
        im = im.resize((gen, round(im.height * gen / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

trb = CK["tr_beklenen"]; ck = CK["tr_kuklali"]
kat_gid = trb["giden_beklenen"] / trb["giden_gercek"]; kat_gel = trb["gelen_beklenen"] / trb["gelen_gercek"]
tr_ilk = mk["tr_ilk5_pagerank"][0]
PR = [x[0] for x in mk["ilk10"]["pagerank"]][:5]
LINK = "miremgecici.github.io/erasmus-hareketlilik-agi"
y21 = YIL.get(2021); y22 = YIL.get(2022)
renk = ["#2f6db5", "#d1495b", "#2a9d8f", "#e9a03b", "#7b5ea7", "#4d908e", "#c06c84", "#6a994e"]

# statik ağdaki renk sırası: görsel alt ağdaki topluluk büyüklüğüne göre
g = json.load(open("output/gorsel_ag.json", encoding="utf-8"))
say = {}
for d in g["dugumler"]:
    say[d["topluluk"]] = say.get(d["topluluk"], 0) + 1
sira = [c for c in sorted(say, key=lambda c: -say[c]) if str(c) in AD][:8]
LEJANT = "".join(f"<div style='display:flex;gap:8px;align-items:center;margin:4px 0'><span style='width:13px;height:13px;border-radius:50%;background:{renk[i]};flex:none'></span>{AD[str(c)]['tr']}</div>"
                 for i, c in enumerate(sira))


def slaytlar():
    S = []
    alt = lambda n: f"<div class='alt'><span>Müesser İrem Gecici · Sosyal Ağ Analizi · Erasmus+ öğrenci ağı</span><span>{n} / 10</span></div>"
    S.append(f"""<section class='s kapak'><div class='ust' style='color:#f1948a'>Sosyal Ağ Analizi · Dönem Ödevi</div>
<h1>Türkiye, Erasmus+ öğrenci ağının en dengesiz göndereni</h1>
<div class='not' style='max-width:900px'>Soru: Türkiye Erasmus ağında gönderen mi, alan mı? Akışlar mesafe ve ülke büyüklüğüyle açıklanabiliyor mu?</div>
<div class='not' style='margin-top:40px'>Müesser İrem Gecici · 2516016027 · Öğr. Gör. Osman Can Çetlenbik · 30 Ekim 2026</div></section>""")
    v = R["veri"]
    S.append(f"""<section class='s'><div class='ust'>Veri ve ağ kurma</div>
<h1>867 bin Erasmus kaydından {s(TK['dugum'])} kurumluk yönlü bir öğrenci ağı kurduk</h1>
<div class='akis'><div class='adim'><b>{s(v['ham_satir'])}</b>hareketlilik kaydı<br><span class='not'>data.europa.eu, 2022, script ile indirildi</span></div>
<div class='adim'><b>{s(v['ogrenci'])}</b>yükseköğretim öğrencisi<br><span class='not'>personel, okul, gençlik çıkarıldı</span></div>
<div class='adim'><b>{s(v['kurum_agi_ogrenci'])}</b>öğrenci, tek ad sistemi<br><span class='not'>2021–2027 dönemi kayıtları</span></div>
<div class='adim'><b>{s(TK['dugum'])} / {s(TK['kenar'])}</b>kurum / kenar<br><span class='not'>+ ülke ağı: {TU['dugum']} ülke, {s(TU['kenar'])} kenar</span></div></div>
<div class='govde' style='margin-top:26px'><div class='metin' style='flex:1'><ul>
<li><b>Düğüm:</b> üniversite ("ÜLKE | KURUM") · <b>Kenar:</b> gönderen → alan, <b>yönlü</b> · <b>Ağırlık:</b> öğrenci sayısı</li>
<li>Yönlü çünkü soru giden ile gelen arasındaki fark.</li>
<li><b>Ara kontrolden sonra bulduğumuz hata:</b> aynı üniversite iki adla geçiyordu ("UGR" ve "UNIVERSIDAD DE GRANADA"). Kurum ağını tek ad sistemiyle yeniden kurduk.</li></ul></div></div>{alt(2)}</section>""")
    S.append(f"""<section class='s'><div class='ust'>Temel yapı</div>
<h1>Ağ seyrek ama küçük bir dünya: iki kurum ortalama {s(TK['ort_en_kisa_yol'], 1)} adımla birbirine ulaşıyor</h1>
<div class='govde'><div class='kpi' style='width:330px;flex:none'>
<div class='k'><b>%{s(TK['yogunluk'] * 100, 2)}</b><span>yoğunluk: olası bağların binde 4'ü var</span></div>
<div class='k'><b>%{s(100 * TK['en_buyuk_zayif'] / TK['dugum'])}</b><span>kurum tek dev bileşende</span></div>
<div class='k'><b>%{s(100 * DD['derece1_orani'])}</b><span>kurumun yalnızca 1 partneri var</span></div>
<div class='k'><b>{s(TK['assortativity_yonsuz'], 2)}</b><span>derece benzeşimi: küçükler büyük merkezlere bağlanıyor</span></div></div>
<div style='flex:1;display:flex;flex-direction:column'><img src='{kucuk('fig/derece_dagilimi.png')}' style='max-height:440px'>
<div class='not' style='margin-top:8px'>Kuvvet yasası α = {s(DD['alpha'], 2)} (k ≥ {s(DD['xmin'])}), ama log-normalden ayırt edilemiyor (p = {s(DD['p_lognormal'], 2)}): kuyruk ağır, "ölçekten bağımsız" kanıtı yok.</div></div></div>{alt(3)}</section>""")
    satir = "".join(f"<tr><td class='n'>{i+1}</td><td>{k[5:]}</td><td>{k[:2]}</td></tr>" for i, k in enumerate(PR))
    S.append(f"""<section class='s'><div class='ust'>Merkeziyet</div>
<h1>Bologna her ölçüde birinci; en üstteki Türk kurumu PageRank'te ancak {s(tr_ilk[3])}. sırada</h1>
<div class='govde'><div style='width:430px;flex:none'><table><tr><th class='n'>#</th><th>PageRank ilk 5</th><th>Ülke</th></tr>{satir}
<tr class='vurgu'><td class='n'>{s(tr_ilk[3])}</td><td>{tr_ilk[0][5:]}</td><td>TR</td></tr></table></div>
<div class='metin' style='flex:1'><ul>
<li><b>PageRank ≈ çekicilik:</b> gelen öğrenciyle ρ = {s(mk['spearman']['pagerank']['gelen_ogrenci'], 2)}, giden öğrenciyle yalnızca ρ = {s(mk['spearman']['pagerank']['giden_ogrenci'], 2)}.</li>
<li>Çok gönderip az alan kurumlar PageRank'te geride kalıyor: Türk kurumlarının durumu bu.</li>
<li><b>Köprüler:</b> Ljubljana ve Zagreb betweenness'ta ilk 10'da; farklı toplulukları birbirine bağlıyorlar.</li>
<li>Ülke düzeyinde Türkiye: giden öğrencide <b>{int(R['ulke_tr']['giden_sira'])}.</b>, gelen öğrencide <b>{int(R['ulke_tr']['gelen_sira'])}.</b></li></ul></div></div>{alt(4)}</section>""")
    S.append(f"""<section class='s'><div class='ust'>Topluluklar (Leiden)</div>
<h1>Topluluklar ülkeye göre değil kurum türüne göre ayrışıyor</h1>
<div class='govde'><div style='flex:1;display:flex;justify-content:center'><img src='{kucuk('fig/ag_statik.png', 1300)}' style='max-height:530px'></div>
<div style='width:430px;flex:none;font-size:17px'>{LEJANT}
<div class='not' style='margin-top:16px'>Modülerlik Q = {s(TOP['leiden']['Q_ort'], 2)} · 10 tohumda NMI = {s(TOP['leiden']['NMI_ort'], 2)} · Louvain ile NMI = {s(TOP['louvain_vs_leiden']['NMI'], 2)}.
Teknik üniversiteler (İTÜ, ODTÜ, YTÜ dahil) bir arada; Türk kurumlarının çoğu ({R['tr_topluluklar'][0][1]}) Akdeniz ekseninde. Siyah halka: Türk kurumu.</div></div></div>{alt(5)}</section>""")
    S.append(f"""<section class='s'><div class='ust'>Null model · 100 rastgele ağ</div>
<h1>Bu yapı rastlantı değil: modülerlikte z = {s(NM['modulerlik']['z'])}, karşılıklılıkta z = {s(NM['karsiliklilik']['z'])}</h1>
<div style='flex:1;display:flex;flex-direction:column;justify-content:center'><img src='{kucuk('fig/null_model.png', 1900)}'>
<div class='metin' style='margin-top:22px;font-size:19px'><ul>
<li>Aynı derece dizisine sahip 100 configuration model ağıyla karşılaştırdık.</li>
<li>Gözlenen modülerlik {s(NM['modulerlik']['gozlenen'], 3)}, rastgele ağlarda {s(NM['modulerlik']['null_ort'], 3)}: topluluklar "büyük kurum her yere bağlı" olmasından kendiliğinden çıkmıyor.</li>
<li>Null model olmasaydı yüksek modülerliğin yalnızca derece dağılımından gelip gelmediğini söyleyemezdik.</li></ul></div></div>{alt(6)}</section>""")
    S.append(f"""<section class='s'><div class='ust'>İleri yöntem 1 · Karşılıklılık ve dengesizlik</div>
<h1>Türkiye 34 ülkenin en dengesiz göndereni: her 1 gelen öğrenciye {s(TD['oran'], 1)} giden</h1>
<div class='govde'><div class='kpi' style='width:300px;flex:none'>
<div class='k kirmizi'><b>{s(TD['giden'])}</b><span>Türkiye'den giden</span></div>
<div class='k mavi'><b>{s(TD['gelen'])}</b><span>Türkiye'ye gelen</span></div>
<div class='k'><b>{s(TD['dengesizlik'], 2)}</b><span>(giden − gelen) / (giden + gelen)<br>2. sıradaki Romanya: {s(R['dengesizlik_tablosu'][1]['dengesizlik'], 2)}</span></div></div>
<div style='flex:1;display:flex;flex-direction:column'><img src='{kucuk('fig/dengesizlik.png')}' style='max-height:400px'>
<div class='not' style='margin-top:10px'>Karşılıklılık: kurum bağlarının %{s(100 * KR['kurum_agirliksiz'])}'si, ülke bağlarının %{s(100 * KR['ulke_agirliksiz'])}'i iki yönlü. Polonya'ya {s(R['tr_partnerler'][1]['giden'])} öğrenci gidip {s(R['tr_partnerler'][1]['gelen'])} öğrenci geliyor.</div></div></div>{alt(7)}</section>""")
    S.append(f"""<section class='s'><div class='ust'>İleri yöntem 2 · Çekim modeli (PPML, 34 ülke)</div>
<h1>Nüfus ve mesafe akışların çoğunu açıklıyor; Türkiye ise beklenenin çok altında kalıyor</h1>
<div class='govde'><div style='flex:1'><img src='{kucuk('fig/tr_beklenen.png')}' style='max-height:470px'></div>
<div class='metin' style='width:440px;flex:none;font-size:18px'>
<p style='background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 14px;font-size:16px'>Akış<sub>ij</sub> ∝ Nüfus<sub>i</sub><sup>{s(CK['temel']['katsayi']['ln_nufus_i'], 2)}</sup> × Nüfus<sub>j</sub><sup>{s(CK['temel']['katsayi']['ln_nufus_j'], 2)}</sup> × Mesafe<sup>{s(CK['temel']['katsayi']['ln_mesafe'], 2)}</sup><br><span class='not'>sözde R² = {s(CK['temel']['pseudo_R2'], 2)}</span></p>
<ul><li>Model Türkiye'den <b>{s(trb['giden_beklenen'])}</b> giden bekliyor, gerçek <b>{s(trb['giden_gercek'])}</b> (≈{s(kat_gid, 1)} kat az).</li>
<li>Gelen için <b>{s(trb['gelen_beklenen'])}</b> bekliyor, gerçek <b>{s(trb['gelen_gercek'])}</b> (≈{s(kat_gel, 1)} kat az).</li>
<li>TR kuklaları anlamlı: gönderen z = {s(ck['z']['tr_kaynak'], 1)}, alan z = {s(ck['z']['tr_hedef'], 1)}.</li></ul></div></div>{alt(8)}</section>""")
    if y21:
        S.append(f"""<section class='s'><div class='ust'>İleri yöntem 3 · Yıllar arası değişim</div>
<h1>2021'den 2022'ye Türkiye'nin giden/gelen oranı {s(y21['tr_oran'], 2)}'den {s(y22['tr_oran'], 2)}'e</h1>
<div style='flex:1'><img src='{kucuk('fig/yillar.png', 1900)}' style='max-height:470px'></div>{alt(9)}</section>""")
    else:
        S.append(f"""<section class='s'><div class='ust'>Canlı gösterim</div>
<h1>Etkileşimli ağda Ege Üniversitesi: 295 giden, 78 gelen öğrenci</h1>
<div class='govde'><div style='flex:1'><img src='{kucuk('fig/etkilesimli_ege.png', 1700)}' style='max-height:480px;border:1px solid var(--line);border-radius:8px'></div>
<div class='metin' style='width:330px;flex:none;font-size:18px'><ul><li>Arama, kuruma tıklayınca detay paneli, topluluk filtresi, TR/EN.</li>
<li>Kırmızı: giden · mavi: gelen öğrenci.</li><li>En büyük 600 kurum (kurum ağındaki akışın %{s(100 * R['gorsel']['akis_payi'])}'ı).</li></ul>
<div class='not' style='margin-top:14px'>{LINK}</div></div></div>{alt(9)}</section>""")
    S.append(f"""<section class='s'><div class='ust'>Cevap ve sınırlar</div>
<h1>Türkiye net gönderen; ama büyüklüğüne göre ağa az bağlı ve en çok alan tarafında eksik</h1>
<div class='govde'><div class='metin' style='flex:1'><p><b>Cevap</b></p><ul>
<li>Gönderen mi alan mı? <b>Gönderen</b>: {s(TD['giden'])} giden, {s(TD['gelen'])} gelen; 34 ülke içinde en dengesiz.</li>
<li>Mesafe ve büyüklük açıklıyor mu? <b>Avrupa için büyük ölçüde evet, Türkiye için hayır</b>: model Türkiye'den yaklaşık {s(kat_gel, 0)} kat fazla gelen öğrenci bekliyor.</li></ul></div>
<div class='metin' style='flex:1;font-size:18px'><p><b>Sınırlar</b></p><ul>
<li>Kurum adları iki sistemde yazılmış; kurum ağı 2021–2027 kayıtlarıyla sınırlı.</li>
<li>Veri "geçici"; ortalama yol ve betweenness örneklemeyle.</li>
<li>Çekim modelinde gelir, dil, vize yok; bulgular ilişki gösterir, nedensellik değil.</li></ul></div></div>{alt(10)}</section>""")
    html = f"<!doctype html><html lang='tr'><head><meta charset='utf-8'><title>Erasmus+ Ağı Sunum</title><link rel='stylesheet' href='slayt_stil.css'></head><body>{''.join(S)}</body></html>"
    open("sunum.html", "w", encoding="utf-8").write(html)
    print("sunum.html yazıldı,", len(S), "slayt")


def poster():
    html = f"""<!doctype html><html lang='tr'><head><meta charset='utf-8'><title>Erasmus+ Ağı Poster</title><style>
@page {{ size: A3; margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: "DejaVu Sans", Arial, sans-serif; color: #1d232b; }}
.p {{ width: 297mm; height: 419mm; overflow: hidden; padding: 14mm 14mm 10mm; display: flex; flex-direction: column; background: #fbfaf8; }}
.bas {{ border-bottom: 2px solid #1d232b; padding-bottom: 5mm; margin-bottom: 5mm; }}
.ust {{ font-size: 10pt; letter-spacing: .08em; text-transform: uppercase; color: #c0392b; font-weight: 700; }}
h1 {{ font-size: 28pt; line-height: 1.12; margin: 2mm 0 3mm; }}
.alt-bas {{ font-size: 11pt; color: #5f6670; }}
.ana {{ display: flex; flex-direction: column; gap: 5mm; flex: 1; min-height: 0; }}
.ag {{ background: #fff; border: 1px solid #e3e1dc; border-radius: 3mm; padding: 4mm; display: grid; grid-template-columns: 1fr 62mm; grid-template-rows: auto minmax(0, 1fr); gap: 2mm 5mm; height: 200mm; flex: none; }}
.ag .bas2 {{ grid-column: 1 / -1; }} .ag .yan {{ display: flex; flex-direction: column; justify-content: center; }}
.ag img {{ width: 100%; height: 100%; object-fit: contain; min-height: 0; }}
.lej {{ display: flex; flex-direction: column; gap: 2.2mm; font-size: 9.5pt; }}
.lej div {{ display: flex; gap: 2mm; align-items: center; }} .lej span {{ width: 3.2mm; height: 3.2mm; border-radius: 50%; flex: none; }}
.kol {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5mm; flex: 1; min-height: 0; }}
.kutu {{ background: #fff; border: 1px solid #e3e1dc; border-radius: 3mm; padding: 4mm 5mm; }}
.kutu h2 {{ font-size: 13pt; margin: 0 0 2mm; line-height: 1.25; }}
.kutu p, .kutu li {{ font-size: 9.8pt; line-height: 1.4; margin: 0 0 1.5mm; }}
.kutu ul {{ margin: 0; padding-left: 4.5mm; }}
.kutu img {{ width: 100%; max-height: 58mm; object-fit: contain; display: block; margin-top: 2mm; }}
.sayi {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; margin-top: 2mm; }}
.sayi div {{ background: #f3f2ef; border-radius: 2mm; padding: 2.5mm; font-size: 8.5pt; color: #5f6670; }}
.sayi b {{ display: block; font-size: 17pt; color: #1d232b; font-variant-numeric: tabular-nums; }}
.kir b {{ color: #c0392b !important; }} .mav b {{ color: #2471a3 !important; }}
.ayak {{ display: flex; justify-content: space-between; font-size: 8.5pt; color: #5f6670; border-top: 1px solid #dcdad5; padding-top: 3mm; margin-top: 5mm; }}
</style></head><body><div class='p'>
<div class='bas'><div class='ust'>Sosyal Ağ Analizi · Erasmus+ Öğrenci Hareketliliği Ağı · 2022</div>
<h1>Türkiye Erasmus+ ağının en dengesiz göndereni ve büyüklüğüne göre ağa az bağlı</h1>
<div class='alt-bas'>Müesser İrem Gecici · 2516016027 · Manisa Celal Bayar Üniversitesi, Büyük Veri Analistliği · Öğr. Gör. Osman Can Çetlenbik</div><div style='font-size:10.5pt;margin-top:3mm;line-height:1.45'><b>Soru:</b> Türkiye Erasmus ağında gönderen mi, alan mı? Akışlar mesafe ve ülke büyüklüğüyle açıklanabiliyor mu? <b>Veri:</b> data.europa.eu Erasmus+ 2022 KA1, {s(R['veri']['ham_satir'])} kayıt → {s(R['veri']['ogrenci'])} yükseköğretim öğrencisi. <b>Ağ:</b> yönlü, öğrenci sayısıyla ağırlıklı; {s(TK['dugum'])} kurum / {s(TK['kenar'])} kenar ve {TU['dugum']} ülke / {s(TU['kenar'])} kenar.</div></div>
<div class='ana'>
<div class='ag'><div class='bas2'><div style='font-size:13pt;font-weight:700;margin-bottom:1mm'>Topluluklar ülkeye göre değil, kurum türüne göre ayrışıyor</div>
<div style='font-size:9.5pt;color:#5f6670'>Öğrenci hacmine göre en büyük {R['gorsel']['dugum']} kurum · renk: Leiden topluluğu · daire: giden + gelen öğrenci · siyah halka: Türk kurumu · çizgi: her kurumun en güçlü 6 bağı</div>
</div><div style='min-height:0'><img src='{kucuk('fig/ag_statik.png', 2600)}'></div>
<div class='yan'><div class='lej'>{''.join(f"<div><span style='background:{renk[i]}'></span>{AD[str(c)]['tr']}</div>" for i, c in enumerate(sira))}</div>
<div style='font-size:9pt;color:#5f6670;margin-top:2.5mm'>Leiden modülerlik Q = {s(TOP['leiden']['Q_ort'], 3)}; 10 tohumda ortalama NMI = {s(TOP['leiden']['NMI_ort'], 2)}, ARI = {s(TOP['leiden']['ARI_ort'], 2)}; Louvain ile NMI = {s(TOP['louvain_vs_leiden']['NMI'], 2)}.</div></div></div>
<div class='kol'>
<div class='kutu'><h2>Türkiye: her 1 gelen öğrenciye {s(TD['oran'], 1)} giden</h2>
<div class='sayi'><div class='kir'><b>{s(TD['giden'])}</b>giden</div><div class='mav'><b>{s(TD['gelen'])}</b>gelen</div><div><b>{s(TD['dengesizlik'], 2)}</b>dengesizlik endeksi, 34 ülkede 1.</div></div>
<img src='{kucuk('fig/dengesizlik.png', 1400)}'></div>
<div class='kutu'><h2>Çekim modeli Türkiye'den ~{s(kat_gel, 0)} kat fazla gelen öğrenci bekliyor</h2>
<p>PPML, 34 ülke, {s(CK['ornek']['cift'])} yönlü çift: nüfus ve mesafe akışların çoğunu açıklıyor (sözde R² = {s(CK['temel']['pseudo_R2'], 2)}). Türkiye için beklenen {s(trb['giden_beklenen'])} giden / {s(trb['gelen_beklenen'])} gelen; gerçek {s(trb['giden_gercek'])} / {s(trb['gelen_gercek'])}. TR kuklaları anlamlı (z = {s(ck['z']['tr_kaynak'], 1)} ve {s(ck['z']['tr_hedef'], 1)}).</p>
<img src='{kucuk('fig/tr_beklenen.png', 1400)}'></div>
<div class='kutu'><h2>Yapı rastlantı değil</h2><ul>
<li>100 configuration model ağına göre modülerlik z = {s(NM['modulerlik']['z'])}, geçişlilik z = {s(NM['gecislilik']['z'])}, karşılıklılık z = {s(NM['karsiliklilik']['z'])}.</li>
<li>Küçük dünya: iki kurum ortalama {s(TK['ort_en_kisa_yol'], 1)} adımda bağlı; kurumların %{s(100 * DD['derece1_orani'])}'ının tek partneri var.</li>
<li>Bologna (UNIBO) derece, PageRank ve betweenness'ta birinci.</li></ul><img src='{kucuk('fig/null_model.png', 1600)}'></div>
</div></div>
<div class='ayak'><span>Kod, veri, etkileşimli ağ: github.com/Miremgecici/erasmus-hareketlilik-agi · {LINK}</span><span>Kaynak: Avrupa Komisyonu DG EAC, Erasmus+ Mobility Raw Data · Dünya Bankası SP.POP.TOTL</span></div>
</div></body></html>"""
    open("poster.html", "w", encoding="utf-8").write(html)
    print("poster.html yazıldı")


if __name__ == "__main__":
    slaytlar(); poster()

# Erasmus+ Öğrenci Hareketliliği Ağı

**Sosyal Ağ Analizi dönem ödevi** · Müesser İrem Gecici (2516016027) · Manisa Celal Bayar Üniversitesi, Büyük Veri Analistliği · Öğr. Gör. Osman Can Çetlenbik

> **Bulgu (tek cümle):** Türkiye 2022'de Erasmus+ ağının en dengesiz göndereni: 16.214 öğrenci gönderip 6.045 öğrenci aldı (oran 2,68); nüfus ve mesafeye dayalı çekim modeli ise Türkiye'nin büyüklüğüne göre hem daha az gönderdiğini hem de çok daha az öğrenci aldığını gösteriyor.

> **CV cümlesi:** Avrupa Komisyonu'nun 867 bin kayıtlık Erasmus+ verisinden 13 bin kurumluk yönlü bir hareketlilik ağı kurdum; topluluk tespiti, null model testleri ve PPML çekim modeliyle Türkiye'nin ağdaki konumunu analiz ettim (Python, networkx).

🔗 **Etkileşimli ağ:** https://miremgecici.github.io/erasmus-hareketlilik-agi/ (arama, detay paneli, topluluk filtresi, TR/EN)

## Araştırma sorusu
Türkiye Erasmus ağında "gönderen" mi "alan" mı? Akışlar mesafe ve ülke büyüklüğüyle açıklanabiliyor mu?

## Temel sonuçlar (2022)

| | Değer |
|---|---|
| Kurum ağı | 13.167 düğüm, 69.839 yönlü kenar, yoğunluk 0,00040 |
| Ülke ağı | 176 düğüm, 3.060 kenar, yoğunluk 0,099 |
| Türkiye | 16.214 giden / 6.045 gelen öğrenci, dengesizlik 0,457 (34 ülkede 1.) |
| Çekim modeli (PPML) | Türkiye için beklenen 36.569 giden / 27.606 gelen; gerçek 16.037 / 5.603 |
| Topluluklar | Leiden Q = 0,331, 10 tohumda NMI = 0,84; ülkeye değil kurum türüne göre ayrışma |
| Null model (100 ağ) | modülerlik z = 107,7, kümelenme z = 18,6, karşılıklılık z = 171,1 |

## Depo yapısı

| Yol | İçerik |
|---|---|
| `analiz.ipynb` | Çalıştırılmış analiz defteri (tüm adımlar ve çıktıları) |
| `analiz.py` | Defterin kaynağı (`# %%` hücreleri) |
| `ara_kontrol.py` | 26 Ekim ara kontrol scripti (ilk sürüm; final analiz `analiz.ipynb`) |
| `requirements.txt` | Python paketleri |
| `data/external/ulkeler_worldbank_2022.csv` | Dünya Bankası nüfus ve başkent koordinatları |
| `data/processed/ogrenci_2022.csv.gz` | Süzülmüş yükseköğretim öğrenci kayıtları |
| `output/kenar_listesi_kurum_2022.csv`, `output/kenar_listesi_ulke_2022.csv` | Kenar listeleri |
| `output/ag_kurum_2022.graphml`, `output/ag_ulke_2022.graphml` | GraphML (Gephi'de açılabilir) |
| `output/merkeziyet_*.csv`, `output/dengesizlik_ulke_2022.csv`, `output/turkiye_partnerler_2022.csv` | Merkeziyet, dengesizlik, Türkiye partnerleri |
| `output/sonuclar.json` | Rapor ve görsellerdeki tüm sayılar |
| `output/onbellek_*.json` | Topluluk ve null model sonuçları (silinirse yeniden hesaplanır) |
| `output/topluluk_adlari.json` | Topluluklara verdiğimiz adlar |
| `fig/` | Şekiller |
| `docs/` | Etkileşimli ağ (GitHub Pages) |
| `rapor/` | Rapor (PDF), sunum (PDF) ve A3 poster (PDF) |
| `rapor_uret.py`, `slayt_uret.py`, `statik_ag.py`, `gorsel_uret.py`, `gorsel_sablon.html`, `pdf_yap.js`, `*.css` | Rapor, sunum, poster ve etkileşimli ağı üreten scriptler |
| `notebook_calistir.py` | `analiz.py`'yi çalıştırıp çıktılı `analiz.ipynb` üretir |

## Çalıştırma

```bash
pip install -r requirements.txt
python notebook_calistir.py analiz.py analiz.ipynb   # veya analiz.ipynb'yi Jupyter/Colab'da çalıştırın
```

Ham Excel (~72 MB) depoda yoktur; defter `data/raw/` altında bulamazsa kaynaktan indirir. Tüm rastgele işlemler `SEED = 42` ile sabittir.
Topluluk ve null model hesapları birkaç dakika sürer; sonuçlar `output/onbellek_*.json` dosyalarına yazılır ve yeniden çalıştırmada oradan okunur. Baştan hesaplamak için bu dosyaları silin.

Görselleri yeniden üretmek için: `python gorsel_uret.py` (etkileşimli ağ), `python statik_ag.py` (poster ağı), `python rapor_uret.py` ve `python slayt_uret.py` (HTML), ardından `node pdf_yap.js rapor.html rapor/rapor.pdf A4`, `node pdf_yap.js sunum.html rapor/sunum.pdf slayt`, `node pdf_yap.js poster.html rapor/poster.pdf A3`.

## Veri sözlüğü

**Kaynak:** [Erasmus+ Mobility Raw Data](https://data.europa.eu/data/datasets/erasmus-mobility-raw-data), Avrupa Komisyonu DG EAC, dosya `Erasmus-KA1-Mobility-Data-2022.xlsx` (867.767 satır). **Lisans:** European Commission reuse notice (Karar 2011/833/AB); dosyalar "provisional data" etiketlidir. **Toplama tarihi:** 26 Ekim 2026.
Nüfus ve başkentler: [Dünya Bankası API](https://api.worldbank.org) (SP.POP.TOTL, 2022; CC BY 4.0).

Kullanılan ham sütunlar: `Field` (eğitim alanı), `Participant Profile` (öğrenci/personel), `Activity (mob)` (faaliyet; `HE-…` kodları 2021–2027 dönemi), `Sending Country`, `Sending Organization`, `Receiving Country`, `Receiving Organization`, `Actual Participants (Contracted Projects)` (kişi sayısı).

`data/processed/ogrenci_2022.csv.gz`

| Sütun | Anlamı |
|---|---|
| `kaynak_ulke`, `hedef_ulke` | Gönderen / alan ülke kodu (ilk iki harf; Yunanistan `EL`, Birleşik Krallık `UK`) |
| `kaynak_kurum`, `hedef_kurum` | Kurum adı (boşluk temizlenmiş, büyük harf) |
| `faaliyet` | Faaliyet türü |
| `kisi` | Satırdaki öğrenci sayısı |
| `toplam_satir` | Ham dosyadaki toplam satır (bilgi amaçlı) |

Kenar listeleri: `source` (gönderen düğüm), `target` (alan düğüm), `weight` (öğrenci sayısı). Kurum düğümü `ÜLKE | KURUM` biçimindedir.

`output/merkeziyet_kurum_2022.csv`: `derece` (farklı partner sayısı), `gelen_ogrenci`, `giden_ogrenci`, `betweenness` (1.000 kaynakla örneklenmiş, yönlü), `pagerank` (ağırlıklı), `closeness` (en yüksek dereceli 2.000 kurum için), `ulke`.

## Ağ kurma kararları
- Yalnızca yükseköğretim öğrencileri (`Field = Higher Education`, `Participant Profile = Learner(s)`): 365.590 öğrenci.
- Yönlü (gönderen → alan) ve öğrenci sayısıyla ağırlıklı; ülke içi akışlar çıkarıldı.
- 2022 dosyasında aynı kurum iki ad sistemiyle geçer (2014–2020 projelerinde uzun ad, 2021–2027'de kısa kod). Kurum ağı bu yüzden yalnızca 2021–2027 dönemi kayıtlarıyla kuruldu (193.465 öğrenci); ülke ağı tüm kayıtları kullanır.
- Ağ 500 düğüm şartını örneklemesiz karşılar. Etkileşimli görünüm öğrenci hacmine göre en büyük 600 kurumu gösterir (kurum ağındaki akışın %69,2'i).

## Sınırlar
Geçici veri; kurum adlarında kalan küçük çiftlemeler; ortalama yol, çap, betweenness ve closeness örneklemeyle; çekim modelinde yalnızca nüfus, mesafe ve Türkiye kuklaları var. Bulgular ilişki gösterir, nedensellik iddiası taşımaz.

## Yapay zekâ beyanı
Bu projede kodun yazımı, analizlerin çalıştırılması, görsellerin ve rapor taslağının hazırlanmasında yapay zekâ asistanı (Anthropic Claude) kullanılmıştır. Veri kaynağı, ağ kurma kararları ve yorumlar tarafımdan gözden geçirilmiştir.

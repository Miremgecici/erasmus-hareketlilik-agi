# Sosyal Ağ Analizi – Ara Kontrol (26 Ekim 2026)

**Öğrenci:** Müesser İrem Gecici · 2516016027
**Proje:** Erasmus+ Öğrenci Hareketliliği Ağı

## Dosyalar

| Dosya | İçerik |
|---|---|
| `requirements.txt` | Gerekli Python paketleri |
| `ara_kontrol.py` | Veriyi kaynaktan indiren, filtreleyen, ağı kuran ve istatistikleri hesaplayan script |
| `output/kenar_listesi_kurum_2022.csv` | Kurum düzeyi yönlü, ağırlıklı kenar listesi (ana ağ) |
| `output/kenar_listesi_ulke_2022.csv` | Ülke düzeyi yönlü, ağırlıklı kenar listesi |
| `output/temel_istatistikler_2022.csv` | Düğüm, kenar, yoğunluk, bileşen sayıları |
| `output/ag_kurum_2022.graphml`, `output/ag_ulke_2022.graphml` | Ağların GraphML biçimi |

## Veri kaynağı

- **Kaynak:** data.europa.eu – *Erasmus+ Mobility Raw Data*, KA1 2022 dosyası
  (https://data.europa.eu/data/datasets/erasmus-mobility-raw-data)
- **Yayımlayan:** Avrupa Komisyonu, DG EAC
- **Lisans:** European Commission reuse notice / provisional data
- **Toplama tarihi:** 26 Ekim 2026
- Ham Excel dosyası (~72 MB, 867.767 satır) boyutu nedeniyle eklenmemiştir; `ara_kontrol.py` dosyası veriyi kaynaktan otomatik indirir.

## Ağ tanımı

- **Filtre:** Yalnızca yükseköğretim (`Field = Higher Education`) öğrencileri (`Participant Profile = Learner`) alındı. Personel, gençlik, okul ve mesleki eğitim kayıtları çıkarıldı. Bu filtreden sonra 349.634 satır ve 365.590 öğrenci kaldı.
- **Düğüm:** Kurum ağında *"ülke kodu | kurum adı"*, ülke ağında ülke kodu. Ülke kodu, farklı ülkelerdeki aynı adlı kurumların karışmasını önler.
- **Kenar:** Gönderen → alan yönünde öğrenci akışı. Ağ **yönlüdür**, çünkü gitmek ile gelmek farklı şeylerdir ve araştırma sorusu tam olarak bu farkı soruyor.
- **Ağırlık:** Öğrenci sayısı (`Actual Participants`).
- **Çıkarılanlar:** Kurum adı boş ("-") olan 72.147 satır kurum ağına alınmadı (ülke ağında kullanıldı). Ülke ağında aynı ülke içindeki 12 akış (öz-döngü) çıkarıldı.

## Temel istatistikler (2022)

| Ölçü | Kurum ağı | Ülke ağı |
|---|---|---|
| Düğüm sayısı | 36.609 | 176 |
| Kenar sayısı | 124.112 | 3.060 |
| Toplam öğrenci (ağırlık) | 290.073 | 365.550 |
| Yoğunluk | 0,000093 | 0,0994 |
| Zayıf bağlı bileşen | 865 | 1 |
| En büyük zayıf bileşen | 33.206 düğüm | 176 düğüm |
| Güçlü bağlı bileşen | 33.283 | 44 |
| En büyük güçlü bileşen | 3.307 düğüm | 133 düğüm |

**Kısa yorum:**
- Ülke ağının yoğunluğu yaklaşık 0,10. Yani olası ülke çiftlerinin yaklaşık onda biri arasında öğrenci akışı var.
- Kurum ağı çok seyrek. Kurumların büyük çoğunluğu (%91) tek bir büyük zayıf bileşende toplanıyor.
- Güçlü bileşen sayısının yüksek olması, birçok kurumun yalnızca gönderen ya da yalnızca alan olduğunu gösteriyor; karşılıklı değişim sınırlı.
- **İlk bulgu:** Türkiye 2022'de 16.214 öğrenci göndermiş, 6.045 öğrenci almış. Giden/gelen oranı 2,68, yani Türkiye net bir *gönderen* ülke.

## Çalıştırma

```
pip install -r requirements.txt
python ara_kontrol.py
```

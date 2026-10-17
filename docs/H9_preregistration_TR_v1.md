# Önceden Kayıt — H9: Sinir ağı tarafına eşit emek

**Çalışma:** GNN ile kriging tabanlı yöntemlerin heterotopik ortamda karşılaştırılması
**Yazar:** Kaan Erarslan (Kütahya Dumlupınar Üniversitesi)
**Kayıt tarihi:** 13 Ekim 2026 (yükleme zaman damgası esas alınır)
**İlgili kod:** `GNN_Jura_Asama0-5_H4_v9.ipynb`, Hücre 70–72

## 1. Gerekçe

Önceki aşamalarda GNN-K'nın kazandığı durumlarda klasik tarafa yeni rakipler eklendi (KED-lin, KED-spline, KED-log, KED-sel). Sinir ağı tarafında ise GNN-K değişmedi: gizli boyut 64'te sabit, ayar ızgarası dar. H9 bu emek asimetrisini kapatır. Sinir ağı tarafına altı yeni aday eklenir ve iç katlarda seçilen `GNN-sel`, iç katlarda seçilen `KED-sel` ile yarışır.

## 2. Bu kayıttan önce görülenler

- H9 adaylarının hiçbirinin hata (MAE) sonucu görülmedi.
- Kodun çalıştığını doğrulamak için Meuse, Zn, ilk iki dış katta altı aday koşuldu. Yalnız seçilen hiperparametreler ve süreler görüldü; tahmin hataları incelenmedi. Bu duman testleri asıl koşuya girmez (ayrı klasöre yazıldı).
- Mevcut sonuçlar biliniyor: Jura ve Meuse'da GNN-K, KED-lin, KED-sel ve RK sonuçları (Aşama 4g, 4h, 4j).

## 3. Veri ve protokol

- **Veri:** Jura (359 nokta; hedefler Zn, Cd, Cu, Pb; yardımcılar diğer altı metal) ve Meuse (155 nokta; hedefler Zn, Cd, Cu, Pb; yardımcılar dist, ffreq, soil).
- **Doğrulama:** Tekrarlı çapraz doğrulama, 5 tekrar × 5 kat, her dış eğitim kümesinde 4 iç kat. Kat dosyaları önceki aşamalarla aynı. Jura kanonik bölmesi bu aşamada koşulmaz.
- **Ölçüt:** MAE (orijinal ölçek).

## 4. Adaylar (sinir ağı tarafı)

Hepsi aynı bilgiyi kullanır: koordinatlar, hedef noktada bilinen yardımcılar ve eğitim noktalarındaki hedef değerleri. Hiçbir aday KED'in görmediği bir bilgiyi kullanmaz.

| # | Ad | Tanım |
|---|---|---|
| 1 | GNN-K | Mevcut. Komşu hedefleri, geometri ve softmax dikkat (KCN ailesi). |
| 2 | GNN-GAT | Standart iki katmanlı graf dikkat ağı. Komşu hedeflerini görmez. |
| 3 | GNN-K-PE | GNN-K ve çok ölçekli sinüzoidal konum kodlaması (16 boyut). |
| 4 | GNN-K-L | Gizli boyut 128, k ∈ {16, 32}, eğitimde %20 komşu düşürme, 10 tohumlu topluluk. |
| 5 | GNN-K-cov | Kenar özniteliklerine, eğitim verisinden uydurulan variogramla ρ(d) ve komşu kümesindeki OK ağırlığı eklenir. |
| 6 | GNN-KED | Sürüklenme [1, yardımcılar] GLS ile (KED ile aynı); artık GNN-K ile öğrenilir. |
| 7 | NN-GLS | Yalnız yardımcılardan MLP ortalama, GLS (beyazlatılmış) kayıpla; ardından artığın OK'si. |

## 5. Eşitlik kuralları

- Her adayın ızgarası 8 yapılandırma (dropout {0,1; 0,3} × dönüşüm {ham, log} × üçüncü bir boyut: k, ya da NN-GLS için gizli boyut) ve aynı epoch ızgarası (20, 40, …, 200).
- Yapılandırma ve epoch yalnız iç katlarda, iç kat MAE'siyle seçilir.
- Dış tahmin 5 tohumlu topluluk (GNN-K-L: 10).
- **GNN-sel:** Her dış katta yedi aday arasından iç kat MAE'si en düşük olan.
- **KED-sel:** Önceki aşamadaki tanım (KED-lin/KED-spline × ham/log, iç katlarda seçim).

## 6. Analizler

**H9-1 (birincil).** GNN-sel vs KED-sel; 8 hedef-veri (Jura 4 + Meuse 4); nokta bazında eşleştirilmiş Wilcoxon (çift yönlü); Holm düzeltmesi. Yön öngörüsü yoktur. Karar kuralı:

- (a) GNN-sel MAE ≤ KED-sel en az 6/8'de **ve** KED-sel'in anlamlı üstün olduğu hedef yok → "sinir ağı tarafı gerçek veride en az eşit".
- (b) KED-sel en az 2/8'de anlamlı üstün **ve** GNN-sel hiçbirinde anlamlı üstün değil → "klasik taraf üstün".
- (c) Diğer durumlar → "karışık / hedefe bağlı".

**H9-2 (keşifsel).** Her aday tek tek KED-sel'e karşı (7 × 8 = 56 test, Holm). Önceden belirlenmiş tek varyantlar (GNN-K, KED-lin) seçim yanlılığına karşı her zaman ayrıca raporlanır.

**H9-3 (keşifsel).** Ort = (GNN-sel + KED-sel) / 2, sabit eşit ağırlıkla; KED-sel'e karşı.

**Ek raporlar.** Hangi adayın kaç dış katta seçildiği; her adayın MAE tablosu.

## 7. Raporlama taahhüdü

Sonuç hangi yönde çıkarsa çıksın yayımlanacaktır. Bu kayıttan sonra yapılan her değişiklik (hata düzeltmesi dahil) tarihiyle birlikte ayrıca belirtilecektir.

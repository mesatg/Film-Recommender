Bu proje, Flask ve Makine Öğrenimi kullanarak film önerileri sunan bir web uygulamasıdır. Kullanıcılar bir film adı girerek, benzer filmleri görüntüleyebilir. Makine öğrenimi modeli Google Colab üzerinde eğitilmiş ve kaydedilmiştir.

Dosya Açıklamaları

🔹 Web Uygulaması (Flask + JavaScript + HTML + CSS)

app.py → Flask ile web uygulamasını çalıştırır, modeli yükler ve film önerileri sunar.
script.js → Otomatik tamamlama ve önerilen filmlerin gösterilmesini sağlar.
style.css → Web sayfasının tasarımını düzenler.
index.html → Kullanıcı arayüzünü içeren ana HTML dosyasıdır.

🔹 Makine Öğrenimi (Google Colab Üzerinde Eğitildi)

film_recommender_model.pkl → Google Colab'de eğitilen makine öğrenimi modeli.
Google Colab Notebook → Filmler için veri işleme, TF-IDF vektörleme ve benzerlik hesaplamalarını içerir.
Model, Google Drive'a kaydedilmiş ve Flask uygulamasında kullanılmak üzere indirilmektedir.

🔹 Deploy (Yayınlama ve Sunucu Ayarları)

requirements.txt → Uygulamanın çalışması için gereken Python kütüphanelerini listeler.
Procfile → Render’da Flask uygulamasının nasıl başlatılacağını belirtir.
runtime.txt → Sunucunun hangi Python sürümünü kullanacağını belirler.

🔹 Git ve Büyük Dosya Yönetimi

.gitignore → Gereksiz veya büyük dosyaların GitHub’a yüklenmesini engeller.
.gitattributes → Büyük dosyaların Git LFS ile yönetilmesini sağlar.

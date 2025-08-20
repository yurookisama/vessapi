### **VessAPI - Ürün Gereksinim Dokümanı (PRD)**

**1. Proje Vizyonu ve Hedefi**

*   **Vizyon:** VessAPI, müzik tabanlı uygulamalar (mobil, masaüstü, web) için merkezi, güvenli, ölçeklenebilir ve yüksek performanslı bir backend hizmeti olacaktır.
*   **Ana Hedef:** Farklı istemcilere müzik, sanatçı, albüm, kullanıcı ve çalma listesi verilerini standart bir API üzerinden tutarlı bir şekilde sunmak ve yönetmek.

---

### **Faz 1: Güvenlik ve Test Altyapısını Tamamlama (MVP Güvenliği)**

*Bu fazın amacı, API'yi temel güvenlik standartlarına ve test edilebilir bir yapıya kavuşturarak dış tehditlere karşı korunaklı hale getirmektir.*

#### **1.1. Yetkilendirme (Authorization) Mekanizması**
*   [X] **1.1.1.** `users` rotası için yetkilendirme kuralları oluşturulacak:
    *   [X] Bir kullanıcı sadece kendi bilgilerini getirebilmeli (`/users/me`).
    *   [X] Bir kullanıcı sadece kendi bilgilerini güncelleyebilmeli.
    *   [X] Bir kullanıcı sadece kendi hesabını silebilmeli.
    *   [X] Admin rolü tanımlanacak ve sadece admin tüm kullanıcıları listeleyebilmeli/silebilmeli.
*   [X] **1.1.2.** `playlists` rotası için yetkilendirme kuralları oluşturulacak:
    *   [X] Bir kullanıcı sadece kendi çalma listelerini oluşturabilmeli.
    *   [X] Bir kullanıcı sadece kendi çalma listelerini getirebilmeli, güncelleyebilmeli ve silebilmeli.
    *   [X] Çalma listesine müzik ekleme/çıkarma işlemleri sadece liste sahibi tarafından yapılabilmeli.
*   [X] **1.1.3.** `music`, `albums`, `artists` rotaları için içerik yönetimi yetkilendirmesi (Admin/Editör Rolü) eklenecek:
    *   [X] Sadece belirli rollere sahip kullanıcıların (örn: admin, editör) müzik, albüm veya sanatçı eklemesine/güncellemesine/silmesine izin verilecek.
    *   [X] Genel kullanıcılar bu verileri sadece okuyabilmeli.

#### **1.2. API Güvenlik Sertleştirmesi**
*   [X] **1.2.1.** Giriş (`/token`) endpoint'i için `fastapi-limiter` kullanılarak hız limiti (rate limiting) eklenecek. (Örnek: 1 dakikada 5 hatalı deneme sonrası 5 dakika bekleme).
*   [X] **1.2.2.** Diğer hassas veya kaynak tüketen endpoint'ler için genel bir hız limiti kuralı tanımlanacak. (Örnek: Bir kullanıcı saniyede 10'dan fazla istek atamamalı).
*   [X] **1.2.3.** Tüm API rotaları için CORS (Cross-Origin Resource Sharing) ayarları yapılacak ve sadece izin verilen istemci adreslerinden (mobil, web uygulaması domain'leri) gelen isteklere izin verilecek.

#### **1.3. Test Altyapısı Kurulumu ve Temel Testler**
*   [X] **1.3.1.** `pytest` ve `httpx` kütüphaneleri projeye eklenecek.
*   [] **1.3.2.** Test için ayrı bir veritabanı yapılandırması oluşturulacak. Testler çalışmadan önce bu veritabanı temizlenip yeniden oluşturulacak.
*   [X] **1.3.3.** **Authentication Testleri:**
    *   [X] Başarılı kullanıcı oluşturma testi.
    *   [X] Aynı e-posta ile ikinci bir kullanıcı oluşturulamama testi.
    *   [X] Başarılı token alma (giriş) testi.
    *   [X] Yanlış şifre ile token alamama testi.
*   [X] **1.3.4.** **Yetkilendirme Testleri:**
    *   [] Bir kullanıcının, başka bir kullanıcının çalma listesini silmeye çalıştığında `403 Forbidden` hatası alma testi.
    *   [X] Normal bir kullanıcının, yeni bir sanatçı eklemeye çalıştığında `403 Forbidden` hatası alma testi.

---

### **Faz 2: Veritabanı ve Altyapıyı Olgunlaştırma**

*Bu fazın amacı, projenin altyapısını sağlamlaştırmak, bakımını kolaylaştırmak ve geliştirme/dağıtım süreçlerini otomatize etmektir.*

#### **2.1. Veritabanı Yönetimi**
*   [] **2.1.1.** `Alembic` kütüphanesi projeye entegre edilecek.
*   [] **2.1.2.** Mevcut `Beanie` modelleri için ilk veritabanı şeması "migration" dosyası oluşturulacak.
*   [] **2.1.3.** `README.md` dosyasına veritabanı şeması güncelleme (migration çalıştırma) komutları eklenecek.

#### **2.2. Yapılandırma ve Hassas Veri Yönetimi**
*   [] **2.2.1.** `pydantic-settings` kütüphanesi projeye eklenecek.
*   [] **2.2.2.** Proje kök dizinine bir `.env.example` dosyası oluşturulacak. Bu dosyada `DATABASE_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES` gibi tüm yapılandırma değişkenleri yer alacak.
*   [] **2.2.3.** Kod içerisindeki tüm sabit yapılandırma değerleri (secret key, db adresi vb.) `.env` dosyasından okunacak şekilde refaktör edilecek.
*   [] **2.2.4.** `.gitignore` dosyasına `.env` dosyası eklenecek.

#### **2.3. Konteynerizasyon (Containerization)**
*   [] **2.3.1.** Proje kök dizinine `docker-compose.yml` dosyası oluşturulacak.
*   [] **2.3.2.** `docker-compose.yml` içine `api`, `db` (MongoDB) ve `cache` (Redis) servisleri tanımlanacak.
*   [] **2.3.3.** `api` servisi, `Dockerfile`'ı kullanarak build edilecek şekilde ayarlanacak.
*   [] **2.3.4.** `db` ve `cache` servisleri için resmi imajlar kullanılacak ve verilerin kalıcı olması için "volume" tanımlamaları yapılacak.
*   [] **2.3.5.** `README.md` dosyasına projeyi `docker-compose up` komutu ile başlatma talimatları eklenecek.

---

### **Faz 3: API ve Kullanıcı Deneyimini Geliştirme**

*Bu fazın amacı, API'nin performansını ve kullanılabilirliğini artırarak son kullanıcıya daha iyi bir deneyim sunmaktır.*

#### **3.1. Performans Optimizasyonu**
*   [] **3.1.1.** Liste döndüren tüm endpoint'ler (`/music`, `/albums`, `/artists`, `/playlists`, `/users`) için sayfalama (pagination) mekanizması eklenecek.
    *   [] Bu endpoint'ler `skip: int = 0` ve `limit: int = 100` query parametrelerini kabul edecek.
    *   [] Dönen yanıta toplam öğe sayısı (`total_count`) gibi meta veriler eklenecek.
*   [] **3.1.2.** Sık erişilen ve değişmeyen veriler (örn: popüler şarkılar, ana sayfa albümleri) için `Redis` tabanlı bir önbellekleme (caching) stratejisi geliştirilecek.

#### **3.2. Asenkron İşlemler**
*   [] **3.2.1.** Müzik dosyası yükleme (`/upload-music`) endpoint'i refaktör edilecek.
    *   [] Dosya kabul edildikten sonra API, anında `202 Accepted` yanıtı dönecek.
    *   [] Dosyanın diske yazılması, metadata'sının çıkarılması ve veritabanına kaydedilmesi işlemleri FastAPI `BackgroundTasks` ile arka planda yapılacak.
*   [] **3.2.2.** Albüm kapağı veya diğer resim dosyalarını işleme (örn: yeniden boyutlandırma) gibi potansiyel olarak uzun sürebilecek işlemler için de arka plan görevleri kullanılacak.

#### **3.3. Gelişmiş Arama ve Filtreleme**
*   [] **3.3.1.** `/music` endpoint'ine `artist_id`, `album_id`, `genre` gibi alanlara göre filtreleme özellikleri eklenecek.
*   [] **3.3.2.** Müzik, sanatçı ve albüm isimlerine göre arama yapmayı sağlayan bir `/search` endpoint'i oluşturulacak.

---
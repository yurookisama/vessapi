# 🎵 VessAPI - Müzik Yönetim Sistemi

VessAPI, müzik koleksiyonunuzu dijital ortamda organize etmenizi, paylaşmanizi ve yönetmenizi sağlayan modern bir müzik yönetim sistemidir. Bu sistem sayesinde müziklerinizi, albümlerinizi, sanatçılarınızı ve çalma listelerinizi kolayca yönetebilirsiniz.

## 🌟 Özellikler

### 🎶 **Müzik Yönetimi**
- Müzik dosyalarınızı sisteme yükleyebilirsiniz
- Müzikleri başlık, sanatçı, tür gibi kriterlere göre arayabilirsiniz
- Müzikleri doğrudan tarayıcınızdan dinleyebilirsiniz
- Her müzik için kapak resmi ekleyebilirsiniz

### 💿 **Albüm Organizasyonu**
- Müziklerinizi albümler halinde gruplandırabilirsiniz
- Albüm kapak resimleri ekleyebilirsiniz
- Albüm bilgilerini (çıkış tarihi, tür, açıklama) yönetebilirsiniz

### 🎤 **Sanatçı Bilgileri**
- Sanatçı profilleri oluşturabilirsiniz
- Sanatçı biyografileri ve fotoğrafları ekleyebilirsiniz
- Sanatçıların tüm müziklerini ve albümlerini görüntüleyebilirsiniz

### 📝 **Çalma Listeleri**
- Kişisel çalma listeleri oluşturabilirsiniz
- Çalma listelerini herkese açık veya özel yapabilirsiniz
- Çalma listelerine müzik ekleyip çıkarabilirsiniz

### 👤 **Kullanıcı Yönetimi**
- Güvenli kullanıcı hesapları oluşturabilirsiniz
- Kullanıcı adı ve şifre ile giriş yapabilirsiniz
- Kişisel profilinizi yönetebilirsiniz

## 🚀 Kurulum Rehberi

### Gereksinimler
Sistemi çalıştırmak için bilgisayarınızda şunların yüklü olması gerekir:

1. **Python 3.8 veya üzeri** - Programlama dili
2. **MongoDB** - Veritabanı sistemi
3. **Git** - Kod indirmek için (opsiyonel)

### Adım 1: Projeyi İndirin

#### Yöntem 1: Git ile (Önerilen)
```bash
git clone https://github.com/kullanici-adi/VessAPI.git
cd VessAPI
```

#### Yöntem 2: ZIP dosyası ile
1. GitHub sayfasından "Code" butonuna tıklayın
2. "Download ZIP" seçeneğini seçin
3. İndirilen dosyayı bir klasöre çıkarın
4. Komut satırında o klasöre gidin

### Adım 2: Sanal Ortam Oluşturun
```bash
python -m venv venv
```

### Adım 3: Sanal Ortamı Aktifleştirin

**Windows için:**
```bash
venv\Scripts\activate
```

**Mac/Linux için:**
```bash
source venv/bin/activate
```

### Adım 4: Gerekli Paketleri Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 5: Konfigürasyon Dosyasını Hazırlayın
```bash
# .env.example dosyasını .env olarak kopyalayın
cp .env.example .env

# Gerekirse .env dosyasını düzenleyin (varsayılan ayarlar çoğu durumda yeterlidir)
```

### Adım 6: MongoDB'yi Başlatın
MongoDB'nin bilgisayarınızda çalıştığından emin olun. Genellikle şu komutla başlatılır:
```bash
mongod
```

### Adım 7: Uygulamayı Başlatın
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Adım 8: Kurulum Kontrolü (Opsiyonel)
Kurulumun doğru yapılıp yapılmadığını kontrol etmek için:
```bash
python check_config.py
```

🎉 **Tebrikler!** Uygulamanız artık çalışıyor. 

### Kurulum Testi
Uygulamanın doğru çalıştığını test etmek için:

1. **API Dokümantasyonu**: `http://localhost:8000/docs`
2. **Ana Sayfa**: `http://localhost:8000`
3. **Health Check**: `http://localhost:8000/health`

### İlk Kullanım Adımları
1. Ana sayfaya gidin: `http://localhost:8000`
2. Yeni bir kullanıcı hesabı oluşturun
3. Giriş yapın
4. İlk müziğinizi yükleyin ve keyfini çıkarın!

## 📖 Kullanım Kılavuzu

### İlk Kullanım

1. **Tarayıcınızı açın** ve `http://localhost:8000` adresine gidin
2. **Hesap oluşturun**: Ana sayfada kayıt formunu doldurun
3. **Giriş yapın**: Kullanıcı adınız ve şifrenizle sisteme giriş yapın

### Müzik Yükleme

1. Ana sayfada **"Müzik Yükle"** bölümünü bulun
2. **Müzik dosyalarınızı seçin** (MP3, FLAC, OGG formatları desteklenir)
3. İsteğe bağlı olarak **kapak resmi** ekleyin
4. **"Yükle"** butonuna tıklayın
5. Sistem otomatik olarak müzik bilgilerini analiz edecek ve veritabanına ekleyecek

### Müzik Dinleme

1. **"Müzikler"** sayfasına gidin
2. Dinlemek istediğiniz müziği bulun
3. Müzik adına tıklayarak **çalma sayfasına** gidin
4. **Play** butonuna tıklayarak dinlemeye başlayın

### Çalma Listesi Oluşturma

1. **"Çalma Listeleri"** sayfasına gidin
2. **"Yeni Çalma Listesi"** butonuna tıklayın
3. **Liste adı** ve **açıklama** girin
4. Listeyi **herkese açık** veya **özel** yapın
5. **"Oluştur"** butonuna tıklayın
6. Oluşturduğunuz listeye müzik eklemek için müzik sayfalarından **"Çalma Listesine Ekle"** butonunu kullanın

## 🔧 API Kullanımı (Geliştiriciler İçin)

VessAPI, RESTful API mimarisi kullanır. Tüm API endpoint'leri `/v1/` prefix'i ile başlar.

### Temel Endpoint'ler

#### Sistem Durumu
```
GET /health
```
Sistemin çalışıp çalışmadığını kontrol eder.

#### Kullanıcı İşlemleri
```
POST /v1/users/          # Yeni kullanıcı oluştur
POST /token              # Giriş yap (token al)
GET /v1/users/me         # Mevcut kullanıcı bilgileri
```

#### Müzik İşlemleri
```
GET /v1/songs/           # Tüm müzikleri listele
GET /v1/songs/{id}       # Belirli bir müziği getir
GET /v1/songs/{id}/stream # Müziği dinle
```

#### Albüm İşlemleri
```
GET /v1/albums/          # Tüm albümleri listele
GET /v1/albums/{id}      # Belirli bir albümü getir
```

#### Sanatçı İşlemleri
```
GET /v1/artists/         # Tüm sanatçıları listele
GET /v1/artists/{id}     # Belirli bir sanatçıyı getir
```

#### Çalma Listesi İşlemleri
```
GET /v1/playlists/       # Erişilebilir çalma listelerini listele
POST /v1/playlists/      # Yeni çalma listesi oluştur
GET /v1/playlists/{id}   # Belirli bir çalma listesini getir
```

### API Dokümantasyonu
Detaylı API dokümantasyonu için uygulamayı başlattıktan sonra şu adreslere gidin:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📁 Proje Yapısı

```
VessAPI/
├── main.py                 # Ana uygulama dosyası
├── requirements.txt        # Gerekli Python paketleri
├── README.md              # Bu dosya
├── check_config.py         # Konfigürasyon kontrol scripti
├── .env.example           # Örnek konfigürasyon dosyası
├── .env                   # Konfigürasyon dosyası (kopyalanacak)
├── .gitignore             # Git ignore kuralları
├── pytest.ini             # Test konfigürasyonu
├── library/               # Yüklenen dosyaların saklandığı klasör
│   ├── music/            # Müzik dosyaları
│   └── images/           # Resim dosyaları
│       ├── album_image/  # Albüm kapakları
│       ├── music_image/  # Müzik kapakları
│       ├── user_image/   # Kullanıcı resimleri
│       └── artist_image/ # Sanatçı fotoğrafları
├── templates/             # Web sayfası şablonları
├── static/               # CSS, JavaScript dosyaları
├── tests/                # Test dosyaları
│   ├── conftest.py       # Test konfigürasyonu
│   └── test_*.py         # Test dosyaları
├── logs/                 # Log dosyaları (opsiyonel)
└── vessapi/              # Ana kod klasörü
    ├── __init__.py       # Python paketi
    ├── config.py         # Konfigürasyon yönetimi
    ├── models.py         # Veritabanı modelleri
    ├── schemas.py        # API şemaları
    ├── crud.py           # Veritabanı işlemleri
    ├── auth.py           # Kimlik doğrulama
    ├── database.py       # Veritabanı bağlantısı
    ├── services.py       # İş mantığı servisleri
    └── routers/          # API endpoint'leri
        ├── __init__.py   # Python paketi
        ├── music.py      # Müzik API'leri (songs endpoint)
        ├── albums.py     # Albüm API'leri
        ├── artists.py    # Sanatçı API'leri
        ├── playlists.py  # Çalma listesi API'leri
        ├── users.py      # Kullanıcı API'leri
        └── web.py        # Web sayfası API'leri
```

### Dosya Açıklamaları

#### Konfigürasyon Dosyaları
- **`.env`**: Ana konfigürasyon dosyası (veritabanı, güvenlik, sunucu ayarları)
- **`.env.example`**: Örnek konfigürasyon dosyası (versiyon kontrolünde)
- **`check_config.py`**: Kurulum ve konfigürasyon kontrol scripti

#### Ana Uygulama
- **`main.py`**: FastAPI uygulamasının ana dosyası, router'ları ve middleware'leri içerir
- **`requirements.txt`**: Python bağımlılıkları listesi

#### VessAPI Paketi
- **`config.py`**: Tüm konfigürasyon ayarlarını yöneten merkezi sistem
- **`models.py`**: MongoDB için Beanie modelleri (User, Music, Album, Artist, Playlist)
- **`schemas.py`**: Pydantic şemaları (API request/response modelleri)
- **`crud.py`**: Veritabanı CRUD işlemleri ve yardımcı fonksiyonlar
- **`auth.py`**: JWT tabanlı kimlik doğrulama sistemi
- **`database.py`**: MongoDB bağlantı yönetimi
- **`services.py`**: İş mantığı ve arka plan görevleri

#### API Router'ları
- **`music.py`**: Müzik dosyaları için API endpoint'leri (`/v1/songs/`)
- **`albums.py`**: Albüm yönetimi API'leri (`/v1/albums/`)
- **`artists.py`**: Sanatçı yönetimi API'leri (`/v1/artists/`)
- **`playlists.py`**: Çalma listesi API'leri (`/v1/playlists/`)
- **`users.py`**: Kullanıcı yönetimi API'leri (`/v1/users/`)
- **`web.py`**: Web arayüzü için HTML endpoint'leri

#### Dosya Depolama
- **`library/music/`**: Yüklenen müzik dosyaları
- **`library/images/`**: Tüm resim dosyaları (kapaklar, profil resimleri)

#### Test ve Geliştirme
- **`tests/`**: Otomatik test dosyaları
- **`pytest.ini`**: Test konfigürasyonu
- **`logs/`**: Uygulama log dosyaları (opsiyonel)

## ⚙️ Yapılandırma

### Konfigürasyon Dosyası (.env)
Uygulamanın tüm ayarları `.env` dosyasında yönetilir. İlk kurulumda `.env.example` dosyasını `.env` olarak kopyalayın:

```bash
cp .env.example .env
```

### Temel Ayarlar

#### Veritabanı Ayarları
```bash
DATABASE_URL=mongodb://localhost:27017    # MongoDB sunucu adresi
DATABASE_NAME=vessapi                     # Veritabanı adı
TEST_DATABASE_URL=mongodb://localhost:27017/vessapi_test  # Test veritabanı
```

#### Güvenlik Ayarları
```bash
SECRET_KEY=your-super-secret-key          # JWT şifreleme anahtarı (ÖNEMLİ: Üretimde değiştirin!)
ALGORITHM=HS256                           # Şifreleme algoritması
ACCESS_TOKEN_EXPIRE_MINUTES=30            # Token geçerlilik süresi (dakika)
```

#### Sunucu Ayarları
```bash
HOST=0.0.0.0                             # Sunucu adresi
PORT=8000                                # Port numarası
DEBUG=false                              # Debug modu (geliştirme için true)
CORS_ORIGINS=*                           # İzin verilen origin'ler
```

#### Dosya Yönetimi Ayarları
```bash
MUSIC_UPLOAD_DIRECTORY=library/music                    # Müzik dosyaları
ALBUM_IMAGE_DIRECTORY=library/images/album_image        # Albüm kapakları
MUSIC_IMAGE_DIRECTORY=library/images/music_image        # Müzik kapakları
USER_IMAGE_DIRECTORY=library/images/user_image          # Kullanıcı resimleri
ARTIST_IMAGE_DIRECTORY=library/images/artist_image      # Sanatçı fotoğrafları

MAX_MUSIC_FILE_SIZE=100                  # Maksimum müzik dosyası boyutu (MB)
MAX_IMAGE_FILE_SIZE=10                   # Maksimum resim dosyası boyutu (MB)
```

#### Desteklenen Dosya Formatları
```bash
SUPPORTED_MUSIC_FORMATS=mp3,flac,ogg,wav,m4a           # Müzik formatları
SUPPORTED_IMAGE_FORMATS=jpg,jpeg,png,webp              # Resim formatları
```

### Gelişmiş Ayarlar

#### Loglama
```bash
LOG_LEVEL=INFO                           # Log seviyesi (DEBUG, INFO, WARNING, ERROR)
LOG_FILE=logs/vessapi.log               # Log dosyası yolu (opsiyonel)
```

### Üretim Ortamı İçin Önemli Notlar

1. **SECRET_KEY**: Mutlaka güçlü ve benzersiz bir anahtar kullanın
2. **DEBUG**: Üretimde `false` olarak ayarlayın
3. **CORS_ORIGINS**: Sadece güvenilir domain'leri ekleyin
4. **Dosya İzinleri**: Upload klasörlerinin yazma izni olduğundan emin olun

## 🔒 Güvenlik

### Kimlik Doğrulama
- Sistem JWT (JSON Web Token) tabanlı kimlik doğrulama kullanır
- Şifreler bcrypt algoritması ile güvenli şekilde şifrelenir
- Her kullanıcının kendine ait çalma listeleri vardır

### Dosya Güvenliği
- Yüklenen dosyalar güvenli klasörlerde saklanır
- Sadece desteklenen dosya formatları kabul edilir
- Dosya boyutu sınırlamaları mevcuttur

## 🐛 Sorun Giderme

### Otomatik Kontrol Scripti
Sorunları hızlıca tespit etmek için kontrol scriptini çalıştırın:
```bash
python check_config.py
```

Bu script şunları kontrol eder:
- Python sürümü uyumluluğu
- Gerekli dosyaların varlığı
- Python bağımlılıkları
- MongoDB bağlantısı
- Konfigürasyon ayarları

### Yaygın Sorunlar ve Çözümleri

#### "ModuleNotFoundError: No module named 'pydantic_settings'"
**Sorun**: Yeni bağımlılık eksik
**Çözüm**: 
```bash
pip install pydantic-settings
# veya
pip install -r requirements.txt
```

#### "MongoDB bağlantı hatası"
**Sorun**: Uygulama MongoDB'ye bağlanamıyor
**Çözüm**: 
1. MongoDB'nin çalıştığından emin olun: `mongod`
2. `.env` dosyasında `DATABASE_URL` ayarını kontrol edin
3. MongoDB servisinin başlatıldığından emin olun
4. Kontrol scripti çalıştırın: `python check_config.py`

#### "Port zaten kullanımda"
**Sorun**: 8000 portu başka bir uygulama tarafından kullanılıyor
**Çözüm**: 
1. `.env` dosyasında `PORT` değerini değiştirin
2. Veya komut satırında farklı port belirtin: `--port 8001`
3. Çalışan uygulamayı durdurun

#### "Konfigürasyon dosyası bulunamadı"
**Sorun**: `.env` dosyası yok
**Çözüm**:
```bash
cp .env.example .env
```

#### "Müzik dosyası yüklenmiyor"
**Sorun**: Müzik dosyası sisteme yüklenmiyor
**Çözüm**:
1. Dosya formatının desteklendiğinden emin olun (MP3, FLAC, OGG, WAV, M4A)
2. Dosya boyutunun `.env` dosyasındaki `MAX_MUSIC_FILE_SIZE` limitini aşmadığından emin olun
3. Upload klasörlerinin yazma izni olduğundan emin olun
4. Kontrol scripti ile klasör yapısını kontrol edin

#### "Giriş yapamıyorum"
**Sorun**: Kullanıcı adı ve şifre ile giriş yapamıyorum
**Çözüm**:
1. Kullanıcı adı ve şifrenizi doğru yazdığınızdan emin olun
2. Hesabınızın aktif olduğundan emin olun
3. Gerekirse yeni bir hesap oluşturun
4. `.env` dosyasında `SECRET_KEY` ayarının doğru olduğundan emin olun

#### "Internal Server Error"
**Sorun**: API çağrıları 500 hatası veriyor
**Çözüm**:
1. Kontrol scriptini çalıştırın: `python check_config.py`
2. MongoDB bağlantısını kontrol edin
3. Log dosyalarını inceleyin
4. Debug modunu açın: `.env` dosyasında `DEBUG=true`

#### "CORS hatası"
**Sorun**: Tarayıcıda CORS hatası alıyorum
**Çözüm**:
1. `.env` dosyasında `CORS_ORIGINS` ayarını kontrol edin
2. Frontend URL'nizi CORS listesine ekleyin
3. Geliştirme için `CORS_ORIGINS=*` kullanabilirsiniz

### Log Dosyaları
Detaylı hata bilgileri için log dosyalarını kontrol edin:
- Uygulama logları: `.env` dosyasında `LOG_FILE` ile belirtilen dosya
- MongoDB logları: MongoDB kurulum klasöründeki log dosyaları

### Performans Sorunları
- Büyük müzik koleksiyonları için MongoDB indekslerini optimize edin
- Dosya boyutu limitlerini ihtiyacınıza göre ayarlayın
- Debug modunu üretimde kapatın

## 🤝 Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz:

### Geliştirme Ortamı Kurulumu
1. **Projeyi fork edin** ve klonlayın
2. **Geliştirme ortamını kurun**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```
3. **Konfigürasyonu kontrol edin**: `python check_config.py`
4. **Testleri çalıştırın**: `pytest`

### Katkı Süreci
1. **Feature branch** oluşturun (`git checkout -b yeni-ozellik`)
2. **Değişikliklerinizi yapın** ve test edin
3. **Testler ekleyin** (gerekirse)
4. **Kod stilini kontrol edin** (PEP 8)
5. **Commit** edin (`git commit -am 'Yeni özellik: açıklama'`)
6. **Push** edin (`git push origin yeni-ozellik`)
7. **Pull Request** oluşturun

### Katkı Kuralları
- Kod değişiklikleri için test yazın
- Commit mesajlarını açıklayıcı yazın
- Büyük değişiklikler için önce issue açın
- Dokümantasyonu güncel tutun
- PEP 8 kod stiline uyun

### Test Etme
```bash
# Tüm testleri çalıştır
pytest

# Belirli bir test dosyasını çalıştır
pytest tests/test_music.py

# Coverage raporu
pytest --cov=vessapi
```

## 📞 Destek

Herhangi bir sorunuz veya sorununuz varsa:

- **GitHub Issues**: Teknik sorunlar için issue açın
- **Dokümantasyon**: `http://localhost:8000/docs` adresindeki API dokümantasyonunu inceleyin
- **Topluluk**: Diğer kullanıcılarla deneyim paylaşın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

### MIT Lisansı Özeti
- ✅ Ticari kullanım
- ✅ Değiştirme
- ✅ Dağıtım
- ✅ Özel kullanım
- ❌ Sorumluluk
- ❌ Garanti

## 📊 Proje İstatistikleri

- **Dil**: Python 3.8+
- **Framework**: FastAPI
- **Veritabanı**: MongoDB
- **Authentication**: JWT
- **API Tipi**: RESTful
- **Dokümantasyon**: OpenAPI/Swagger

## 🙏 Teşekkürler

VessAPI'yi kullandığınız için teşekkür ederiz! Bu proje, müzik severlerin dijital koleksiyonlarını daha iyi yönetebilmeleri için geliştirilmiştir.

---

**Not**: Bu README dosyası sürekli güncellenmektedir. En son sürüm için GitHub sayfasını kontrol edin.
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

### Adım 5: MongoDB'yi Başlatın
MongoDB'nin bilgisayarınızda çalıştığından emin olun. Genellikle şu komutla başlatılır:
```bash
mongod
```

### Adım 6: Uygulamayı Başlatın
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

🎉 **Tebrikler!** Uygulamanız artık çalışıyor. Tarayıcınızda `http://localhost:8000` adresine giderek kullanmaya başlayabilirsiniz.

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
├── library/               # Yüklenen dosyaların saklandığı klasör
│   ├── music/            # Müzik dosyaları
│   └── images/           # Resim dosyaları
├── templates/             # Web sayfası şablonları
├── static/               # CSS, JavaScript dosyaları
└── vessapi/              # Ana kod klasörü
    ├── models.py         # Veritabanı modelleri
    ├── schemas.py        # API şemaları
    ├── crud.py           # Veritabanı işlemleri
    ├── auth.py           # Kimlik doğrulama
    ├── database.py       # Veritabanı bağlantısı
    └── routers/          # API endpoint'leri
        ├── music.py      # Müzik API'leri
        ├── albums.py     # Albüm API'leri
        ├── artists.py    # Sanatçı API'leri
        ├── playlists.py  # Çalma listesi API'leri
        ├── users.py      # Kullanıcı API'leri
        └── web.py        # Web sayfası API'leri
```

## ⚙️ Yapılandırma

### Ortam Değişkenleri
Uygulamayı özelleştirmek için şu ortam değişkenlerini kullanabilirsiniz:

```bash
SECRET_KEY=your-super-secret-key    # JWT token şifreleme anahtarı
MONGODB_URL=mongodb://localhost:27017/vessapi  # MongoDB bağlantı adresi
PORT=8000                           # Uygulama portu
```

### Dosya Yolları
Yüklenen dosyalar varsayılan olarak şu klasörlerde saklanır:
- **Müzik dosyaları**: `library/music/`
- **Albüm kapakları**: `library/images/album_image/`
- **Müzik kapakları**: `library/images/music_image/`
- **Sanatçı fotoğrafları**: `library/images/artist_image/`

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

### Yaygın Sorunlar ve Çözümleri

#### "MongoDB bağlantı hatası"
**Sorun**: Uygulama MongoDB'ye bağlanamıyor
**Çözüm**: 
1. MongoDB'nin çalıştığından emin olun: `mongod`
2. Bağlantı adresini kontrol edin
3. MongoDB servisinin başlatıldığından emin olun

#### "Port zaten kullanımda"
**Sorun**: 8000 portu başka bir uygulama tarafından kullanılıyor
**Çözüm**: 
1. Farklı bir port kullanın: `--port 8001`
2. Veya çalışan uygulamayı durdurun

#### "Müzik dosyası yüklenmiyor"
**Sorun**: Müzik dosyası sisteme yüklenmiyor
**Çözüm**:
1. Dosya formatının desteklendiğinden emin olun (MP3, FLAC, OGG)
2. Dosya boyutunun çok büyük olmadığından emin olun
3. `library/music/` klasörünün yazma izni olduğundan emin olun

#### "Giriş yapamıyorum"
**Sorun**: Kullanıcı adı ve şifre ile giriş yapamıyorum
**Çözüm**:
1. Kullanıcı adı ve şifrenizi doğru yazdığınızdan emin olun
2. Hesabınızın aktif olduğundan emin olun
3. Gerekirse yeni bir hesap oluşturun

## 🤝 Katkıda Bulunma

Bu projeye katkıda bulunmak isterseniz:

1. **Fork** yapın (projeyi kendi hesabınıza kopyalayın)
2. **Feature branch** oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi **commit** edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi **push** edin (`git push origin yeni-ozellik`)
5. **Pull Request** oluşturun

## 📞 Destek

Herhangi bir sorunuz veya sorununuz varsa:

- **GitHub Issues**: Teknik sorunlar için issue açın
- **Dokümantasyon**: `http://localhost:8000/docs` adresindeki API dokümantasyonunu inceleyin
- **Topluluk**: Diğer kullanıcılarla deneyim paylaşın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 🙏 Teşekkürler

VessAPI'yi kullandığınız için teşekkür ederiz! Bu proje, müzik severlerin dijital koleksiyonlarını daha iyi yönetebilmeleri için geliştirilmiştir.

---

**Not**: Bu README dosyası sürekli güncellenmektedir. En son sürüm için GitHub sayfasını kontrol edin.
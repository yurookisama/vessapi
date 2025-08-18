# VessAPI: Müzik Uygulamaları İçin Bir Yardımcı

Merhaba! Bu proje, müzik uygulamaları yaparken size yardımcı olacak bir "arka plan" sistemidir. Müziklerinizi, albümlerinizi, sanatçılarınızı, kullanıcılarınızı ve kendi müzik listelerinizi (çalma listeleri) düzenlemenizi sağlar.

## VessAPI Ne Yapar? (Özellikler)

Bu sistem sayesinde şunları yapabilirsiniz:

*   **Müziklerinizi Yönetin:** Yeni müzikler ekleyebilir, var olanları değiştirebilir, silebilir veya tüm müziklerinizi görebilirsiniz.
*   **Albümlerinizi Yönetin:** Albümlerinizi ekleyebilir, düzenleyebilir, silebilir ve içindeki müzikleri görebilirsiniz.
*   **Sanatçıları Yönetin:** Sanatçı bilgilerini ekleyebilir, güncelleyebilir veya silebilirsiniz.
*   **Kullanıcıları Yönetin:** Uygulamanıza yeni kullanıcılar kaydedebilir, onların bilgilerini düzenleyebilir veya silebilirsiniz.
*   **Çalma Listeleri Oluşturun:** Kendi müzik listelerinizi yapabilir, içine müzik ekleyip çıkarabilirsiniz.
*   **Dosyaları Yükleyin:** Müzik dosyalarınızı ve albüm kapaklarını sisteme yükleyebilirsiniz.

## Nasıl Kurulur ve Çalıştırılır? (Adım Adım)

Bu sistemi bilgisayarınızda çalıştırmak için birkaç şeye ihtiyacınız var:

### İhtiyacınız Olanlar:

1.  **Python:** Bilgisayarınızda Python programlama dili kurulu olmalı (sürüm 3.9 veya üzeri).
2.  **MongoDB:** Bu, verilerinizi sakladığımız bir "veritabanı"dır. Bilgisayarınızda kurulu ve çalışıyor olması gerekiyor.

### Kurulum Adımları:

1.  **Projeyi Bilgisayarınıza Getirin:**
    *   Bu projenin dosyalarını bilgisayarınıza indirin. Eğer `git` kullanıyorsanız, şu komutu çalıştırabilirsiniz:
        ```bash
        git clone <proje_adresi>
        cd VessAPI
        ```
    *   Yoksa, dosyaları manuel olarak indirip `VessAPI` klasörüne girin.

2.  **Sanal Ortam Oluşturun (Önemli!):**
    *   Bu adım, projenin ihtiyaç duyduğu özel araçları (kütüphaneleri) bilgisayarınızdaki diğer Python projelerinden ayırır. Böylece karışıklık olmaz.
    *   `VessAPI` klasöründeyken, komut istemcisini (Windows'ta `cmd` veya `PowerShell`, Mac/Linux'ta `Terminal`) açın ve şu komutları yazın:

    **Windows için:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

    **Mac/Linux için:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Gerekli Araçları Yükleyin:**
    *   Şimdi projenin çalışması için gereken tüm kütüphaneleri yükleyelim. Sanal ortamınız aktifken (komut satırında `(venv)` yazısını görmelisiniz), şu komutu çalıştırın:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Uygulamayı Başlatın:**
    *   Her şey hazır! Şimdi sistemi çalıştıralım. Aynı komut istemcisinde şu komutu yazın:
        ```bash
        uvicorn main:app --reload
        ```
    *   Eğer her şey yolundaysa, sistem `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır.

## Sistemi Nasıl Kullanırım? (API ve Web Arayüzü)

Sistemi iki şekilde kullanabilirsiniz:

### 1. API ile (Programcılar İçin)

Bu sistem, diğer uygulamaların (mobil uygulama, web sitesi vb.) onunla konuşmasını sağlayan bir "API" sunar. Yani, uygulamanız bu sistemden bilgi alabilir veya ona bilgi gönderebilir.

**Nasıl Bağlanılır ve Kullanılır?**

1.  **Sistemin Adresi (Temel URL):**
    *   Uygulamanızın bu sistemle konuşmak için bilmesi gereken ana adres şudur: `http://127.0.0.1:8000`
    *   Bu adresi, yapacağınız her isteğin başına ekleyeceksiniz. Örneğin, müzikleri listelemek için `http://127.0.0.1:8000/v1/music/` adresine istek göndereceksiniz.

2.  **API Haritası (Dokümantasyon):**
    *   Sistemin neler yapabildiğini ve hangi bilgilere ihtiyacı olduğunu görmek için tarayıcınızda şu adresleri ziyaret edin:
        *   `http://127.0.0.1:8000/docs` (Daha interaktif bir arayüz, deneyip test edebilirsiniz.)
        *   `http://127.0.0.1:8000/redoc` (Daha sade bir arayüz.)
    *   Burada, her bir işlem (müzik ekleme, kullanıcı kaydetme vb.) için hangi adrese istek göndermeniz gerektiği, hangi bilgileri vermeniz gerektiği ve sistemin size nasıl bir cevap vereceği detaylıca anlatılır.

3.  **Giriş Yapma (Token Alma):**
    *   Bazı işlemler (örneğin kendi çalma listenizi düzenleme veya kullanıcı bilgilerinizi güncelleme) için sisteme "giriş yapmış" olmanız gerekir.
    *   Giriş yapmak için, `/token` adresine kullanıcı adınız (e-posta) ve şifrenizle bir istek gönderirsiniz. Sistem size bir "token" (bir çeşit geçici anahtar) verir.
    *   Bu token'ı, giriş gerektiren sonraki tüm isteklerinizde "Authorization" (Yetkilendirme) başlığı altında `Bearer <token_buraya_gelecek>` şeklinde göndermeniz gerekir.
    *   **Örnek (Python ile):**
        ```python
        import requests

        # Giriş yapmak için
        token_url = "http://127.0.0.1:8000/token"
        login_data = {"username": "sizin_emailiniz@example.com", "password": "sizin_sifreniz"}
        token_response = requests.post(token_url, data=login_data)
        access_token = token_response.json()["access_token"]

        # Müzik eklemek için (giriş gerektiren bir işlem)
        music_url = "http://127.0.0.1:8000/v1/music/"
        headers = {"Authorization": f"Bearer {access_token}"}
        music_data = {"title": "Yeni Şarkı", "artist_ids": ["bir_sanatci_id"], "duration": 180, "file_path": "/path/to/song.mp3", "publish_date": "2023-01-01T00:00:00Z"}
        response = requests.post(music_url, json=music_data, headers=headers)
        print(response.json())
        ```

4.  **Dosya Yükleme (Müzik ve Kapak Resimleri):**
    *   Müzik dosyalarınızı veya albüm kapaklarınızı sisteme yüklemek için özel adresler bulunur. Bu işlemler için giriş yapmanıza gerek yoktur.
    *   Yüklediğiniz dosyalar, sistemin `library` klasörüne kaydedilir ve `http://127.0.0.1:8000/library/` adresi altında erişilebilir olur.
    *   **Örnek (Python ile müzik yükleme):**
        ```python
        import requests
        import os

        upload_url = "http://127.0.0.1:8000/upload-music"
        music_file_path = "C:/Users/Siz/Muziklerim/harika_sarki.mp3" # Kendi dosya yolunuzu yazın

        files = {
            "music_files": (os.path.basename(music_file_path), open(music_file_path, "rb"), "audio/mpeg")
        }

        response = requests.post(upload_url, files=files)
        print(response.json())
        ```

5.  **Veri Gönderme ve Alma (JSON Formatı):**
    *   Sistemle konuşurken, genellikle bilgileri "JSON" formatında gönderir ve alırsınız. JSON, bilgisayarların kolayca anlayabileceği bir veri biçimidir.
    *   API dokümantasyonunda her işlem için hangi bilgileri JSON olarak göndermeniz gerektiği ve sistemin size nasıl bir JSON cevabı vereceği gösterilir.


### 2. Web Arayüzü ile (Basit Kullanım)

Sistemin basit bir web arayüzü de var. Tarayıcınızda şu adresleri ziyaret ederek kullanabilirsiniz:

*   **Ana Sayfa:** `http://127.0.0.1:8000/`
*   **Müzikler Sayfası:** `http://127.0.0.1:8000/music_page`
*   **Albümler Sayfası:** `http://127.0.0.1:8000/albums_page`
*   **Sanatçı Sayfası:** `http://127.0.0.1:8000/artists_page/{sanatci_id}` (Buradaki `{sanatci_id}` yerine bir sanatçının özel numarasını yazmanız gerekir.)

Bu sayfalar üzerinden müziklerinizi, albümlerinizi ve sanatçılarınızı görebilir, yeni kullanıcı kaydedebilir ve müzik/albüm kapakları yükleyebilirsiniz.

## Geliştirme ve Katkıda Bulunma

Eğer bu projeyi daha da geliştirmek isterseniz, kodları inceleyebilir ve değişiklikler yapabilirsiniz. Katkılarınız her zaman bekleriz!
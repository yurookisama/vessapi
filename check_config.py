#!/usr/bin/env python3
"""
VessAPI Konfigürasyon Kontrol Scripti

Bu script, VessAPI'nin doğru şekilde yapılandırılıp yapılandırılmadığını kontrol eder.
Kurulum sonrası sorunları tespit etmek için kullanılabilir.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Python sürümünü kontrol et"""
    print("🐍 Python Sürümü Kontrolü")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (Uyumlu)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Python 3.8+ gerekli)")
        return False

def check_env_file():
    """Konfigürasyon dosyasını kontrol et"""
    print("\n📄 Konfigürasyon Dosyası Kontrolü")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("   ✅ .env dosyası mevcut")
        return True
    elif env_example.exists():
        print("   ⚠️  .env dosyası yok, .env.example mevcut")
        print("   💡 Çözüm: cp .env.example .env")
        return False
    else:
        print("   ❌ Ne .env ne de .env.example dosyası bulunamadı")
        return False

def check_directories():
    """Gerekli klasörleri kontrol et"""
    print("\n📁 Klasör Yapısı Kontrolü")
    
    required_dirs = [
        "library",
        "library/music",
        "library/images",
        "library/images/album_image",
        "library/images/music_image",
        "library/images/user_image",
        "library/images/artist_image",
    ]
    
    all_good = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path} (eksik)")
            all_good = False
    
    if not all_good:
        print("   💡 Çözüm: Uygulama ilk çalıştırıldığında otomatik oluşturulacak")
    
    return all_good

def check_dependencies():
    """Python bağımlılıklarını kontrol et"""
    print("\n📦 Bağımlılık Kontrolü")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "beanie",
        "motor",
        "pydantic",
        "pydantic_settings",
        "python_jose",
        "passlib",
        "python_multipart",
        "jinja2",
        "aiofiles",
        "mutagen",
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "python_jose":
                import jose
            elif package == "python_multipart":
                import multipart
            elif package == "pydantic_settings":
                import pydantic_settings
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (eksik)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   💡 Çözüm: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_mongodb_connection():
    """MongoDB bağlantısını kontrol et"""
    print("\n🍃 MongoDB Bağlantı Kontrolü")
    
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        import asyncio
        
        async def test_connection():
            try:
                # .env dosyasından DATABASE_URL'yi oku
                from vessapi.config import settings
                client = AsyncIOMotorClient(settings.database.url)
                
                # Ping testi
                await client.admin.command('ping')
                print(f"   ✅ MongoDB bağlantısı başarılı ({settings.database.url})")
                return True
            except Exception as e:
                print(f"   ❌ MongoDB bağlantı hatası: {e}")
                print("   💡 Çözüm: MongoDB servisinin çalıştığından emin olun (mongod)")
                return False
        
        return asyncio.run(test_connection())
        
    except ImportError as e:
        print(f"   ❌ MongoDB bağımlılıkları eksik: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Beklenmeyen hata: {e}")
        return False

def check_config_values():
    """Konfigürasyon değerlerini kontrol et"""
    print("\n⚙️  Konfigürasyon Değerleri Kontrolü")
    
    try:
        from vessapi.config import settings
        
        # Secret key kontrolü
        if settings.security.secret_key == "your-super-secret-key-change-this-in-production":
            print("   ⚠️  SECRET_KEY varsayılan değerde (güvenlik riski)")
            print("   💡 Çözüm: .env dosyasında SECRET_KEY değerini değiştirin")
        else:
            print("   ✅ SECRET_KEY özelleştirilmiş")
        
        # Database URL kontrolü
        print(f"   ℹ️  Database URL: {settings.database.url}")
        print(f"   ℹ️  Database Name: {settings.database.name}")
        
        # Server ayarları
        print(f"   ℹ️  Server: {settings.server.host}:{settings.server.port}")
        print(f"   ℹ️  Debug Mode: {settings.server.debug}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Konfigürasyon yükleme hatası: {e}")
        return False

def main():
    """Ana kontrol fonksiyonu"""
    print("🔍 VessAPI Konfigürasyon Kontrolü")
    print("=" * 50)
    
    checks = [
        ("Python Sürümü", check_python_version),
        ("Konfigürasyon Dosyası", check_env_file),
        ("Klasör Yapısı", check_directories),
        ("Python Bağımlılıkları", check_dependencies),
        ("Konfigürasyon Değerleri", check_config_values),
        ("MongoDB Bağlantısı", check_mongodb_connection),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ❌ {name} kontrolü sırasında hata: {e}")
            results.append((name, False))
    
    # Sonuçları özetle
    print("\n" + "=" * 50)
    print("📊 Kontrol Sonuçları")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ BAŞARILI" if result else "❌ BAŞARISIZ"
        print(f"{name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nToplam: {passed}/{total} kontrol başarılı")
    
    if passed == total:
        print("\n🎉 Tüm kontroller başarılı! VessAPI kullanıma hazır.")
        print("💡 Uygulamayı başlatmak için: python -m uvicorn main:app --reload")
    else:
        print(f"\n⚠️  {total - passed} sorun tespit edildi. Lütfen yukarıdaki çözümleri uygulayın.")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""
VessAPI Konfigürasyon Yönetimi

Bu modül, uygulamanın tüm konfigürasyon ayarlarını yönetir.
Ortam değişkenlerinden (.env dosyası) ayarları okur ve varsayılan değerler sağlar.
"""

import os
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseModel):
    """Veritabanı ayarları"""
    url: str = Field(default="mongodb://localhost:27017", description="MongoDB bağlantı URL'si")
    name: str = Field(default="vessapi", description="Veritabanı adı")
    test_url: str = Field(default="mongodb://localhost:27017/vessapi_test", description="Test veritabanı URL'si")


class SecuritySettings(BaseModel):
    """Güvenlik ayarları"""
    secret_key: str = Field(default="your-super-secret-key-change-this-in-production", description="JWT şifreleme anahtarı")
    algorithm: str = Field(default="HS256", description="JWT şifreleme algoritması")
    access_token_expire_minutes: int = Field(default=30, description="Token geçerlilik süresi (dakika)")


class ServerSettings(BaseModel):
    """Sunucu ayarları"""
    host: str = Field(default="0.0.0.0", description="Sunucu host adresi")
    port: int = Field(default=8000, description="Sunucu portu")
    debug: bool = Field(default=False, description="Debug modu")
    cors_origins: List[str] = Field(default=["*"], description="CORS izin verilen origin'ler")


class FileSettings(BaseModel):
    """Dosya yönetimi ayarları"""
    music_upload_directory: str = Field(default="library/music", description="Müzik dosyaları klasörü")
    album_image_directory: str = Field(default="library/images/album_image", description="Albüm kapakları klasörü")
    music_image_directory: str = Field(default="library/images/music_image", description="Müzik kapakları klasörü")
    user_image_directory: str = Field(default="library/images/user_image", description="Kullanıcı resimleri klasörü")
    artist_image_directory: str = Field(default="library/images/artist_image", description="Sanatçı resimleri klasörü")
    
    # Dosya boyutu limitleri (MB)
    max_music_file_size: int = Field(default=100, description="Maksimum müzik dosyası boyutu (MB)")
    max_image_file_size: int = Field(default=10, description="Maksimum resim dosyası boyutu (MB)")
    
    # Desteklenen formatlar
    supported_music_formats: List[str] = Field(default=["mp3", "flac", "ogg", "wav", "m4a"], description="Desteklenen müzik formatları")
    supported_image_formats: List[str] = Field(default=["jpg", "jpeg", "png", "webp"], description="Desteklenen resim formatları")


class LoggingSettings(BaseModel):
    """Loglama ayarları"""
    level: str = Field(default="INFO", description="Log seviyesi")
    file: Optional[str] = Field(default=None, description="Log dosyası yolu")


class Settings(BaseSettings):
    """Ana konfigürasyon sınıfı"""
    
    # Alt konfigürasyon grupları
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    files: FileSettings = Field(default_factory=FileSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    
    # Geriye uyumluluk için direkt erişim
    DATABASE_URL: Optional[str] = Field(default=None, description="Veritabanı URL (geriye uyumluluk)")
    DATABASE_NAME: Optional[str] = Field(default=None, description="Veritabanı adı (geriye uyumluluk)")
    SECRET_KEY: Optional[str] = Field(default=None, description="Secret key (geriye uyumluluk)")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "allow"
    }
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Ortam değişkenlerinden ayarları oku
        self._load_from_env()
        
        # Geriye uyumluluk için eski değişkenleri kontrol et
        self._handle_legacy_vars()
    
    def _load_from_env(self):
        """Ortam değişkenlerinden ayarları yükle"""
        
        # Veritabanı ayarları
        if os.getenv("DATABASE_URL"):
            self.database.url = os.getenv("DATABASE_URL")
        if os.getenv("DATABASE_NAME"):
            self.database.name = os.getenv("DATABASE_NAME")
        if os.getenv("TEST_DATABASE_URL"):
            self.database.test_url = os.getenv("TEST_DATABASE_URL")
            
        # Güvenlik ayarları
        if os.getenv("SECRET_KEY"):
            self.security.secret_key = os.getenv("SECRET_KEY")
        if os.getenv("ALGORITHM"):
            self.security.algorithm = os.getenv("ALGORITHM")
        if os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"):
            self.security.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
            
        # Sunucu ayarları
        if os.getenv("HOST"):
            self.server.host = os.getenv("HOST")
        if os.getenv("PORT"):
            self.server.port = int(os.getenv("PORT"))
        if os.getenv("DEBUG"):
            self.server.debug = os.getenv("DEBUG").lower() in ("true", "1", "yes")
        if os.getenv("CORS_ORIGINS"):
            self.server.cors_origins = os.getenv("CORS_ORIGINS").split(",")
            
        # Dosya ayarları
        if os.getenv("MUSIC_UPLOAD_DIRECTORY"):
            self.files.music_upload_directory = os.getenv("MUSIC_UPLOAD_DIRECTORY")
        if os.getenv("ALBUM_IMAGE_DIRECTORY"):
            self.files.album_image_directory = os.getenv("ALBUM_IMAGE_DIRECTORY")
        if os.getenv("MUSIC_IMAGE_DIRECTORY"):
            self.files.music_image_directory = os.getenv("MUSIC_IMAGE_DIRECTORY")
        if os.getenv("USER_IMAGE_DIRECTORY"):
            self.files.user_image_directory = os.getenv("USER_IMAGE_DIRECTORY")
        if os.getenv("ARTIST_IMAGE_DIRECTORY"):
            self.files.artist_image_directory = os.getenv("ARTIST_IMAGE_DIRECTORY")
            
        # Loglama ayarları
        if os.getenv("LOG_LEVEL"):
            self.logging.level = os.getenv("LOG_LEVEL")
        if os.getenv("LOG_FILE"):
            self.logging.file = os.getenv("LOG_FILE")
    
    def _handle_legacy_vars(self):
        """Geriye uyumluluk için eski değişkenleri işle"""
        if self.DATABASE_URL:
            self.database.url = self.DATABASE_URL
        if self.DATABASE_NAME:
            self.database.name = self.DATABASE_NAME
        if self.SECRET_KEY:
            self.security.secret_key = self.SECRET_KEY
    
    def create_directories(self):
        """Gerekli klasörleri oluştur"""
        directories = [
            self.files.music_upload_directory,
            self.files.album_image_directory,
            self.files.music_image_directory,
            self.files.user_image_directory,
            self.files.artist_image_directory,
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def get_database_url(self, test_mode: bool = False) -> str:
        """Veritabanı URL'sini al"""
        if test_mode:
            return self.database.test_url
        return self.database.url
    
    def get_full_database_url(self, test_mode: bool = False) -> str:
        """Tam veritabanı URL'sini al (veritabanı adı ile birlikte)"""
        base_url = self.get_database_url(test_mode)
        if test_mode:
            return base_url  # Test URL'si zaten veritabanı adını içeriyor
        return f"{base_url}/{self.database.name}"


# Global settings instance
settings = Settings()

# Geriye uyumluluk için
DATABASE_URL = settings.database.url
DATABASE_NAME = settings.database.name
SECRET_KEY = settings.security.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = settings.security.access_token_expire_minutes
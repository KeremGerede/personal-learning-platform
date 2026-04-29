# AI Destekli Kişisel Öğrenme Planlayıcı

Bu proje, kullanıcının öğrenmek istediği konuya, mevcut seviyesine, hedeflerine, haftalık ayırabileceği süreye ve öğrenme tercihine göre yapay zekâ destekli kişisel öğrenme planı oluşturan bir platformdur.

Sistem, kullanıcıdan aldığı bilgilerle haftalara ayrılmış bir öğrenme yol haritası üretir. Her hafta için görevler, tahmini çalışma süresi, zorluk seviyesi, mini proje, kaynak önerileri ve haftalık quizler oluşturulur. Kullanıcı görevleri tamamladıkça ilerleme yüzdesi otomatik olarak güncellenir.

---

## Projenin Amacı

Günümüzde öğrenmek isteyen kullanıcılar çok fazla kaynakla karşılaşmakta, ancak nereden başlayacaklarını veya nasıl düzenli ilerleyeceklerini belirlemekte zorlanmaktadır.

Bu projenin amacı, kullanıcının öğrenme hedefini daha yönetilebilir parçalara bölerek kişiselleştirilmiş bir öğrenme planı sunmaktır.

Sistem şu sorulara çözüm üretmeyi hedefler:

- Kullanıcı hangi konudan başlamalı?
- Hangi sırayla ilerlemeli?
- Haftalık ne kadar çalışmalı?
- Hangi görevleri tamamlamalı?
- Hangi kaynaklardan yararlanmalı?
- Öğrendiğini nasıl test etmeli?

---

## Hedef Kitle

Bu platform aşağıdaki kullanıcı gruplarına hitap eder:

- Üniversite öğrencileri
- Yeni bir konu öğrenmek isteyen bireyler
- Kendi kendine öğrenme sürecini planlamak isteyen kullanıcılar
- Yazılım, yapay zekâ, veri analizi veya DevOps gibi alanlarda gelişmek isteyen kişiler
- Belirli bir hedef doğrultusunda düzenli çalışma planına ihtiyaç duyan öğreniciler

---

## Kullanılan Teknolojiler

| Katman | Teknoloji |
|---|---|
| Backend | FastAPI |
| Veritabanı | SQLite |
| ORM | SQLAlchemy |
| AI Servisi | Gemini API |
| Test Arayüzü | Streamlit |
| HTTP İstekleri | requests |
| Ortam Değişkenleri | python-dotenv |
| Frontend | React planlanıyor |

---

## Mevcut Özellikler

- Yapay zekâ destekli kişisel öğrenme planı oluşturma
- Planları SQLite veritabanına kaydetme
- Plan listeleme
- Plan detaylarını görüntüleme
- Plan silme
- Haftalık öğrenme planı gösterme
- Plan özeti ve plan sonu kazanım gösterme
- Haftalık tahmini çalışma süresi gösterme
- Haftalık mini proje önerisi gösterme
- Görev türü gösterme
- Görev tahmini süresi gösterme
- Görev zorluk seviyesi gösterme
- Görevleri checkbox ile tamamlandı olarak işaretleme
- İlerleme yüzdesi hesaplama
- Genel dashboard istatistikleri gösterme
- Kaynak önerileri gösterme
- Kaynak bağlantısı varsa bağlantı butonu gösterme
- Haftalık quiz oluşturma
- Quiz cevaplarını kontrol etme
- Quiz skorunu hesaplama
- Gemini hata verdiğinde local fallback plan üretme

---

## Bilinçli Olarak Eklenmeyen Özellikler

İlk MVP kapsamını sade tutmak için bazı özellikler henüz eklenmemiştir:

- Kullanıcı kayıt/giriş sistemi
- E-posta ile authentication
- Kullanıcı bazlı plan ayrımı
- RAG sistemi
- OpenAI fallback
- Admin panel
- React frontend
- Deployment
- Quiz sonuçlarını veritabanına kaydetme

Bu özellikler sonraki geliştirme aşamalarında eklenebilir.

---

## Proje Mimarisi

```text
personal-learning-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── ai_service.py
│   │   └── routes/
│   │       ├── plans.py
│   │       ├── tasks.py
│   │       ├── quiz.py
│   │       └── stats.py
│   │
│   ├── streamlit_app.py
│   ├── learning.db
│   ├── .env
│   └── requirements.txt
│
└── README.md
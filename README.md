# AI Destekli Kişisel Öğrenme Planlayıcı

Bu proje, kullanıcının öğrenmek istediği konuya, mevcut seviyesine, hedeflerine, haftalık ayırabileceği süreye ve öğrenme tercihine göre yapay zekâ destekli kişisel öğrenme planı oluşturan bir platformdur.

Sistem, kullanıcıdan aldığı bilgilerle haftalara ayrılmış kişiselleştirilmiş bir öğrenme yol haritası üretir. Her hafta için görevler, tahmini çalışma süresi, zorluk seviyesi, mini proje, kaynak önerileri ve haftalık quizler oluşturulur. Kullanıcı görevleri tamamladıkça ilerleme yüzdesi otomatik olarak güncellenir. Quiz sonuçları ve soru/cevap detayları veritabanına kaydedilerek daha sonra tekrar görüntülenebilir.

---

## Projenin Amacı

Günümüzde öğrenmek isteyen kullanıcılar çok fazla kaynakla karşılaşmakta, ancak nereden başlayacaklarını, hangi sırayla ilerleyeceklerini veya öğrenme sürecini nasıl takip edeceklerini belirlemekte zorlanmaktadır.

Bu projenin amacı, kullanıcının öğrenme hedefini daha yönetilebilir parçalara bölerek kişiselleştirilmiş, haftalık ve takip edilebilir bir öğrenme planı sunmaktır.

Sistem şu sorulara çözüm üretmeyi hedefler:

- Kullanıcı hangi konudan başlamalı?
- Hangi sırayla ilerlemeli?
- Haftalık ne kadar çalışmalı?
- Hangi görevleri tamamlamalı?
- Hangi kaynaklardan yararlanmalı?
- Öğrendiğini nasıl test etmeli?
- Gelişimini nasıl takip etmeli?

---

## Hedef Kitle

Bu platform aşağıdaki kullanıcı gruplarına hitap eder:

- Üniversite öğrencileri
- Yeni bir konu öğrenmek isteyen bireyler
- Kendi kendine öğrenme sürecini planlamak isteyen kullanıcılar
- Yazılım, yapay zekâ, veri analizi, DevOps veya benzeri teknik alanlarda gelişmek isteyen kişiler
- Belirli bir hedef doğrultusunda düzenli çalışma planına ihtiyaç duyan öğreniciler

---

## Kullanılan Teknolojiler

| Katman | Teknoloji | Kullanım Amacı |
|---|---|---|
| Backend | FastAPI | API endpointlerini geliştirmek için kullanıldı. |
| Veritabanı | SQLite | MVP aşamasında hafif ve kolay kurulabilir veritabanı olarak kullanıldı. |
| ORM | SQLAlchemy | Python modelleri ile veritabanı tabloları arasındaki ilişkiyi yönetmek için kullanıldı. |
| AI Servisi | Gemini API | Öğrenme planı ve haftalık quiz üretimi için kullanıldı. |
| Test Arayüzü | Streamlit | Backend geliştirme ve hızlı test için kullanıldı. |
| Frontend | React | Nihai kullanıcı arayüzünü oluşturmak için kullanıldı. |
| Frontend Build Tool | Vite | React projesini hızlı geliştirmek ve çalıştırmak için kullanıldı. |
| Styling | Tailwind CSS | Modern, responsive ve dark theme arayüz tasarımı için kullanıldı. |
| HTTP İstekleri | fetch / requests | React ve Streamlit arayüzlerinden FastAPI backend'e istek göndermek için kullanıldı. |
| Ortam Değişkenleri | python-dotenv | Gemini API key gibi hassas bilgileri `.env` dosyasından okumak için kullanıldı. |
| Veri Doğrulama | Pydantic | API request ve response şemalarını tanımlamak için kullanıldı. |
| ASGI Server | Uvicorn | FastAPI uygulamasını çalıştırmak için kullanıldı. |

---

## MVP Kapsamı

Bu proje şu anda çalışan bir MVP seviyesindedir.

Bu aşamada bilinçli olarak eklenmeyen özellikler:

- Kullanıcı kayıt/giriş sistemi
- E-posta ile authentication
- Kullanıcı bazlı veri ayrımı
- RAG sistemi
- OpenAI fallback
- Admin panel
- Deployment

MVP kapsamındaki amaç, önce çalışan ve sunulabilir bir yapay zekâ destekli öğrenme planlama sistemi oluşturmaktır.

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
│   │       ├── quiz_results.py
│   │       └── stats.py
│   │
│   ├── streamlit_app.py
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── apiClient.js
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── MobileNavigation.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── PlanCard.jsx
│   │   │   └── WeeklyQuizPanel.jsx
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── PlanCreatorPage.jsx
│   │   │   ├── MyPlansPage.jsx
│   │   │   ├── PlanDetailPage.jsx
│   │   │   ├── QuizResultsPage.jsx
│   │   │   └── ResourcesPage.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── node_modules/
│
├── README.md
└── .gitignore
```

---

## Backend Modülleri

### `main.py`

FastAPI uygulamasının ana giriş dosyasıdır.

Görevleri:

- FastAPI uygulamasını başlatır.
- CORS ayarlarını yapar.
- Veritabanı tablolarını oluşturur.
- Router dosyalarını uygulamaya dahil eder.
- `/health` endpointi ile backend sağlık kontrolü sağlar.

---

### `database.py`

SQLite bağlantısının ve SQLAlchemy session yapısının oluşturulduğu dosyadır.

Görevleri:

- SQLite bağlantısını kurar.
- SQLAlchemy `Base` yapısını oluşturur.
- Endpointlerde kullanılacak `get_db()` fonksiyonunu sağlar.

---

### `models.py`

Veritabanı tablolarını temsil eden SQLAlchemy modellerini içerir.

Ana modeller:

- `LearningPlan`
- `PlanWeek`
- `PlanTask`
- `PlanResource`
- `QuizResult`

---

### `schemas.py`

API request ve response formatlarını tanımlayan Pydantic şemalarını içerir.

Ana şemalar:

- `GeneratePlanRequest`
- `PlanResponse`
- `WeekResponse`
- `TaskResponse`
- `ResourceResponse`
- `ProgressResponse`
- `QuizResponse`
- `QuizResultCreate`
- `QuizResultResponse`
- `StatsOverviewResponse`

---

### `ai_service.py`

Gemini API entegrasyonunun ve AI tabanlı üretim mantığının bulunduğu dosyadır.

Görevleri:

- Gemini API client oluşturur.
- Öğrenme planı promptunu hazırlar.
- Haftalık quiz promptunu hazırlar.
- Gemini’den JSON formatında cevap alır.
- Gemini cevaplarını parse eder.
- Plan çıktısını normalize eder.
- Quiz çıktısını normalize eder.
- Quiz seçeneklerini karıştırır.
- Gemini hata verdiğinde local fallback plan üretir.
- Gemini hata verdiğinde local fallback quiz üretir.

---

## Veritabanı Yapısı

### `learning_plans`

Öğrenme planının genel bilgilerini tutar.

Alanlar:

- `id`
- `topic`
- `level`
- `goal`
- `weekly_hours`
- `duration_weeks`
- `learning_preference`
- `summary`
- `final_outcome`
- `created_at`

---

### `plan_weeks`

Her öğrenme planına bağlı haftalık bölümleri tutar.

Alanlar:

- `id`
- `plan_id`
- `week_number`
- `title`
- `description`
- `estimated_hours`
- `mini_project`

---

### `plan_tasks`

Her haftaya bağlı görevleri tutar.

Alanlar:

- `id`
- `week_id`
- `task_text`
- `is_completed`
- `task_type`
- `estimated_minutes`
- `difficulty`

---

### `plan_resources`

Her haftaya bağlı kaynak önerilerini tutar.

Alanlar:

- `id`
- `week_id`
- `resource_title`
- `resource_type`
- `resource_description`
- `resource_url`

---

### `quiz_results`

Kullanıcının tamamladığı quiz sonuçlarını tutar.

Alanlar:

- `id`
- `plan_id`
- `week_id`
- `quiz_title`
- `correct_count`
- `total_questions`
- `score_percentage`
- `details_json`
- `created_at`

`details_json` alanı, quiz soru/cevap detaylarını JSON string olarak saklar.

Örnek içerik:

```json
[
  {
    "question_number": 1,
    "question": "Soru metni",
    "selected_answer": "Kullanıcının seçtiği cevap",
    "correct_answer": "Doğru cevap",
    "is_correct": true,
    "explanation": "Cevabın açıklaması"
  }
]
```

---

## Mevcut Özellikler

### Backend Özellikleri

- Yapay zekâ destekli kişisel öğrenme planı oluşturma
- Gemini API ile plan üretimi
- Gemini API ile haftalık quiz üretimi
- Gemini hata verdiğinde local fallback plan üretimi
- Gemini hata verdiğinde local fallback quiz üretimi
- AI çıktısı için plan normalizer
- Quiz çıktısı için güvenli veri yapısı kontrolü
- Quiz seçeneklerini karıştırma
- Planları SQLite veritabanına kaydetme
- Plan listeleme
- Plan detaylarını görüntüleme
- Plan silme
- Haftalık görevleri kaydetme
- Haftalık kaynakları kaydetme
- Görev tamamlanma durumunu güncelleme
- İlerleme yüzdesi hesaplama
- Dashboard istatistikleri üretme
- Quiz sonuçlarını veritabanına kaydetme
- Quiz soru/cevap detaylarını `details_json` alanında saklama
- Kayıtlı quiz sonuçlarını listeleme
- Backend sağlık kontrol endpointi
- React ve Streamlit için CORS ayarları
- Response sıralaması: haftalar, görevler ve kaynaklar düzenli sırada döner

---

### React Frontend Özellikleri

- Dashboard sayfası
- Backend health check gösterimi
- Genel plan/görev/quiz istatistik kartları
- Plan oluşturma sayfası
- Plan başarıyla oluşturulduktan sonra plan detayına gitme butonu
- Planlarım sayfası
- Plan silme
- Plan detay sayfası
- Haftalık görevleri görüntüleme
- Görev tamamlama checkbox sistemi
- Haftalık kaynakları görüntüleme
- Haftalık quiz oluşturma
- Quiz çözme
- Quiz skor hesaplama
- Quiz sonucunu veritabanına kaydetme
- Kaydedilmiş quiz sonuçlarını görüntüleme
- Quiz soru/cevap detaylarını görüntüleme
- Quiz Sonuçları sayfası
- Resources sayfası
- Resources sayfasında hedef/plan bazlı gruplama
- Kaynak arama ve kaynak tipi filtresi
- Mobil/tablet görünüm için Mobile Navigation
- Desktop görünüm için Sidebar navigation

---

### Streamlit Test UI Özellikleri

- Plan oluşturma
- Plan listeleme
- Plan detay görüntüleme
- Görev tamamlama
- Quiz oluşturma
- Quiz çözme
- Quiz sonucu kaydetme
- Dashboard metriklerini görüntüleme

---

## API Endpointleri

### Genel

```http
GET /
```

API'nin çalışıp çalışmadığını kontrol eder.

```http
GET /health
```

Backend sağlık kontrolünü döndürür.

Örnek response:

```json
{
  "status": "ok",
  "database": "connected",
  "ai_provider": "gemini"
}
```

---

### Plan Endpointleri

```http
POST /plans/generate
```

Kullanıcıdan gelen bilgilere göre Gemini ile kişiselleştirilmiş öğrenme planı oluşturur ve veritabanına kaydeder.

Örnek request:

```json
{
  "topic": "Jenkins",
  "level": "Başlangıç",
  "goal": "Stajımda CI/CD süreçlerini anlayıp basit pipeline yazabilmek",
  "weekly_hours": 5,
  "duration_weeks": 4,
  "learning_preference": "Uygulamalı proje ağırlıklı"
}
```

```http
GET /plans
```

Veritabanındaki tüm öğrenme planlarını listeler.

```http
GET /plans/{plan_id}
```

Belirli bir öğrenme planını haftaları, görevleri ve kaynaklarıyla birlikte getirir.

```http
DELETE /plans/{plan_id}
```

Belirli bir öğrenme planını siler. Plana bağlı haftalar, görevler, kaynaklar ve quiz sonuçları da temizlenir.

```http
GET /plans/{plan_id}/progress
```

Belirli bir öğrenme planındaki görevlerin tamamlanma yüzdesini hesaplar.

---

### Görev Endpointleri

```http
PATCH /tasks/{task_id}/complete?is_completed=true
```

Bir görevin tamamlandı/tamamlanmadı durumunu günceller.

---

### Quiz Endpointleri

```http
POST /quiz/plans/{plan_id}/weeks/{week_id}/generate
```

Belirli bir planın belirli haftası için Gemini ile haftalık quiz üretir.

---

### Quiz Sonuçları Endpointleri

```http
POST /quiz-results/
```

Kullanıcının tamamladığı quiz sonucunu veritabanına kaydeder.

```http
GET /quiz-results/
```

Tüm kayıtlı quiz sonuçlarını listeler.

```http
GET /quiz-results/plan/{plan_id}
```

Belirli bir plana ait quiz sonuçlarını listeler.

```http
GET /quiz-results/week/{week_id}
```

Belirli bir haftaya ait quiz sonuçlarını listeler.

---

### İstatistik Endpointleri

```http
GET /stats/overview
```

Dashboard için genel istatistikleri döndürür.

Örnek response:

```json
{
  "total_plans": 5,
  "total_tasks": 80,
  "completed_tasks": 20,
  "overall_progress_percentage": 25.0,
  "total_quizzes": 6,
  "average_quiz_score": 72.5,
  "latest_quiz_score": 80.0
}
```

---

## LLM Prompt Yapısı

Projede kullanılan LLM promptları aşağıdaki standart yapıya göre hazırlanır:

1. **Context**  
   Modele verilen arka plan bilgisi.

2. **Role**  
   Modelin üstleneceği rol.

3. **Constraints**  
   Modelin uyması gereken kurallar.

4. **Task**  
   Modelin yapması gereken iş.

5. **Template Variables**  
   Kullanıcıdan veya sistemden gelen dinamik veriler.

6. **Output Control**  
   Beklenen çıktı formatı.

Prompt dili İngilizcedir. Kullanıcıya gösterilen içerikler Türkçe üretilir.

---

## Kurulum

### 1. Projeyi klonla veya proje klasörüne gir

```bash
cd personal-learning-platform
```

---

## Backend Kurulumu

### 1. Backend klasörüne gir

```bash
cd backend
```

### 2. Sanal ortam oluştur

```bash
python -m venv venv
```

### 3. Sanal ortamı aktif et

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 4. Gerekli paketleri kur

```bash
pip install -r requirements.txt
```

### 5. `.env` dosyası oluştur

`backend/.env` dosyasını oluştur:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Alternatif olarak `.env.example` dosyasını kopyalayabilirsin:

Windows:

```bash
copy .env.example .env
```

Mac/Linux:

```bash
cp .env.example .env
```

Daha sonra `.env` içindeki `GEMINI_API_KEY` alanını kendi Gemini API key'in ile değiştir.

### 6. FastAPI backend'i çalıştır

```bash
uvicorn app.main:app --reload
```

Backend Swagger arayüzü:

```text
http://127.0.0.1:8000/docs
```

Health endpoint:

```text
http://127.0.0.1:8000/health
```

---

## Streamlit Test UI Çalıştırma

Streamlit arayüzü geliştirme ve backend testi için kullanılabilir.

Backend klasöründeyken:

```bash
streamlit run streamlit_app.py
```

Streamlit arayüzü:

```text
http://localhost:8501
```

---

## React Frontend Kurulumu

### 1. Frontend klasörüne gir

Proje ana dizinindeyken:

```bash
cd frontend
```

### 2. Gerekli paketleri kur

```bash
npm install
```

### 3. React frontend'i çalıştır

```bash
npm run dev
```

React arayüzü:

```text
http://localhost:5173
```

Not: Backend'in çalışıyor olması gerekir. React frontend, FastAPI backend'e `http://127.0.0.1:8000` üzerinden istek gönderir.

---

## Kullanım Akışı

1. Kullanıcı React arayüzünü açar.
2. Dashboard üzerinden genel durumu görüntüler.
3. Plan Oluştur sayfasından öğrenmek istediği konuyu ve hedefini girer.
4. Sistem Gemini API ile kişiselleştirilmiş öğrenme planı oluşturur.
5. Kullanıcı oluşturulan planın detayına geçer.
6. Plan detayında haftalık görevleri, kaynakları ve mini projeleri görüntüler.
7. Görevleri tamamladıkça checkbox ile işaretler.
8. Haftalık quiz oluşturur.
9. Quiz sorularını çözer.
10. Quiz sonucunu ve soru/cevap detaylarını kaydeder.
11. Quiz Sonuçları sayfasından geçmiş quizlerini görüntüler.
12. Resources sayfasından tüm kaynakları hedef/plan bazlı gruplu şekilde inceleyebilir.

---

## React Frontend Sayfaları

### Dashboard

Genel sistem durumunu gösterir.

Gösterilen metrikler:

- Toplam plan
- Toplam görev
- Tamamlanan görev
- Genel ilerleme yüzdesi
- Toplam quiz
- Ortalama quiz başarısı
- En son quiz skoru
- Backend sağlık durumu

---

### Plan Oluştur

Kullanıcıdan öğrenme bilgilerini alır:

- Konu
- Seviye
- Öğrenme hedefi
- Haftalık çalışma süresi
- Plan süresi
- Öğrenme tercihi

Form gönderildiğinde `POST /plans/generate` endpointine istek atılır. Plan başarıyla oluşturulursa kullanıcı isterse direkt plan detay sayfasına geçebilir.

---

### Planlarım

Kayıtlı planları listeler.

Özellikler:

- Plan kartları
- Detayı Gör butonu
- Plan Sil butonu

---

### Plan Detayı

Seçilen planın detayını gösterir.

Özellikler:

- Plan özeti
- Plan sonu kazanım
- İlerleme yüzdesi
- Haftalık görevler
- Görev checkbox sistemi
- Haftalık mini proje
- Haftalık kaynaklar
- Haftalık quiz oluşturma
- Quiz çözme
- Quiz sonucu kaydetme
- Kaydedilmiş quiz sonuçlarını görüntüleme

---

### Quiz Sonuçları

Tüm kayıtlı quiz sonuçlarını listeler.

Özellikler:

- Quiz başlığı
- Plan ID / Hafta ID
- Skor
- Başarı yüzdesi
- Oluşturulma tarihi
- Soru/cevap detayları
- Arama filtresi

---

### Resources

Tüm planlarda önerilen kaynakları tek sayfada gösterir.

Özellikler:

- Hedef/plan bazlı gruplama
- Kaynak tipi filtresi
- Arama
- Kaynak linki varsa dış bağlantı
- Plan konusu ve hafta bilgisi

---

## `.gitignore` İçin Önerilenler

Frontend ve backend geliştirme dosyalarının GitHub'a gereksiz veya hassas dosya göndermemesi için `.gitignore` içinde şunlar bulunmalıdır:

```gitignore
# Node / React
node_modules/
frontend/node_modules/
frontend/dist/

# Environment variables
.env
.env.local
.env.*.local

# Python virtual environments
venv/
.venv/

# Python cache
__pycache__/
*.pyc

# SQLite database
*.db
*.db-shm
*.db-wal

# OS / IDE
.DS_Store
Thumbs.db
.vscode/
.idea/
```

---

## Gelecek Geliştirmeler

Planlanan geliştirmeler:

- Kullanıcı kayıt/giriş sistemi
- Kullanıcıya özel planlar
- JWT authentication
- Plan güncelleme veya yeniden oluşturma özelliği
- Daha gelişmiş dashboard grafikleri
- Streak / motivasyon sistemi
- Daha iyi kaynak öneri sistemi
- PostgreSQL desteği
- Deployment
- RAG desteği

---

## Proje Durumu

Proje şu anda çalışan bir MVP seviyesindedir.

Tamamlanan temel özellikler:

- AI destekli plan üretimi
- Veritabanına kayıt
- Görev takibi
- İlerleme hesaplama
- Plan silme
- Haftalık quiz üretimi
- Quiz skor hesaplama
- Quiz sonuçlarını ve detaylarını kaydetme
- Genel dashboard
- React frontend
- Resources sayfası
- Mobil uyumlu navigasyon

Bu haliyle proje, mezuniyet projesi için güçlü ve sunulabilir bir temel oluşturmaktadır.

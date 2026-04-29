import json
import os
import time
from typing import Any, Dict

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# ENV CONFIG
# ============================================================
# .env dosyasındaki GEMINI_API_KEY ve GEMINI_MODEL değerlerini okuyoruz.
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# ============================================================
# GEMINI CLIENT
# ============================================================
# Gemini API istemcisi. API key yoksa fonksiyon çağrıldığında hata vereceğiz.
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_learning_plan_prompt(
    topic: str,
    level: str,
    goal: str,
    weekly_hours: int,
    duration_weeks: int,
    learning_preference: str | None = None
) -> str:
    """
    Builds the prompt sent to Gemini.

    Prompt structure:
    1. Context
    2. Role
    3. Constraints
    4. Task
    5. Template variables
    6. Output control

    The prompt is written in English, but the generated learning plan content
    must be in Turkish because the application currently targets Turkish users.
    """

    return f"""
# 1. Context

You are generating a personalized learning plan for a user in an AI-powered learning platform.

The platform receives the user's learning goal, current level, available weekly study time, preferred learning style, and desired plan duration. Based on this information, the system creates a weekly learning roadmap with tasks, resources, estimated effort, difficulty level, mini projects, a general summary, and a final learning outcome.

The generated plan will be saved into a database and displayed in a learning dashboard. Therefore, the output must be consistent, structured, and easy to parse.

# 2. Role

Act as an expert AI learning coach, curriculum designer, and educational planner.

You should design a realistic, beginner-friendly, actionable, and personalized learning roadmap.

# 3. Constraints

- Return only valid JSON.
- Do not use Markdown.
- Do not add explanations outside the JSON.
- The JSON must be parseable by Python's json.loads().
- The learning plan content must be written in Turkish.
- The total number of weeks must be exactly {duration_weeks}.
- Each week must include at least 4 tasks.
- Each week must include at least 2 learning resources.
- Each week must include exactly one mini project in the mini_project field.
- Do not include the mini project as a task inside the tasks array.
- The mini project must only appear in the mini_project field.
- The summary field must briefly explain the overall purpose of the plan.
- The final_outcome field must explain what the user will be able to do after completing the plan.
- summary and final_outcome must be written in Turkish.
- Each task must be specific, measurable, and actionable.
- task_text must be written as a clear action sentence.
- task_text should not use a title-colon-description format.
- Avoid task_text values like "Topic: explanation".
- Prefer action-oriented Turkish task sentences.
- Do not write the task type inside task_text.
- Do not add labels like "(Teori)", "(Uygulama)", "(Proje)" inside task_text.
- task_type must be one of: "Teori", "Uygulama", "Proje", "Tekrar", "Araştırma".
- difficulty must be one of: "Kolay", "Orta", "Zor".
- estimated_minutes must be a positive integer.
- The total estimated_minutes of all tasks in a week should approximately match {weekly_hours} hours.
- estimated_hours for each week should be close to {weekly_hours}.
- Resource URLs may be null if you are not sure about the exact URL.
- Prefer reliable and beginner-friendly resources.
- Avoid overly generic tasks such as "research the topic".
- Avoid duplicate tasks within the same week.
- Make the plan suitable for the user's current level.
- The plan should gradually increase in difficulty.

# 4. Task

Generate a personalized weekly learning plan for the user.

The plan should help the user move from their current level toward their stated learning goal. The output must include a general plan summary, a final learning outcome, and weekly learning sections. Each week should have a clear theme, a short description, estimated study hours, actionable tasks, a mini project, and learning resources.

# 5. Template Variables

User input:

- topic: "{topic}"
- current_level: "{level}"
- learning_goal: "{goal}"
- weekly_hours: {weekly_hours}
- duration_weeks: {duration_weeks}
- learning_preference: "{learning_preference or "Belirtilmedi"}"

# 6. Output Control

Return the output using exactly this JSON structure:

{{
  "topic": "{topic}",
  "level": "{level}",
  "goal": "{goal}",
  "weekly_hours": {weekly_hours},
  "duration_weeks": {duration_weeks},
  "learning_preference": "{learning_preference or "Belirtilmedi"}",
  "summary": "Bu planın genel amacı ve kullanıcıya nasıl yardımcı olacağının kısa açıklaması",
  "final_outcome": "Bu plan tamamlandığında kullanıcının kazanacağı becerilerin açıklaması",
  "weeks": [
    {{
      "week_number": 1,
      "title": "Hafta başlığı",
      "description": "Bu haftanın kısa açıklaması",
      "estimated_hours": {weekly_hours},
      "mini_project": "Bu haftanın sonunda yapılacak mini proje veya uygulama önerisi",
      "tasks": [
        {{
          "task_text": "Görev açıklaması",
          "task_type": "Teori",
          "estimated_minutes": 60,
          "difficulty": "Kolay"
        }},
        {{
          "task_text": "Görev açıklaması",
          "task_type": "Uygulama",
          "estimated_minutes": 90,
          "difficulty": "Orta"
        }},
        {{
          "task_text": "Görev açıklaması",
          "task_type": "Tekrar",
          "estimated_minutes": 45,
          "difficulty": "Kolay"
        }},
        {{
          "task_text": "Görev açıklaması",
          "task_type": "Proje",
          "estimated_minutes": 120,
          "difficulty": "Orta"
        }}
      ],
      "resources": [
        {{
          "resource_title": "Kaynak adı",
          "resource_type": "Video / Dokümantasyon / Makale / Uygulama / Kurs",
          "resource_description": "Kaynağın neden önerildiği",
          "resource_url": null
        }},
        {{
          "resource_title": "Kaynak adı",
          "resource_type": "Video / Dokümantasyon / Makale / Uygulama / Kurs",
          "resource_description": "Kaynağın neden önerildiği",
          "resource_url": null
        }}
      ]
    }}
  ]
}}
"""


# ============================================================
# AI RESPONSE PARSER
# ============================================================

def parse_gemini_json_response(response_text: str) -> Dict[str, Any]:
    """
    Gemini'den gelen cevabı JSON'a çevirir.

    Normalde response_mime_type='application/json' kullandığımız için
    model doğrudan JSON döndürmeli. Yine de güvenlik için markdown code block
    temizliği yapıyoruz.
    """

    cleaned_text = response_text.strip()

    # Model bazen ```json ... ``` şeklinde dönerse temizliyoruz.
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text.replace("```json", "", 1).strip()

    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.replace("```", "", 1).strip()

    if cleaned_text.endswith("```"):
        cleaned_text = cleaned_text[:-3].strip()

    return json.loads(cleaned_text)


# ============================================================
# MAIN AI FUNCTION
# ============================================================

def generate_learning_plan_with_gemini(
    topic: str,
    level: str,
    goal: str,
    weekly_hours: int,
    duration_weeks: int,
    learning_preference: str | None = None
) -> Dict[str, Any]:
    """
    Gemini API ile kişiselleştirilmiş öğrenme planı üretir.

    Eğer Gemini geçici olarak cevap veremezse:
    - Birkaç kez tekrar dener
    - Yine başarısız olursa fallback plan üretir

    Bu sayede demo sırasında sistem tamamen çökmez.
    """

    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY bulunamadı. Lütfen backend/.env dosyasına GEMINI_API_KEY ekle."
        )

    prompt = build_learning_plan_prompt(
        topic=topic,
        level=level,
        goal=goal,
        weekly_hours=weekly_hours,
        duration_weeks=duration_weeks,
        learning_preference=learning_preference
    )

    max_retries = 3

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.4
                )
            )

            return parse_gemini_json_response(response.text)

        except Exception as e:
            error_message = str(e)

            print(f"[Gemini Error] Attempt {attempt}/{max_retries}: {error_message}")

            # 503, timeout veya geçici servis hatalarında kısa bekleyip tekrar deniyoruz.
            if attempt < max_retries:
                time.sleep(2 * attempt)
                continue

            # Son deneme de başarısızsa fallback plan döndürüyoruz.
            print("[Gemini Fallback] Gemini unavailable. Using fallback learning plan.")

            return generate_fallback_learning_plan(
                topic=topic,
                level=level,
                goal=goal,
                weekly_hours=weekly_hours,
                duration_weeks=duration_weeks,
                learning_preference=learning_preference
            )






def generate_fallback_learning_plan(
    topic: str,
    level: str,
    goal: str,
    weekly_hours: int,
    duration_weeks: int,
    learning_preference: str | None = None
) -> Dict[str, Any]:
    """
    Gemini API çalışmadığında kullanılacak basit fallback plan üreticisi.

    Amaç:
    - Demo sırasında sistemin tamamen çökmesini engellemek
    - Kullanıcıya yine de kaydedilebilir ve görüntülenebilir bir plan sunmak
    - Gemini tekrar çalışana kadar MVP akışını korumak
    """

    weeks = []

    for week_number in range(1, duration_weeks + 1):
        weeks.append({
            "week_number": week_number,
            "title": f"{topic} - Hafta {week_number}",
            "description": (
                f"Bu hafta {topic} konusunda seviyene uygun temel çalışmalar yapacaksın."
            ),
            "estimated_hours": weekly_hours,
            "mini_project": (
                f"{topic} ile ilgili küçük ve uygulanabilir bir mini proje geliştir."
            ),
            "tasks": [
                {
                    "task_text": f"{topic} konusundaki temel kavramları öğren.",
                    "task_type": "Teori",
                    "estimated_minutes": 60,
                    "difficulty": "Kolay" if week_number == 1 else "Orta"
                },
                {
                    "task_text": f"{topic} ile ilgili başlangıç seviyesinde örnekleri incele.",
                    "task_type": "Araştırma",
                    "estimated_minutes": 45,
                    "difficulty": "Kolay"
                },
                {
                    "task_text": f"{topic} konusunda basit bir uygulama yap.",
                    "task_type": "Uygulama",
                    "estimated_minutes": 90,
                    "difficulty": "Orta"
                },
                {
                    "task_text": f"Bu hafta öğrendiğin {topic} konularını kısa notlar halinde tekrar et.",
                    "task_type": "Tekrar",
                    "estimated_minutes": 45,
                    "difficulty": "Kolay"
                }
            ],
            "resources": [
                {
                    "resource_title": f"{topic} resmi dokümantasyonu",
                    "resource_type": "Dokümantasyon",
                    "resource_description": (
                        f"{topic} konusunu temel kaynaktan öğrenmek için kullanılabilir."
                    ),
                    "resource_url": None
                },
                {
                    "resource_title": f"{topic} başlangıç seviyesi eğitim içeriği",
                    "resource_type": "Video / Kurs",
                    "resource_description": (
                        f"{topic} konusuna giriş yapmak için başlangıç seviyesinde kaynak araştır."
                    ),
                    "resource_url": None
                }
            ]
        })

    return {
        "topic": topic,
        "level": level,
        "goal": goal,
        "weekly_hours": weekly_hours,
        "duration_weeks": duration_weeks,
        "learning_preference": learning_preference or "Belirtilmedi",
        "summary": (
            f"Bu fallback plan, {topic} konusunu {level} seviyesindeki kullanıcı için "
            f"haftalık görevler ve mini projelerle öğrenilebilir hale getirmek amacıyla oluşturulmuştur."
        ),
        "final_outcome": (
            f"Plan sonunda kullanıcı {topic} konusunda temel kavramları anlayabilecek, "
            f"basit uygulamalar geliştirebilecek ve kendi öğrenme sürecini sürdürebilecek seviyeye gelecektir."
        ),
        "weeks": weeks
    }


def build_weekly_quiz_prompt(
    topic: str,
    level: str,
    goal: str,
    week_title: str,
    week_description: str | None,
    tasks: list[str],
    mini_project: str | None,
    question_count: int = 5
) -> str:
    """
    Builds the prompt for generating a weekly quiz.

    Prompt structure:
    1. Context
    2. Role
    3. Constraints
    4. Task
    5. Template variables
    6. Output control

    The prompt is written in English, but the quiz content must be in Turkish.
    """

    tasks_text = "\n".join([f"- {task}" for task in tasks])

    return f"""
# 1. Context

You are generating a weekly assessment quiz for an AI-powered personalized learning platform.

The user has a learning plan divided into weekly sections. Each week contains a title, description, tasks, resources, and a mini project. The quiz should evaluate whether the user understood the main concepts and practical goals of the selected week.

The generated quiz will be displayed in the application UI. Therefore, the output must be structured, clear, and easy to parse.

# 2. Role

Act as an expert educational assessment designer and technical interviewer.

You should create beginner-friendly, fair, practical, and concept-focused multiple-choice questions.

# 3. Constraints

- Return only valid JSON.
- Do not use Markdown.
- Do not add explanations outside the JSON.
- The JSON must be parseable by Python's json.loads().
- All quiz content must be written in Turkish.
- Generate exactly {question_count} questions.
- Each question must have exactly 4 options.
- The correct_answer must exactly match one of the options.
- Each explanation must briefly explain why the answer is correct.
- Questions must be based only on the selected week content.
- Avoid overly generic questions.
- Avoid trick questions.
- Avoid duplicate questions.
- The quiz must be suitable for the user's current level: "{level}".
- The quiz should include both conceptual and practical understanding.
- Do not include answer labels such as "A)", "B)", "C)", "D)" in the options.

# 4. Task

Generate a weekly multiple-choice quiz for the selected learning week.

The quiz should help the user check their understanding of the week's topic, tasks, and mini project.

# 5. Template Variables

User and plan information:

- topic: "{topic}"
- current_level: "{level}"
- learning_goal: "{goal}"
- week_title: "{week_title}"
- week_description: "{week_description or "No description provided"}"
- mini_project: "{mini_project or "No mini project provided"}"

Week tasks:

{tasks_text}

# 6. Output Control

Return the output using exactly this JSON structure:

{{
  "quiz_title": "{week_title} Quiz",
  "questions": [
    {{
      "question": "Soru metni",
      "options": [
        "Seçenek 1",
        "Seçenek 2",
        "Seçenek 3",
        "Seçenek 4"
      ],
      "correct_answer": "Doğru seçenek",
      "explanation": "Doğru cevabın kısa açıklaması"
    }}
  ]
}}
"""


def generate_weekly_quiz_with_gemini(
    topic: str,
    level: str,
    goal: str,
    week_title: str,
    week_description: str | None,
    tasks: list[str],
    mini_project: str | None,
    question_count: int = 5
) -> Dict[str, Any]:
    """
    Gemini API ile seçili hafta için quiz üretir.

    Gemini geçici olarak hata verirse local fallback quiz üretir.
    """

    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY bulunamadı. Lütfen backend/.env dosyasına GEMINI_API_KEY ekle."
        )

    prompt = build_weekly_quiz_prompt(
        topic=topic,
        level=level,
        goal=goal,
        week_title=week_title,
        week_description=week_description,
        tasks=tasks,
        mini_project=mini_project,
        question_count=question_count
    )

    max_retries = 3

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3
                )
            )

            return parse_gemini_json_response(response.text)

        except Exception as e:
            error_message = str(e)
            print(f"[Gemini Quiz Error] Attempt {attempt}/{max_retries}: {error_message}")

            if attempt < max_retries:
                time.sleep(2 * attempt)
                continue

            print("[Gemini Quiz Fallback] Gemini unavailable. Using fallback quiz.")

            return generate_fallback_weekly_quiz(
                topic=topic,
                week_title=week_title,
                question_count=question_count
            )


def generate_fallback_weekly_quiz(
    topic: str,
    week_title: str,
    question_count: int = 5
) -> Dict[str, Any]:
    """
    Gemini çalışmadığında kullanılacak basit fallback quiz üreticisi.
    """

    questions = []

    fallback_templates = [
        {
            "question": f"{topic} öğrenirken ilk olarak neye dikkat edilmelidir?",
            "options": [
                "Temel kavramları anlamaya",
                "Sadece ezber yapmaya",
                "Hiç uygulama yapmamaya",
                "Kaynakları tamamen atlamaya"
            ],
            "correct_answer": "Temel kavramları anlamaya",
            "explanation": "Yeni bir konuyu öğrenirken temel kavramları anlamak sağlam bir başlangıç sağlar."
        },
        {
            "question": f"{week_title} kapsamında pratik yapmak neden önemlidir?",
            "options": [
                "Bilgiyi uygulamaya dönüştürmek için",
                "Konuyu daha karmaşık hale getirmek için",
                "Kaynak kullanmamak için",
                "Öğrenmeyi tamamen ezbere dayandırmak için"
            ],
            "correct_answer": "Bilgiyi uygulamaya dönüştürmek için",
            "explanation": "Pratik yapmak, öğrenilen teorik bilgilerin gerçek örneklerle pekişmesini sağlar."
        },
        {
            "question": "Mini proje yapmanın öğrenme sürecindeki temel faydası nedir?",
            "options": [
                "Öğrenilen bilgileri somut bir çıktıya dönüştürmek",
                "Görevleri tamamen atlamak",
                "Sadece kaynak listesini çoğaltmak",
                "Hiç tekrar yapmamak"
            ],
            "correct_answer": "Öğrenilen bilgileri somut bir çıktıya dönüştürmek",
            "explanation": "Mini projeler, öğrenilen konuların uygulanabilir hale gelmesini sağlar."
        },
        {
            "question": "Bir öğrenme planında görevlerin tamamlanma durumunu takip etmek ne işe yarar?",
            "options": [
                "İlerlemeyi ölçmeye yardımcı olur",
                "Planı gereksiz hale getirir",
                "Öğrenme hedefini siler",
                "Kaynakları kullanmayı engeller"
            ],
            "correct_answer": "İlerlemeyi ölçmeye yardımcı olur",
            "explanation": "Görev takibi, kullanıcının ne kadar ilerlediğini görmesini sağlar."
        },
        {
            "question": f"{topic} konusunda düzenli tekrar yapmanın amacı nedir?",
            "options": [
                "Bilgiyi kalıcı hale getirmek",
                "Konuyu unutmayı hızlandırmak",
                "Uygulamaları tamamen bırakmak",
                "Öğrenme süresini anlamsız hale getirmek"
            ],
            "correct_answer": "Bilgiyi kalıcı hale getirmek",
            "explanation": "Düzenli tekrar, öğrenilen bilgilerin daha uzun süre hatırlanmasına yardımcı olur."
        }
    ]

    for index in range(question_count):
        questions.append(fallback_templates[index % len(fallback_templates)])

    return {
        "quiz_title": f"{week_title} Quiz",
        "questions": questions
    }
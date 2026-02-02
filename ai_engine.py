import google.generativeai as genai

# إعداد المفتاح
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-pro')

async def get_ai_response(text):
    try:
        response = model.generate_content(text)
        return response.text
    except Exception as e:
        return "⚠️ عذراً سيدي، واجه المحرك الذكي خطأ تقني."

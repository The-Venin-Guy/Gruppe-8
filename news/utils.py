import requests
from django.conf import settings
from groq import Groq

def fetch_financial_news():
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'stocks OR investment OR market OR inflation OR Fed OR earnings OR crypto OR bonds OR portfolio',
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 10,
        'apiKey': settings.NEWS_API_KEY,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        articles = data.get('articles', [])
        return [
            {
                'title': a.get('title', ''),
                'description': a.get('description', '') or '',
                'url': a.get('url', ''),
                'source': a.get('source', {}).get('name', ''),
                'publishedAt': a.get('publishedAt', ''),
            }
            for a in articles if a.get('title')
        ]
    except:
        return []


def get_ai_recommendations(articles):
    if not articles:
        return "No news available for analysis."

    client = Groq(api_key=settings.GROQ_API_KEY)

    top5 = articles[:5]
    content_block = "\n\n".join([
        f"Title: {a['title']}\nSummary: {a['description']}"
        for a in top5
    ])

    prompt = f"""You are a professional financial analyst. Based on the following 5 financial news articles, give a clear investment recommendation summary.

{content_block}

Your response must include:
1. Overall Market Sentiment: (Bullish / Bearish / Neutral) with one sentence explanation
2. Top Signals:
   - [BUY / HOLD / WATCH] specific asset or sector + one line reasoning
   - [BUY / HOLD / WATCH] specific asset or sector + one line reasoning
   - [BUY / HOLD / WATCH] specific asset or sector + one line reasoning
3. Key Risk: one sentence on the biggest risk to watch today

Keep the entire response under 200 words. Be direct and specific."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"
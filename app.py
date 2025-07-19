from flask import Flask, request, render_template
import time
from collections import deque

app = Flask(__name__)

# In-memory storage (replace with DB for production)
ai_visits = deque(maxlen=1000)
human_visits = deque(maxlen=1000)

# Known AI User-Agents
KNOWN_AI_BOTS = [
    'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'GrokBot', 'ai-crawler'
]

def is_ai_crawler(user_agent):
    return any(bot.lower() in user_agent.lower() for bot in KNOWN_AI_BOTS)

@app.before_request
def track_visit():
    user_agent = request.headers.get('User-Agent', '')
    referrer = request.referrer or 'None'
    url = request.url
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    visit_data = {
        'timestamp': timestamp,
        'ip': request.remote_addr,
        'user_agent': user_agent,
        'referrer': referrer,
        'url': url
    }

    if is_ai_crawler(user_agent):
        ai_visits.appendleft(visit_data)
    else:
        human_visits.appendleft(visit_data)

@app.route('/')
def index():
    return render_template('index.html',
                           human_count=len(human_visits),
                           ai_count=len(ai_visits),
                           human_visits=list(human_visits)[:10],
                           ai_visits=list(ai_visits)[:10])

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, redirect, url_for, session, request, render_template_string
from authlib.integrations.flask_client import OAuth
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Change this to a fixed secret key in production

# OAuth Configuration
oauth = OAuth(app)

# Google OAuth Setup
# Google OAuth Setup
# google = oauth.register(
#     name='google',
#     client_id='373926153415-qqergqk9lpp8pgrbg64epjlu82h7sd87.apps.googleusercontent.com',
#     client_secret='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',
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={'scope': 'openid email profile'}
# )

# GitHub OAuth Setup
# GitHub OAuth Setup
# github = oauth.register(
#     name='github',
#     client_id='Ov23liT4wmhWAr5yflUT',
#     client_secret='e744821547921415b75f8fddaff74889a35b915e',
#     access_token_url='https://github.com/login/oauth/access_token',
#     authorize_url='https://github.com/login/oauth/authorize',
#     api_base_url='https://api.github.com/',
#     client_kwargs={'scope': 'user repo'}
# )

# HTML Templates
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>GitHub Repository Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .login-box { text-align: center; padding: 40px; border: 1px solid #ddd; border-radius: 8px; }
        button { padding: 12px 24px; font-size: 16px; cursor: pointer; background: #4285f4; color: white; border: none; border-radius: 4px; }
        button:hover { background: #357ae8; }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>GitHub Repository Viewer</h1>
        <p>Login with your Gmail account to view GitHub repositories</p>
        <a href="{{ url_for('google_login') }}">
            <button>Login with Google</button>
        </a>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1000px; margin: 20px auto; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .user-info { display: flex; align-items: center; gap: 15px; }
        .logout { padding: 8px 16px; background: #dc3545; color: white; text-decoration: none; border-radius: 4px; }
        .connect-btn { padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .repo-list { list-style: none; padding: 0; }
        .repo-item { padding: 15px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
        .repo-name { font-size: 18px; font-weight: bold; color: #0366d6; }
        .repo-desc { color: #586069; margin: 5px 0; }
        .repo-stats { color: #586069; font-size: 14px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="user-info">
            <h2>Welcome, {{ user.email }}</h2>
        </div>
        <a href="{{ url_for('logout') }}" class="logout">Logout</a>
    </div>
    
    {% if not github_connected %}
    <div style="text-align: center; padding: 30px;">
        <p>Connect your GitHub account to view repositories</p>
        <a href="{{ url_for('github_login') }}">
            <button class="connect-btn">Connect GitHub Account</button>
        </a>
    </div>
    {% else %}
    <h3>Your GitHub Repositories ({{ github_user }})</h3>
    <ul class="repo-list">
        {% for repo in repositories %}
        <li class="repo-item">
            <div class="repo-name">
                <a href="{{ repo.html_url }}" target="_blank">{{ repo.name }}</a>
            </div>
            {% if repo.description %}
            <div class="repo-desc">{{ repo.description }}</div>
            {% endif %}
            <div class="repo-stats">
                ⭐ {{ repo.stargazers_count }} | 🍴 {{ repo.forks_count }} | 
                {% if repo.language %}{{ repo.language }}{% endif %}
            </div>
        </li>
        {% endfor %}
    </ul>
    {% endif %}
</body>
</html>
'''

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(HOME_TEMPLATE)

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_callback', _external=True, _scheme='http')
    return google.authorize_redirect(redirect_uri)

@app.route('/callback/google')
def google_callback():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    session['user'] = {
        'email': user_info['email'],
        'name': user_info.get('name', '')
    }
    return redirect(url_for('dashboard'))

@app.route('/login/github')
def github_login():
    redirect_uri = url_for('github_callback', _external=True, _scheme='http')
    return github.authorize_redirect(redirect_uri)

@app.route('/callback/github')
def github_callback():
    token = github.authorize_access_token()
    session['github_token'] = token['access_token']
    
    # Get GitHub user info
    headers = {'Authorization': f"token {token['access_token']}"}
    user_resp = requests.get('https://api.github.com/user', headers=headers)
    session['github_user'] = user_resp.json()['login']
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    repositories = []
    github_connected = False
    github_user = None
    
    if 'github_token' in session:
        github_connected = True
        github_user = session.get('github_user')
        headers = {'Authorization': f"token {session['github_token']}"}
        
        # Fetch user's repositories
        repos_resp = requests.get('https://api.github.com/user/repos', 
                                 headers=headers,
                                 params={'per_page': 100, 'sort': 'updated'})
        repositories = repos_resp.json()
    
    return render_template_string(DASHBOARD_TEMPLATE, 
                                 user=session['user'],
                                 repositories=repositories,
                                 github_connected=github_connected,
                                 github_user=github_user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

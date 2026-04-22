@echo off
cd /d G:\dumatework\kotti_ai_community
G:\dumatework\.venv\Scripts\python.exe -c "from pyramid.paster import get_app; from waitress import serve; app = get_app('development.ini', 'main'); serve(app, host='0.0.0.0', port=6542)"

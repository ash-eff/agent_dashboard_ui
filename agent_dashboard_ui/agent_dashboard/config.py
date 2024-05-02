import os
import shutil
from pathlib import Path

home_dir = str(Path.home())
app_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(home_dir, 'AgentDashboard', 'data')
style_dir = os.path.join(home_dir, 'AgentDashboard', 'styles')

os.makedirs(data_dir, exist_ok=True)
os.makedirs(style_dir, exist_ok=True)

app_dark_mode_path = os.path.join(app_dir, 'styles', 'dark_mode.css')
app_light_mode_path = os.path.join(app_dir, 'styles', 'light_mode.css')

dark_mode_path = os.path.join(style_dir, 'dark_mode.css')
light_mode_path = os.path.join(style_dir, 'light_mode.css')

app_domains_path = os.path.join(app_dir, 'data', 'domains.json')
app_email_templates_path = os.path.join(app_dir, 'data', 'email_templates.json')

domains_path = os.path.join(data_dir, 'domains.json')
email_templates_path = os.path.join(data_dir, 'email_templates.json')


if not os.path.exists(dark_mode_path):
    shutil.copy(app_dark_mode_path, dark_mode_path)

if not os.path.exists(light_mode_path):
    shutil.copy(app_light_mode_path, light_mode_path)

if not os.path.exists(domains_path):
    shutil.copy(app_domains_path, domains_path)

if not os.path.exists(email_templates_path):
    shutil.copy(app_email_templates_path, email_templates_path)
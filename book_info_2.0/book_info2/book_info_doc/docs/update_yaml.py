import requests
import os
import re
from pathlib import Path
import subprocess

# 1. Получаем адрес из ngrok API
def get_ngrok_url():
    try:
        r = requests.get("http://127.0.0.1:4040/api/tunnels")
        r.raise_for_status()
        tunnels = r.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except Exception as e:
        print("Ошибка получения ngrok адреса:", e)
        return None

# 2. Обновляем YAML-файлы
def update_yaml_files(folder_path, new_host):
    yaml_files = list(Path(folder_path).rglob("*.yaml"))
    for file in yaml_files:
        text = file.read_text(encoding='utf-8')
        text = re.sub(r"host:\s.*", f"host: {new_host.replace('https://', '')}", text)
        text = re.sub(r"schemes:\s*\n\s*-\s*\w+", "schemes:\n  - https", text)
        file.write_text(text, encoding='utf-8')
        print(f"Обновлен файл: {file}")

# 3. Git commit и push
def git_commit_and_push():
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "🔄 Автообновление host ngrok"], check=True)
    subprocess.run(["git", "push"], check=True)

# MAIN
if __name__ == "__main__":
    host = get_ngrok_url()
    if not host:
        print("❌ Не удалось получить URL от ngrok.")
        exit(1)

    print(f"🌐 Новый ngrok адрес: {host}")
    update_yaml_files("docs/swagger", host)  # Путь к YAML-файлам
    git_commit_and_push()
    print("✅ Файлы обновлены и загружены на GitHub.")

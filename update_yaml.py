import os
import re
import subprocess
import requests

# Список YAML-файлов, в которых нужно обновлять host
FILES_TO_UPDATE = [
    "../docs/swagger-ui/swagger.yaml",
    "../docs/swagger-ui/swagger_book_by_id.yaml",
    # Добавь сюда другие пути по мере необходимости
]

# Регулярное выражение для поиска строки host:
HOST_REGEX = re.compile(r"(host:\s*)([^\n]+)")

# Получение текущего ngrok-адреса
def get_ngrok_url():
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"].replace("https://", "")
        return None
    except Exception as e:
        print(f"Ошибка при получении ngrok-адреса: {e}")
        return None

# Обновление файлов с новым адресом
def update_files(new_host):
    changed_files = []
    for rel_path in FILES_TO_UPDATE:
        file_path = os.path.abspath(rel_path)
        if not os.path.exists(file_path):
            print(f"Файл не найден: {rel_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        updated_content, count = HOST_REGEX.subn(lambda m: f"{m.group(1)}{new_host}", content)
        if count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            changed_files.append(file_path)

    return changed_files

# Git-коммит и пуш
def git_commit_and_push(files, host):
    try:
        subprocess.run(["git", "add"] + files, check=True)
        subprocess.run(["git", "commit", "-m", f"Обновление host ngrok -> {host}"], check=True)
        subprocess.run(["git", "push"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

#  Деплой документации на GitHub Pages
def deploy_mkdocs():
    print("Деплой документации на GitHub Pages...")
    try:
        subprocess.run(["mkdocs", "gh-deploy", "-f", "../mkdocs.yaml"], check=True)
        print("Документация задеплоена успешно.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при деплое: {e}")

if __name__ == "__main__":
    new_host = get_ngrok_url()
    if not new_host:
        print("Не удалось получить URL от ngrok.")
        exit(1)

    print(f"Новый ngrok адрес: {new_host}")
    changed = update_files(new_host)

if changed:
    print("Изменены YAML-файлы:")
    for f in changed:
        print(f"- {f}")
    git_commit_and_push(changed, new_host)
    print("Изменения закоммичены и отправлены в GitHub.")
    deploy_mkdocs()
else:
    print("Нет изменений в YAML-файлах.")




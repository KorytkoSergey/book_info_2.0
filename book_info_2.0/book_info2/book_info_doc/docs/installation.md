### Установка и разворачивание приложения
## Описание
*Стек* Python
*Библиотеки* Flask
*API* RESTfull
*Тип сообщений* JSON, xml

## Репозиторий
Github https://github.com/KorytkoSergey/book_info_2.0

## Команды для работы со средой в Python
1. Развернуть среду и установить Python.
2. Создать виртуальное окружение
   ```python3 -m venv my_env```  
4. Активировать виртуальное окружение ```source my_env/bin/activate```
5. Устанавливаем библиотеку для наката зависимостей ```pip install requests``` 
6. Накатываем зависимости из файла ```pip install -r requirements.txt```
7. Диактивировать виртуальное окружение ```deactivate```

# **Полезное по работе с виртуальным окружением:**

- **Обновить пакеты, если уже установлены:**
    
    ```
    pip install --upgrade -r requirements.txt
    ```
    
- **Проверить установленные зависимости:**
    
    ```
    pip list
    ```
    
- **Создать `requirements.txt` из текущего окружения:**
    
    ```
    pip freeze > requirements.txt
    ```


<iframe
  src="swagger-ui/index.html"
  style="width: 100%; height: 700px; border: none;"
></iframe>
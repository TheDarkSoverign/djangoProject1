# Используем базовый образ Python
FROM python:3.12

RUN apt-get update && \
    apt-get install -y mongodb-clients

RUN pip install --upgrade pip

# Устанавливаем рабочую директорию внутри контейнера


# Копируем зависимости и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем все файлы в контейнер
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

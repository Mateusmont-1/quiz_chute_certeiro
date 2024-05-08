# Use a imagem oficial do Python como base
FROM python:3.8

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos do aplicativo para o diretório de trabalho
COPY . /app

# Instale as dependências do aplicativo
RUN pip install -r requirements.txt

# Defina o ponto de entrada para o contêiner
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
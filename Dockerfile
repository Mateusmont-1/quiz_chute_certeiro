# Use a imagem oficial do Python
FROM python:3.9-slim

# Define o fuso horário para São Paulo
ENV TZ=America/Sao_Paulo

# Instale as dependências do sistema operacional necessárias para definir o fuso horário
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o conteúdo do diretório atual (onde está o Dockerfile) para o diretório de trabalho no contêiner,
# exceto a pasta venv
COPY quiz-with-interface.py /app/
COPY assets /app/assets/
COPY requirements.txt /app/

# Instale as dependências Python
RUN pip install -r requirements.txt

# Exponha a porta 8080
EXPOSE 8080

# Comando para iniciar sua aplicação
CMD ["python", "quiz-with-interface.py"]


# Não esquecer de criar a network antes de ativar os docker
# docker network create my_network
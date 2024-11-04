# Use a imagem oficial do Python como base
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de requerimentos (caso tenha) para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o conteúdo do projeto para o diretório de trabalho
COPY . .

# Exponha a porta em que o Flask vai rodar
EXPOSE 3000

# Comando para rodar a aplicação
CMD ["python", "app.py"]

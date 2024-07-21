# Usa la imagen base de Python 3.10 slim
FROM python:3.10-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir es_core_news_md-3.7.0-py3-none-any.whl

# Instala Rasa
RUN pip install rasa

# Expone el puerto en el que la aplicación Flask/Rasa estará escuchando
EXPOSE 5005

# Comando para ejecutar el servidor de Rasa
CMD ["rasa", "run", "-m", "results/20240629-194611-violet-depth", "--enable-api", "--cors", "*"]

#Imagen que incluye todas las dependencias necesarias
FROM python:latest
COPY . /game-p6
#Directorio desde el que trabajaremos(Donde esta la imagen)
WORKDIR /game-p6/

EXPOSE 9999/udp
#Ejecucion del comando
CMD ["python3","-u", "game_server.py" ]


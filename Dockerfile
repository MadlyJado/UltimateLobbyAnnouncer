FROM python

WORKDIR /home/pi/UltimateLobbyAnnouncer

COPY . .

RUN pip install discord

CMD ["python", "ultimatelobbyannouncer.py"]

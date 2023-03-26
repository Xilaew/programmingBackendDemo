from python

WORKDIR /app

COPY . .
RUN ["pip","install","-r","requirements.txt"]

EXPOSE 8080
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
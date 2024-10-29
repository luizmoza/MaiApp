FROM python:3
WORKDIR /app
ARG PORT_BUILD = 5000
ENV PORT = $PORT_BUILD
EXPOSE $PORT_BUILD
COPY . .
RUN pip install --upgrade pip
RUN pip install gevent
RUN pip install pandas
RUN pip install pyodbc
RUN pip install Flask
RUN pip install sqlalchemy
RUN pip install mysql-connector-python
CMD ["python","run.py"]
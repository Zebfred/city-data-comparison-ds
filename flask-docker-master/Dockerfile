FROM zebfred/flask-docker:latest
MAINTAINER Jimmy Zeb Smith "zebfred22@gmail.com"
RUN apt update && apt install python-dev -y
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV ACCESS_KEY=jkekal6d6e5si3i2ld66d4dl
ENV MONGO_URI=mongodb+srv://steve122192:P1kdLg4ODBDrFUH7@steves-cluster-blrmh.mongodb.net/citydata?retryWrites=true&w=majority
ENV SQLALCHEMY_DATABASE_URI=postgresql://postgres:lkjhgfdsa@dsapi.co7exmpaol7l.us-east-2.rds.amazonaws.com/dscitydata
EXPOSE 5000


ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-"]
CMD ["app:app"]

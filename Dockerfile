FROM python:3.7.5-slim

# Installing packages
#RUN apt update
RUN pip3 install --no-cache numpy boto3 botocore pandas joblib flask DEAP seaborn matplotlib

# Defining working directory and adding source code
WORKDIR /usr/src/app/


ENV PYTHONPATH /DEAP


# in case that you want to store some in here...
# but it'd better store files in /tmp/

RUN mkdir -p /usr/src/app/tmp_files
RUN chmod 755 /usr/src/app/tmp_files


COPY bootstrap.sh ./
COPY DEAP ./DEAP

COPY data_csv ./data_csv
COPY data_image ./data_image
COPY data_log ./data_log

RUN chmod 755 /usr/src/app/bootstrap.sh
RUN chmod +x /usr/src/app/bootstrap.sh

# Start app
EXPOSE 54321
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]

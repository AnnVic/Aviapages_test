#base image
FROM python:3.9-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create root directory for our project in the container
RUN mkdir /app

# Set the working directory 
WORKDIR /app

#copy the app code to image working directory
COPY . .

#port where the app runs
EXPOSE 8000

#start server
CMD python manage.py runserver
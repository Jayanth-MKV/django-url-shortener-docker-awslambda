![Django](https://img.shields.io/static/v1?label=Django&message=5.0.7&color=092E20&labelColor=white&logo=django&logoColor=092E20)
![PIP](https://img.shields.io/static/v1?label=PIP&message=24&color=yellow&labelColor=3775A9&logo=pypi&logoColor=white)
![Python](https://img.shields.io/static/v1?label=Python&message=3.12.3&color=yellow&labelColor=3775A9&logo=py&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

# Django URL Shortener (Enhanced)

## Table of Contents

- [🌟 Introduction](#introduction)
- [🛠 Added Functionality](#added-functionality)
- [⚙️ Installation](#installation)
- [🚀 Usage](#usage)
- [📦 Dependencies](#dependencies)
- [🔧 Configuration](#configuration)
- [🐳 Dockerization](#dockerization)
- [☁️ Deployment to AWS Lambda](#deployment-to-aws-lambda)
- [🔗 References](#references)
- [❗️ Troubleshooting](#troubleshooting)

<h2 id="introduction">🌟 Introduction</h2>

Django URL Shortener is a web application for shortening URLs. This project includes additional CRUD operations, search functionality, and is containerized using Docker for deployment to AWS Lambda.

<h2 id="added-functionality">🛠 Added Functionality</h2>

Initially cloned from 
```
https://github.com/mmedoo/django-url-shortener.git
```

- **CRUD Operations:** Added functionality to Create, Read, Update, and Delete shortened URLs (Like TODOIST).
- **Search Functionality:** Implemented a search feature to find URLs based on keywords.
- **Login Functionality**: Will be implemented if time permits

<h2 id="installation">⚙️ Installation</h2>

To get the project up and running locally on the machine, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone <url>
    cd django-url-shortener
    ```

2. **Set up a virtual environment:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```
    ```sh
    # windows
    .\venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations:**
    ```sh
    python manage.py makemigrations url_shortener
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Start the development server:**
    ```sh
    python manage.py runserver
    ```

<h2 id="usage">🚀 Usage</h2>

### Shorten a URL
1. Navigate to the home page.
2. Enter the URL you want to shorten in the provided form.
3. Click the "Shorten URL" button.
4. The shortened URL will be displayed on the screen.

### Retrieve a URL
1. Enter the shortened key in the URL path (e.g., `http://localhost:8000/<shortened-key>`).
2. You will be redirected to the original URL.

### Manage URLs
1. Use the provided CRUD interfaces to manage the shortened URLs.
2. Use the search functionality to find specific URLs.

<h2 id="dependencies">📦 Dependencies</h2>

- Django==5.0.7
- psycopg2-binary
- python-dotenv
- zappa

<h2 id="configuration">🔧 Configuration</h2>

### Database
By default, this project uses PostgreSQL hosted on AWS RDS. We can configure the database by updating the `DATABASES` setting in `settings.py`.

### .env setup
To run the application the database need to be setup, which is hosted on AWS RDS. We can configure the database by updating these.
```sh
RDS_USERNAME = ''
RDS_PASSWORD = ''
RDS_HOSTNAME = ''
RDS_DB_NAME = ''
```

If you want to use the default sqlite database:
In app.settings.py - change this
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

<h2 id="dockerization">🐳 Dockerization</h2>

The application has been Dockerized to ensure consistent deployment and execution across different environments.

### Dockerfile
```dockerfile
FROM python:3.11.9-slim AS stage-1
COPY . /django_lambda/
WORKDIR /django_lambda
RUN pip install pipenv
RUN pipenv install -r requirements.txt
RUN pipenv run zappa package -o /django_zappa.zip

FROM python:3.11.9-slim
COPY --from=stage-1 django_zappa.zip /django_zappa.zip
RUN apt-get update && apt-get install -y unzip
RUN pip install awslambdaric boto3
RUN unzip /django_zappa.zip -d /app/
WORKDIR /app

# IMPORTANT TO SET THIS
ENV PYTHONPATH "${PYTHONPATH}:/app"
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
ENTRYPOINT [ "/entry.sh" ]
CMD ["handler.lambda_handler"]
```

Here for a django application to run on a serverless machine ( here AWS Lambda ) it needs to be configured accordingly so that be hosted. Thi spart is done by an opensource tool called zappa. zappa needds to be configured inside a virtual env hence pyenv is used . Instead of using zappa locally, here we did it inside the docker image.


The image building happens in two stages. First, the zappa package for the django application is created, this will be a zip file. Then create our final image for hosting this container on AWS lambda. Note that the first stage is used for building the zappa package and is not part of the final image.

Now, as we have the final image - for hosting it it need to be compatible with the AWS Lambda run time. Thus we use [awslambdaric](https://github.com/aws/aws-lambda-python-runtime-interface-client) to implement the Lambda Runtime API, allowing to seamlessly extend our final image to be Lambda compatible.

To make it easy to locally test Lambda functions packaged as container images we use  AWS Lambda Runtime Interface Emulator [aws-lambda-rie](https://github.com/aws/aws-lambda-python-runtime-interface-client?tab=readme-ov-file#local-testing).

Run this final image locally and test
```
docker build -f Dockerfile.aws -t urlapp .
docker run -p 8000:8080 --name app urlapp
```

The way we test a Django web server differs from how we would test a Lambda function. The command to test our function invocation is as follows:
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"path": "/", "httpMethod": "GET", "requestContext": {}, "body": null}'
```

<h2 id="deployment-to-aws-lambda">☁️ Deployment to AWS Lambda</h2>

The application is deployed to AWS Lambda using Zappa, which converts the Django app to a serverless architecture.

### Building and Running Docker Image For Hosting
1. Build the Docker image:
    ```sh
    docker build -f Dockerfile.aws -t urlapp .
    ```

2. Tag the Docker image:
    ```sh
    docker tag urlapp:latest 339713069346.dkr.ecr.ap-southeast-2.amazonaws.com/urlapp:latest
    ```

3. Push the Docker image to ECR:
    ```sh
    docker push 339713069346.dkr.ecr.ap-southeast-2.amazonaws.com/urlapp:latest
    ```
4. Deploy the Application:
    ```sh
    zappa deploy dev -d 339713069346.dkr.ecr.ap-southeast-2.amazonaws.com/urlapp:latest
    ```
Zappa takes care of the AWS Gateway here. 

### SOME COMMANDS FOR REFERENCE

1. **Install Zappa:**
    ```sh
    pip install zappa
    ```

2. **Initialize Zappa:**
    ```sh
    zappa init
    ```

3. **Deploy the Application:**
    ```sh
    zappa deploy dev -d 339713069346.dkr.ecr.ap-southeast-2.amazonaws.com/urlapp:latest
    ```

4. **Update the Application:**
    ```sh
    zappa update dev -d 339713069346.dkr.ecr.ap-southeast-2.amazonaws.com/urlapp:latest
    ```

### Configuration and Deployment Details
- **Dockerize Application:** Containerized the Django application using a multi-stage Dockerfile.
- **Zappa:** Used Zappa to package and deploy the application to AWS Lambda.

<h2 id="references">🔗 References</h2>

- [Ian Whitestone's guide on Zappa and Docker](https://ianwhitestone.work/zappa-serverless-docker/)
- [Mark Gituma's guide on deploying Django Docker images to AWS Lambda](https://markgituma.medium.com/deploying-django-docker-images-to-aws-lambda-container-5b3d9faf6982)
- [AWS Lambda Python Image Instructions](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions)
- [YCombinator discussion on AWS Lambda and Docker](https://news.ycombinator.com/item?id=31183109)
- [Zappa GitHub repository](https://github.com/zappa/Zappa)

<h2 id="troubleshooting">❗️ Troubleshooting</h2>

### Common Issues
- **Server not starting:** Ensure all dependencies are installed and the database migrations have been applied.
- **Invalid URL:** Make sure the URL entered is valid and follows the correct format.
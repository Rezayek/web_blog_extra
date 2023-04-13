FROM python:3.9.13 

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python ./app/main.py && \
    python ./app/services/user_auth_service/auth_micro.py && \
    python ./app/services/post_service/post_micro.py && \
    python ./app/services/comments_service/comments_micro.py
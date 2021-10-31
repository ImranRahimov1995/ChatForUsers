docker run --name some-redis --rm -p 6379:6379 -d redis

python3 manage.py runserver 0.0.0.0:8000

docker stop some-redis
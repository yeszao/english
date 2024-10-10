!/bin/bash

docker exec -it english-web python /workspace/src/crawl_news.py


docker run --rm --env-file /home/gary/docker_data/english/local.env english-web python /workspace/src/crawl_news.py
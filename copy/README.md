
##for not first time:
#inits:
docker network create my-app-network
#first 6379 and 27017 can be replaced, if consistence is preserved
docker run -d  --name my-redis   --network news-app-network  -p 6379:6379  redis:latest
docker run -d  --name my-mongo   --network news-app-network  -p 27017:27017 mongo

#init microsevices
#names fetch1 proc1 and front1 are of specific images that were made
#docker build -t fetch1 fetcher/
#docker build -t proc1 processor/
#docker build -t front1 frontend/

#run microservices:
docker run -it -d --network news-app-network   -e REDIS_HOST=my-redis   -e REDIS_PORT=6379  fetch1
docker run -d -it --network news-app-network   -e REDIS_HOST=my-redis   -e REDIS_PORT=6379  -e MONGO_HOST=my-mongo -e MONGO_PORT=27017 proc1
docker run -it  --network news-app-network -p 8080:8080  -e MONGO_HOST=my-mongo -e MONGO_PORT=27017 front1



##for restarting
docker rm -f $(docker ps -qa)
docker image rm -f $(docker image ls -q)

##for first time:
#inits:
docker network create my-app-network
#first 6379 and 27017 can be replaced, if consistence is preserved
docker run -d  --name my-redis   --network news-app-network  -p 6379:6379  redis:latest
docker run -d  --name my-mongo   --network news-app-network  -p 27017:27017 mongo

#init microservices
#names fetch1 proc1 and front1 are of specific images that were made
docker build -t fetch1 fetcher/
docker build -t proc1 processor/
docker build -t front1 frontend/

#run microservices:
docker run -it -d --network news-app-network   -e REDIS_HOST=my-redis   -e REDIS_PORT=6379  fetch1
docker run -d -it --network news-app-network   -e REDIS_HOST=my-redis   -e REDIS_PORT=6379  -e MONGO_HOST=my-mongo -e MONGO_PORT=27017 proc1
docker run -it  --network news-app-network -p 8080:8080  -e MONGO_HOST=my-mongo -e MONGO_PORT=27017 front1


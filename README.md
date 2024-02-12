# Fampay-Assignment

#### Update the config file Db creds 

Api-Key is being read from Mongo Collection - ApiKey to support multiple key
{"key" : ${api_token}}
 

#### Build the docker image with following command
```
docker build -t assignment:1 -f Dockerfile .
```
#### once build is complete run the image 
```
docker run  -p 8000:8000 --name assignment_1 localhost/assignment:1
```
#### Application will be up & running 8000 port
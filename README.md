# Lambda Architecture (Scalable Computing)

This project aims to implement a scalable architecture for live and batch processing of time series data.

## Setup instructions

### Docker Swarm

```
docker swarm init
```

Some images need to be built because they are not on Docker Hub or their scripts lack elementary configuration options. A local registry is required to make them available to all machines in the swarm.
```
docker run -d -p 5000:5000 --name localregistry registry
docker-compose build
docker-compose push
```
The `image` options in the docker file point to `localhost:5000`. If your swarm consists of just one host (e.g. just testing), this is fine. Otherwise, adjust the address in [docker-compose.yml](docker-compose.yml).

Finally, to deploy the services:
```
docker stack deploy -c docker-compose.yml lambda
```

## Checking status
It may take a while before all services are accepting connections.

To see the status of each service in the stack:
```
docker stack services lambda
```

To get the logs of a certain service (of any replica):
```
docker service logs --follow lambda_<NAME>
```
...in which `NAME` is the name of the service within the stack.


## Running the algorithm (batch)
Pyspark does not support cluster mode. This leaves only the option of using client mode and submitting the algorithm from a container. This container then operates as the driver. Moreover, this allows for usage of service hostnames within the algorithm to be run on Spark.

```
cd algorithm-py
docker build -t algorithm .
docker run --name algorithm --network=lambda_default --rm -e SPARK_APPLICATION_PYTHON_LOCATION=/app/main.py algorithm
```

## Running the algorithm (live/streaming)
```
cd algorithm-py
docker build -t algorithm .
docker run --name algorithm --network=lambda_default --rm -e SPARK_APPLICATION_PYTHON_LOCATION=/app/streaming.py algorithm
```


## Stopping all services
```
docker stack rm lambda
```

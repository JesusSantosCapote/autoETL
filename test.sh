docker run --name some-postgres --network test_network -h 172.20.0.2 -e POSTGRES_PASSWORD=postgres -d postgres
docker run -it --name some_app --network test_network --mount type=bind,source=$(pwd),destination=/home/app  -h 172.20.0.3 -d autoetl
docker run --network test_network -p7687:7687 -p7474:7474 -h 172.20.0.4 --name neo4j_data_catalog --env NEO4J_AUTH=neo4j/datacatalog --volume=$(pwd)/data_catalog/data:/data neo4j

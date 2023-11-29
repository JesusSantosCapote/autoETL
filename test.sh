docker run --name some-postgres --network my_net -h 172.20.0.2 -e POSTGRES_PASSWORD=postgres -d postgres
docker run -it --name some_app --network my_net --mount type=bind,source=$(pwd),destination=/home/app  -h 172.20.0.3 -d autoetl
docker run --name target --network my_net -h 172.20.0.4 -e POSTGRES_PASSWORD=postgres -d postgres
docker run --network my_net -p7687:7687 -p7474:7474 -h 172.20.0.5 --name neo4j_data_catalog --env NEO4J_AUTH=neo4j/datacatalog neo4j

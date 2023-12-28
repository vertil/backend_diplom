 # CLEAR ALL DOCKER NETWORKS
 docker network prune
 
# create POSTGREDB
    sudo docker run -p 5432:5432 -e POSTGRES_USER=userP -e POSTGRES_PASSWORD=mypass -e POSTGRES_DB=facedb -d postgres

# crete db file in container
     pg_dump --host "192.168.126.130" --port "5432" --username "userP"  "facedb" > testDB.sql

# copy db file from container
    sudo docker cp 91a99e6b742a:testDB.sql ./
 
docker exec openote_db psql -U openuser -d openote --password -p 5432 -h localhost -f /app/entries.sql
docker exec openote_s3 bash -c 'export MC_HOST_temp=http://$MINIO_ROOT_USER:$MINIO_ROOT_PASSWORD@localhost:9000;for f in $(ls /app/logos); do mc put /app/logos/$f temp/user-logos;done'
docker exec openote_s3 bash -c 'export MC_HOST_temp=http://$MINIO_ROOT_USER:$MINIO_ROOT_PASSWORD@localhost:9000;mc mb temp/user-logos'

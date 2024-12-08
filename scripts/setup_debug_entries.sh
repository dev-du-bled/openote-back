mkdir -p ../storage/logos/ && cp -a ../assets/logos/. ../storage/logos/

docker exec openote_db psql -U openuser -d openote --password -p 5432 -h localhost -f /app/entries.sql

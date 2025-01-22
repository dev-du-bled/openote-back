docker exec openote_db psql -U openuser -d openote --password -p 5432 -h localhost -f /app/entries.sql
docker exec openote_api cp -r /app/default/logos /app/storage/logos

PASSWORD=$(head /dev/random | sha256sum | grep -Po '\w+')
USER="universal"
DATABASE="universal"
echo "Create user $USER with password $PASSWORD" | tee .create_user.log
sudo -u postgres psql -c "CREATE ROLE $USER WITH LOGIN PASSWORD '$PASSWORD' CREATEDB CREATEROLE;"
sudo -u postgres psql -c "CREATE DATABASE $DATABASE OWNER $USER;"

cat app/core/database/schema.sql | sudo psql -U $USER
echo
sudo psql -U $USER -c "SELECT pg_size_pretty(pg_table_size(core.oid)) AS size_tables,
        pg_size_pretty(pg_indexes_size(core.oid)) AS size_index,
        pg_size_pretty(pg_total_relation_size(core.oid)) AS total_size,
        core.relname AS table
FROM pg_class core
    LEFT JOIN pg_namespace space
        ON core.relnamespace=space.oid
WHERE space.nspname='public' AND core.relkind='r'
ORDER BY pg_total_relation_size(core.oid) DESC
LIMIT 20;"

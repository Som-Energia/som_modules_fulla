#!/bin/bash
echo "v23.9.7"

. /erp/bin/activate

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

apt-get install -y locales locales-all

echo "Starting SSH service"
service ssh start

echo "Starting ERP server"

# Test if DB exist
while ! python -c "from psycopg2 import connect; connect(\"dbname='${OPENERP_DB_NAME}' host='${OPENERP_DB_HOST}' user='${OPENERP_DB_USER}' password='${OPENERP_DB_PASSWORD}'\")"; do
	echo "Waiting Timescale, retry in 10 seconds..."
	sleep 10
done

# Get repository name (without owner)
repo_name=som_modules_fulla

# Checkout repository to desired commit
cd /src/$repo_name

# Update available modules
(cd /src/erp/; ./tools/link_addons.sh;)

# Install desired module
echo "Building DB from target module"
destral -m som_modules_fulla

exec /src/erp/server/bin/openerp-server.py -d destral_db --no-netrpc --config=/root/somenergia.conf

while true; do
	echo "Sleeping indefinitely..."
	sleep 86400 # Sleep for 24 hours (86400 seconds) before looping
done


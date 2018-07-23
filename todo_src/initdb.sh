#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
echo "${SCRIPT_DIR}" "hello"

DB_NAME=${DB_NAME:=todo}
DB_USER_NAME=${DB_USER_NAME:="${USER}"}
DB_USER_PASS=${DB_USER_PASS:="1${DB_USER_NAME}2"}
PSQL_ADMIN="sudo -i -u postgres psql"

if [ "$(${PSQL_ADMIN} -c 'select rolname from pg_roles;' | grep -w ${DB_USER_NAME})" == "" ];
then
  echo "create user '${DB_USER_NAME}'..."
  sudo -i -u postgres createuser ${DB_USER_NAME}
  sudo -i -u postgres psql -c \
    "alter user ${DB_USER_NAME} with encrypted pass${DB_USER_PASS}';"
fi

if [ "$(${PSQL_ADMIN} -c 'select datname from pg_database;' | grep -w ${DB_NAME})" == "" ];
then
  echo "create db '${DB_NAME}'..."
  sudo -i -u postgres createdb -O ${DB_USER_NAME} ${DB_NAME}
fi

DB_HOST=${DB_HOST:=}
DB_URL="postgres://${DB_USER_NAME}:${DB_USER_PASS}@${DB_HOST}/${DB_NAME}"

echo "create tables into '${DB_NAME}'..."
psql ${DB_URL} -f ${SCRIPT_DIR}/init_tables.sql -v "schema=public"


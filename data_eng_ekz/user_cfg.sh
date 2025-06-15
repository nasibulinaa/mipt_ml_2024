#!/bin/bash

# TODO: build docker image instead of installing pip3 packages EVERY TIME
# echo "_PIP_ADDITIONAL_REQUIREMENTS=pydrive2==1.21.3" >> .env

# Add some directories mount
mkdir -p ./data ./results
for dir in etl results data; do
    sed -i "/\/opt\/airflow\/plugins/a \ \ \ \ - \${AIRFLOW_PROJ_DIR:-.}/$dir:/opt/airflow/$dir" docker-compose.yaml
done

# Hide paused DAGs
sed -i 's|hide_paused_dags_by_default = False|hide_paused_dags_by_default = True|' ./config/airflow.cfg

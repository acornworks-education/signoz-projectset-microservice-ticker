kubectl -n acornworks create configmap ticker-db-config --from-file db/init_db.sql
kubectl -n acornworks create configmap ticker-db-flyway --from-file flyway/

DB_PASSWORD=$(uuidgen | cut -d "-" -f 1)
kubectl -n acornworks create secret generic ticker-db-password --from-literal=password=${DB_PASSWORD}
kubectl get secret -n acornworks ticker-db-password -o jsonpath='{.data}' | jq -r ".password" | base64 --decode
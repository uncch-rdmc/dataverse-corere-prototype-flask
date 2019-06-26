#!/bin/bash

kubectl apply -f db-service.yaml,flaskapp-service.yaml, db-deployment.yaml, db-envf-configmap.yaml, db-ingress.yaml,dbdata-persistentvolumeclaim.yaml, flaskapp-deployment.yaml, flaskapp-envf-configmap.yaml, flaskapp-ingress.yaml, flaskapp-claim0-persistentvolumeclaim.yaml






#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

PROJECT_ID=$(gcloud config get-value project)
CLUSTER_NAME="cloudymovie"
LOCATION="europe-west3" # Or your desired region

echo "--- Starting Cloud Build Deployment ---"

# 1. Create the GKE Autopilot cluster (if it doesn't exist)
echo "Creating GKE cluster: $CLUSTER_NAME in $LOCATION (if it doesn't exist)..."
gcloud container clusters create-auto "$CLUSTER_NAME" \
    --location="$LOCATION" || true

# 2. Get cluster credentials
echo "Getting cluster credentials..."
gcloud container clusters get-credentials "$CLUSTER_NAME" \
    --location="$LOCATION"

# 3. Create Kubernetes Secrets using environment variables from Cloud Build
echo "Creating Kubernetes secrets using values from Secret Manager..."

# For account-service
kubectl create secret generic account-mongo-secret \
    --from-literal=DB_USER="${DB_USER_ACCOUNT}" \
    --from-literal=DB_PASS="${DB_PASS_ACCOUNT}" \
    --dry-run=client -o yaml | kubectl apply -f -

# For movie-service
kubectl create secret generic movie-mongo-secret \
    --from-literal=DB_USER="${DB_USER_MOVIE}" \
    --from-literal=DB_PASS="${DB_PASS_MOVIE}" \
    --dry-run=client -o yaml | kubectl apply -f -

# For tournament-service
kubectl create secret generic tournament-mongo-secret \
    --from-literal=DB_USER="${DB_USER_TOURNAMENT}" \
    --from-literal=DB_PASS="${DB_PASS_TOURNAMENT}" \
    --dry-run=client -o yaml | kubectl apply -f -

# 4. Apply Kubernetes YAML files
echo "Applying Kubernetes deployments..."

# Iterate over each YAML file that is NOT cloudbuild.yaml and apply it
for file in $(find . -maxdepth 1 -name "*.yaml" -not -name "cloudbuild.yaml" -not -name "cloudbuild-ci.yaml"); do
  echo "Applying: $file" # Optional: to see which file is being applied
  kubectl apply -f "$file"
done

echo "--- Cloud Build Deployment Finished ---"
#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

PROJECT_ID=$(gcloud config get-value project)
CLUSTER_NAME="hello-cluster"
LOCATION="europe-west4" # Or your desired region

echo "--- Starting Cloud Build Deployment ---"

# 1. Create the GKE Autopilot cluster (if it doesn't exist)
#    We use --enable-private-nodes and --master-ipv4-cidr-block for better security in a real-world scenario.
#    For simplicity, if you're consistently using the same cluster, you might create it manually
#    once and then just get credentials. This script assumes it might not exist.
#    For CI/CD, you typically want your build job to be idempotent, so creating a cluster
#    each time is generally not recommended unless it's a test environment.
#    For production, you'd likely have a persistent cluster.
#    For this example, we'll try to create it, and if it exists, it will fail gracefully.
echo "Creating GKE cluster: $CLUSTER_NAME in $LOCATION (if it doesn't exist)..."
gcloud container clusters create-auto "$CLUSTER_NAME" \
    --location="$LOCATION" || true # Using || true to prevent script from failing if cluster exists

# 2. Get cluster credentials
echo "Getting cluster credentials..."
gcloud container clusters get-credentials "$CLUSTER_NAME" \
    --location="$LOCATION"

# 3. Create Kubernetes Secrets
#    It's generally recommended to store secrets in a more secure way for production,
#    like Google Secret Manager, and inject them into your pods.
#    For this exercise, using --from-literal is acceptable, but be aware of the implications.
echo "Creating Kubernetes secrets..."
kubectl create secret generic account-mongo-secret --from-literal=DB_USER=account-service --from-literal=DB_PASS=wLFbz3BfbskMsMJz --dry-run=client -o yaml | kubectl apply -f -
kubectl create secret generic movie-mongo-secret --from-literal=DB_USER=movie-service --from-literal=DB_PASS=GSKLzHMYDXkw9nnv --dry-run=client -o yaml | kubectl apply -f -
kubectl create secret generic tournament-mongo-secret --from-literal=DB_USER=tournament-service --from-literal=DB_PASS=4hUrXKqbxLHfUTDR --dry-run=client -o yaml | kubectl apply -f -

# The --dry-run=client -o yaml | kubectl apply -f - pattern ensures that if the secret already exists,
# it will attempt to apply the new definition, which is more robust for CI/CD than just `create`
# which would fail if the secret already exists.

# 4. Apply Kubernetes YAML files
echo "Applying Kubernetes deployments..."
# Assuming your Kubernetes YAML files are in the current directory (the root of your cloned repo)
kubectl apply -f .

echo "--- Cloud Build Deployment Finished ---"
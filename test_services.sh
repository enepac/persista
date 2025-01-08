#!/bin/bash

# Load environment variables from .env
set -o allexport
if [ -f .env ]; then
  echo "Loading environment variables from .env..."
  source .env
else
  echo "Error: .env file not found!"
  exit 1
fi
set +o allexport

# Helper function for error handling
log_and_exit() {
  echo "Error: $1"
  exit 1
}

echo "Starting Docker Compose services..."
docker-compose up -d || log_and_exit "Failed to start Docker Compose services."

echo "Checking container status..."
docker ps || log_and_exit "Docker containers are not running."

# Test Postgres
echo "Testing Postgres..."
docker exec -i persista_postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT version();" > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "Postgres is running and accessible."
else
  log_and_exit "Postgres test failed. Check logs with: docker logs persista_postgres"
fi

# Test Redis
echo "Testing Redis..."
docker exec -i persista_redis redis-cli ping > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "Redis is running and accessible."
else
  log_and_exit "Redis test failed. Check logs with: docker logs persista_redis"
fi

# Test Etcd
echo "Testing Etcd..."
docker exec -i persista_etcd etcdctl endpoint health > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "Etcd is healthy and running."
else
  log_and_exit "Etcd test failed. Check logs with: docker logs persista_etcd"
fi

# Test MinIO
echo "Testing MinIO..."
mc alias set myminio http://localhost:9000 minioadmin minioadmin > /dev/null 2>&1
if [ $? -eq 0 ]; then
  mc mb myminio/test-bucket > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "MinIO is running and accessible."
  else
    log_and_exit "MinIO bucket creation failed."
  fi
else
  log_and_exit "MinIO test failed."
fi


# Test Milvus
echo "Testing Milvus..."
curl -s http://localhost:19530/version > /dev/null
if [ $? -eq 0 ]; then
  echo "Milvus is running and accessible."
else
  log_and_exit "Milvus test failed. Check logs with: docker logs persista_milvus"
fi

# Test Backend
echo "Testing Backend..."
curl -s http://localhost:5000/ > /dev/null
if [ $? -eq 0 ]; then
  echo "Backend is running and accessible."
else
  log_and_exit "Backend test failed. Check logs with: docker logs persista_backend"
fi

# Test Frontend
echo "Testing Frontend..."
curl -s http://localhost:4283 > /dev/null
if [ $? -eq 0 ]; then
  echo "Frontend is running and accessible."
else
  log_and_exit "Frontend test failed. Check logs with: docker logs persista_frontend"
fi

echo "All tests completed successfully."

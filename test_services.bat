@echo off
echo Testing Services... > test_results.log

REM Test PostgreSQL
echo Testing PostgreSQL... >> test_results.log
docker exec -i persista_postgres psql -U persista_admin -d persista_db -c "\l" >> test_results.log 2>&1

REM Test Redis
echo Testing Redis... >> test_results.log
docker exec -i persista_redis redis-cli ping >> test_results.log 2>&1

REM Test ETCD
echo Testing ETCD... >> test_results.log
docker exec -i persista_etcd etcdctl endpoint health >> test_results.log 2>&1

REM Test MinIO
echo Testing MinIO... >> test_results.log
curl -I http://localhost:9000/minio/health/live >> test_results.log 2>&1

REM Test Milvus
echo Testing Milvus... >> test_results.log
curl -I http://localhost:19530/api/v1/health >> test_results.log 2>&1

REM Test Backend
echo Testing Backend... >> test_results.log
curl -I http://localhost:5000/health >> test_results.log 2>&1

REM Test Frontend
echo Testing Frontend... >> test_results.log
curl -I http://localhost:4283 >> test_results.log 2>&1

REM Check all containers
echo Container Status: >> test_results.log
docker-compose ps >> test_results.log 2>&1

type test_results.log
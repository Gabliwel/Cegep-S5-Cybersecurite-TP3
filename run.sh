docker-compose -f project/docker/docker-compose.yml --project-directory . down
docker-compose -f project/docker/docker-compose.yml --project-directory . build
docker-compose -f project/docker/docker-compose.yml --project-directory . up -d
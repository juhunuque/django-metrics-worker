build:
	docker-compose rm -vsf
	docker-compose down -v --remove-orphans
	docker-compose build

up:
	docker-compose up -d

stop:
	docker-compose rm -vsf
	docker-compose down -v --remove-orphans

down:
	docker-compose down -v

logs:
	docker-compose logs -f

redis:
	docker-compose up -d redis_svc
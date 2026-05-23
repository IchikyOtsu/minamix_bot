deploy:
	git pull && docker compose up -d --build bot

restart:
	docker compose restart bot

logs:
	docker compose logs -f bot

status:
	docker compose ps

# Opencast BugBash :: Leaderboard

Run locally:

```sh
gunicorn -w 1 leaderboard:app
```

Use `docker` or `podman`:

```sh
podman run -it --rm -p 127.0.0.1:8000:8000 ghcr.io/lkiesow/opencast-bugbash-leaderboard:main
```

A `docker-compose.yml` with reverse proxy and HTTPS with valid TSL vertificate:

```yml
services:
  leaderboard:
    image: ghcr.io/lkiesow/opencast-bugbash-leaderboard:main
    restart: always
    volumes:
      - /srv/leaderboard.db:/app/leaderboard.db
    networks:
      - leaderboard

  caddy:
    image: docker.io/library/caddy:2-alpine
    command: caddy reverse-proxy --to leaderboard:8000 --from bugbash.opencast.org
    ports:
      - 80:80
      - 443:443
    restart: always
    networks:
      - leaderboard

networks:
  leaderboard:
```

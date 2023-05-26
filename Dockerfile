FROM caddy:latest

COPY Caddyfile /etc/caddy/Caddyfile

VOLUME /data

EXPOSE 80
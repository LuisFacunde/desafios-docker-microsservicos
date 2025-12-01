FROM alpine:latest

RUN apk add curl

COPY script.sh /app/script.sh

RUN chmod +x /app/script.sh

CMD ["/app/script.sh"]
FROM alpine:latest

RUN apk --no-cache add curl

WORKDIR /app

COPY script.sh .

RUN chmod +x script.sh

CMD ["/app/script.sh"]
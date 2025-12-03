SERVER_URL="http://servidor:8080" 

echo "Iniciando requisições periódicas para $SERVER_URL..."

while true; do
  echo "--- $(date) ---"
  curl -s $SERVER_URL
  echo ""
  sleep 3
done
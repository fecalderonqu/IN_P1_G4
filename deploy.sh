# Variables estilo deploy.sh existente
NAME_CONTAINER="db_postgres_practica1_g4"
NAME_IMAGE="db_postgres_practica1_g4"
PORT_EXPOSE=5432
ENV_PATH=".env"

echo ">> Construyendo imagen $NAME_IMAGE ..."
docker build -t "$NAME_IMAGE" .
echo "Compilado correctamente"

echo ">> Eliminando contenedor previo (si existe)..."
docker rm -f "$NAME_CONTAINER"

echo ">> Iniciando contenedor $NAME_CONTAINER ..."
docker run --name "$NAME_CONTAINER" --restart unless-stopped \
    --env-file "$ENV_PATH" \
    -p "$PORT_EXPOSE":5432 \
    -v db_postgres_data:/var/lib/postgresql/data \
    -d "$NAME_IMAGE"

echo "Successfull service"
# Imagen de base
FROM postgres:16-alpine

# Variables de entorno por defecto (pueden ser sobreescritas vía --env-file)
ENV LANG=es_ES.utf8         LC_ALL=es_ES.utf8         TZ=${TZ:-America/Guayaquil}

# Exponer el puerto de PostgreSQL
EXPOSE 5432

# Salud del contenedor
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" || exit 1

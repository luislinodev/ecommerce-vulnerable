# Docker Setup - Ecommerce Django

Este proyecto está configurado para ejecutarse con Docker y Docker Compose.

## Requisitos Previos

- Docker Desktop (incluyendo Docker Engine y Docker Compose)
- Git

## Archivos Docker Creados

- `Dockerfile` - Imagen Docker del servicio web (Django)
- `docker-compose.yml` - Orquestación de servicios (Django, PostgreSQL, Redis)
- `.dockerignore` - Archivos a ignorar en la construcción de la imagen
- `.env.docker` - Variables de entorno para desarrollo con Docker
- `entrypoint.sh` - Script de inicialización del contenedor
- `Makefile` - Comandos de utilidad para Docker

## Quick Start

### 1. Clonar el repositorio y navegar a la carpeta

```bash
cd ecommerce-django
```

### 2. Copiar archivo de configuración

```bash
cp .env.docker .env
```

### 3. Construir las imágenes

```bash
docker-compose build
# o
make build
```

### 4. Iniciar los contenedores

```bash
docker-compose up -d
# o
make up
```

Esto iniciará:
- **web**: Django en http://localhost:8000
- **db**: PostgreSQL en localhost:5432
- **redis**: Redis en localhost:6379

### 5. Crear usuario admin (opcional)

```bash
docker-compose exec web python manage.py createsuperuser
# o
make createsuperuser
```

### 6. Acceder a la aplicación

- Aplicación: http://localhost:8000
- Admin: http://localhost:8000/admin

## Comandos Útiles

### Ver logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo web
docker-compose logs -f web

# Con make
make logs-web
```

### Acceder a Django Shell
```bash
docker-compose exec web python manage.py shell
# o
make shell
```

### Ejecutar migraciones
```bash
docker-compose exec web python manage.py migrate
# o
make migrate
```

### Crear migraciones
```bash
docker-compose exec web python manage.py makemigrations
# o
make migrations
```

### Acceder a la base de datos PostgreSQL
```bash
docker-compose exec db psql -U ecommerce_user -d ecommerce_db
# o
make dbshell
```

### Detener contenedores
```bash
docker-compose down
# o
make down
```

### Limpiar todo (elimina volúmenes)
```bash
docker-compose down -v
# o
make clean
```

### Reiniciar contenedores
```bash
make restart
```

## Estructura de Servicios

### 1. **web** (Django)
- Puerto: 8000
- Imagen: Personalizada (Dockerfile)
- Volúmenes: Código, archivos estáticos, media
- Depende de: db (PostgreSQL)

### 2. **db** (PostgreSQL)
- Puerto: 5432
- Imagen: postgres:16-alpine
- Volumen: postgres_data (datos persistentes)
- Base de datos: ecommerce_db
- Usuario: ecommerce_user

### 3. **redis** (Cache)
- Puerto: 6379
- Imagen: redis:7-alpine
- Volumen: redis_data (datos persistentes)

## Variables de Entorno

Todas las variables están en `.env.docker`. Principales:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,web

# Database
SQL_DATABASE=ecommerce_db
SQL_USER=ecommerce_user
SQL_PASSWORD=secure_password_123
SQL_HOST=db
SQL_PORT=5432

# CORS
CORS_ALLOW_ALL_ORIGINS=True

# Email (Console por defecto en desarrollo)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## Desarrollo

### Recargar código automáticamente
El código está mapeado como volumen, así que los cambios se reflejarán automáticamente.

### Instalar nuevas dependencias
```bash
# 1. Agregar a requirements.txt
# 2. Reconstruir imagen
docker-compose build

# 3. Reiniciar contenedores
docker-compose up -d
```

### Ejecutar tests
```bash
docker-compose exec web python manage.py test
# o
make test
```

## Problemas Comunes

### Puerto 8000 ya está en uso
Cambiar el puerto en `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Mapear a 8001
```

### Base de datos no inicializa
Ver logs de la base de datos:
```bash
docker-compose logs db
```

### Permisos de archivos
El contenedor usa usuario `appuser` (UID 1000). Si hay problemas:
```bash
docker-compose exec web chmod -R 755 /app
```

### Eliminar todo y empezar de cero
```bash
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

## Production Ready

Para producción:

1. **Cambiar SECRET_KEY** a un valor aleatorio seguro
2. **Configurar DJANGO_DEBUG=False**
3. **Usar certificados SSL** (HTTPS)
4. **Configurar base de datos** con backup automático
5. **Usar gestor de secretos** para credenciales
6. **Configurar ALLOWED_HOSTS** con dominio real
7. **Usar servicio de email** real (SendGrid, AWS SES, etc.)
8. **Habilitar CSRF y cookies seguras**

## Referencias

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django with Docker](https://docs.djangoproject.com/en/6.0/topics/deployment/docker/)

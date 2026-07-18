# Ecommerce Django - PENTESTING EDITION

> **⚠️ FOR AUTHORIZED SECURITY TESTING ONLY** | Edición de pentesting con vulnerabilidades intencionales

Ecommerce web app construida con Django para la gestión de productos, carrito, pedidos y pagos. 
**Esta versión incluye 14 vulnerabilidades de seguridad deliberadamente implementadas para propósitos de pruebas de penetración y educación.**

---

## 🚀 Opciones de Despliegue

### Opción 1: PENTESTING (Con vulnerabilidades)
Para pruebas de seguridad autorizadas y laboratorios de educación.

### Opción 2: PRODUCCIÓN (Segura)
Configuración segura lista para producción.

---

## 🔴 PENTESTING EDITION

### ⚠️ Vulnerabilidades Intencionadas (14 total)

| # | Tipo | Endpoint | Impacto |
|---|------|----------|---------|
| 1 | SQL Injection | `/api/debug/sql-injection/` | Database manipulation |
| 2 | Command Injection (RCE) | `/api/debug/cmd-injection/` | System compromise |
| 3 | Path Traversal | `/api/debug/read-file/` | File disclosure |
| 4 | XXE | `/api/debug/xml-parser/` | SSRF/DoS |
| 5 | Information Disclosure | `/api/debug/system-info/` | Server fingerprinting |
| 6 | Weak Authentication | `/api/debug/weak-auth/` | Unauthorized access |
| 7 | Unsafe Deserialization | `/api/debug/unsafe-pickle/` | RCE |
| 8 | Sensitive Logging | `/api/debug/log-data/` | Data exposure |
| 9 | IDOR | `/api/debug/get-logs/` | Unauthorized access |
| 10 | Code Injection | `/api/debug/process-data/` | RCE |
| 11 | CORS Misconfiguration | Global | Cross-origin attacks |
| 12 | Debug Mode Enabled | Global | Information leakage |
| 13 | Insecure Cookies | Global | Session hijacking |
| 14 | Database Exposed | Port 5050 (pgAdmin) | Database access |

### 🚀 Quick Start - PENTESTING

#### Local (Linux/Mac/Windows)

```bash
# 1. Preparar proyecto
cp .env.pentesting .env

# 2. Iniciar servicios
docker-compose -f docker-compose.pentesting.yml up -d

# 3. Acceder
# - App:     http://localhost:8000
# - Admin:   http://localhost:8000/admin
# - pgAdmin: http://localhost:5050

# 4. Credenciales por defecto
# Admin: admin / admin123
# pgAdmin: admin@example.com / admin123
# DB: ecommerce_user / ecommerce_pass
```

#### AWS EC2 Deployment

```bash
# Conectar a instancia
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Clonar repositorio
git clone <repo-url>
cd ecommerce-django

# Ejecutar script de deployment
./aws-deploy.sh

# Acceder
# http://YOUR_EC2_IP:8000
```

### 📚 Documentación de Pentesting

- **[PENTESTING_GUIDE.md](PENTESTING_GUIDE.md)** - Guía completa con técnicas de explotación
- **[README_PENTESTING.md](README_PENTESTING.md)** - Setup y roadmap de testing
- **[VULNERABILITIES_SUMMARY.md](VULNERABILITIES_SUMMARY.md)** - Matriz de vulnerabilidades
- **[SETUP_QUICK_REFERENCE.txt](SETUP_QUICK_REFERENCE.txt)** - Referencia rápida

### 🧪 Ejemplos de Explotación

```bash
# SQL Injection
curl "http://localhost:8000/api/debug/sql-injection/?user_id=1 OR 1=1"

# Command Execution (RCE)
curl "http://localhost:8000/api/debug/cmd-injection/?cmd=whoami"

# Path Traversal
curl "http://localhost:8000/api/debug/read-file/?file=../../../../.env"

# Weak Authentication
curl "http://localhost:8000/api/debug/weak-auth/?username=admin&password=admin123"

# Information Disclosure
curl http://localhost:8000/api/debug/system-info/
```

---

## ✅ PRODUCCIÓN EDITION

Para usar el proyecto en **producción segura**, ignorar la configuración de pentesting y usar:

```bash
cp .env.prod.example .env
# Editar .env con valores reales
docker-compose -f docker-compose.prod.yml up -d
```

### Características Principales (PRODUCCIÓN)

- ✅ Catálogo de productos con detalle y categorías
- ✅ Carrito de compras con ajuste de cantidad
- ✅ Checkout con cálculo de IGV, transporte y total
- ✅ Gestión de pedidos y perfil de usuario
- ✅ Autenticación con Django Allauth + Google Social Login
- ✅ Integración con Izipay para pagos
- ✅ Configuración basada en variables de entorno
- ✅ Docker ready
- ✅ Nginx + SSL/TLS
- ✅ PostgreSQL persistente
- ✅ Redis cache
- ✅ Seguridad hardened

---

## 📦 Requisitos

### Opción 1: Docker (Recomendado)
- Docker Desktop
- Docker Compose

### Opción 2: Local
- Python 3.12+
- PostgreSQL
- pip
- Virtual environment

---

## 🐳 Docker Setup

### Desarrollo Pentesting

```bash
cp .env.pentesting .env
docker-compose -f docker-compose.pentesting.yml up -d
```

Servicios:
- Django (puerto 8000)
- PostgreSQL (puerto 5432)
- Redis (puerto 6379)
- pgAdmin (puerto 5050)

### Desarrollo Normal

```bash
cp .env.docker .env
docker-compose -f docker-compose.dev.yml up -d
```

### Producción

```bash
cp .env.prod.example .env
# Editar .env
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🖥️ Setup Local (Sin Docker)

### 1. Clonar repositorio

```bash
git clone https://github.com/tu-usuario/ecommerce-django.git
cd ecommerce-django
```

### 2. Crear virtual environment

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.docker .env
# Editar .env según tus necesidades
```

### 5. Base de datos

```bash
# PostgreSQL debe estar corriendo en localhost:5432
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Iniciar servidor

```bash
python manage.py runserver
```

Abrir: http://127.0.0.1:8000/

---

## 📋 Variables de Entorno

### Pentesting (`.env.pentesting`)
```env
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DJANGO_SECRET_KEY=django-insecure-a#%@9j5k3l2m1n0p9o8i7u6y5t4r3e2w1q0z9x8c7v6b5n4m3l2k1j0h9g8f7e6d5
CORS_ALLOW_ALL_ORIGINS=True
SESSION_COOKIE_SECURE=False
# ... (todas las variables debilitadas)
```

### Producción (`.env.prod.example`)
```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-super-secret-key
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
# ... (todas las configuraciones seguras)
```

---

## 🛠️ Comandos Útiles

### Docker

```bash
# Ver logs
docker-compose logs -f web

# Acceder a shell de Django
docker-compose exec web python manage.py shell

# Acceder a base de datos
docker-compose exec db psql -U ecommerce_user -d ecommerce_db

# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Detener servicios
docker-compose down

# Limpiar todo (incluyendo datos)
docker-compose down -v
```

### Local

```bash
# Migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell de Django
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar tests
python manage.py test
```

---

## 🔒 Seguridad

### Pentesting
⚠️ **Esta configuración es INTENCIONALMENTE INSEGURA para testing**
- DEBUG=True (expone información sensible)
- CORS permitido desde cualquier origen
- Credentials débiles
- Sin HTTPS enforcement
- Cookies inseguras

### Producción
✅ Configuración segura
- DEBUG=False
- HTTPS/SSL enforcement
- CORS restringido
- Cookies seguras
- Headers de seguridad
- CSRF protection

**⚠️ Nunca usar configuración de pentesting en producción**

---

## 📚 Documentación

### General
- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Configuración Docker
- [DOCKER_FILES_SUMMARY.md](DOCKER_FILES_SUMMARY.md) - Resumen de archivos Docker

### Pentesting
- [PENTESTING_GUIDE.md](PENTESTING_GUIDE.md) - **LEER PRIMERO para pentesting**
- [README_PENTESTING.md](README_PENTESTING.md) - Quick start guide
- [VULNERABILITIES_SUMMARY.md](VULNERABILITIES_SUMMARY.md) - Matriz de vulnerabilidades
- [SETUP_QUICK_REFERENCE.txt](SETUP_QUICK_REFERENCE.txt) - Referencia rápida

---

## 🧪 Testing

### Pentesting Checklist

- [ ] Reconnaissance (Nmap, fingerprinting)
- [ ] SQL Injection testing
- [ ] Command Injection testing
- [ ] Path Traversal testing
- [ ] XXE testing
- [ ] Authentication bypass
- [ ] CORS exploitation
- [ ] Debug mode information leakage
- [ ] Database enumeration
- [ ] Post-exploitation

### Unit Tests

```bash
# Ejecutar todos los tests
python manage.py test

# Tests específicos
python manage.py test accounts
python manage.py test catalog
```

---

## 🌐 Herramientas Recomendadas

### Pentesting Tools
- OWASP ZAP
- Burp Suite
- SQLmap
- Commix
- Nikto
- Nmap

### Development Tools
- VS Code
- PyCharm
- Postman
- Insomnia
- pgAdmin

---

## 🚨 Advertencia Legal

⚠️ **IMPORTANTE**:

```
Esta aplicación contiene VULNERABILIDADES INTENCIONADAS para propósitos
de PRUEBAS DE SEGURIDAD AUTORIZADAS y EDUCACIÓN.

✅ PERMITIDO:
   - Pentesting autorizado
   - Laboratorios de seguridad
   - Educación y capacitación
   - CTF competitions

❌ NO PERMITIDO:
   - Acceso no autorizado
   - Uso malicioso
   - Testing sin permiso
   - Daño intencional
```

El acceso no autorizado a sistemas informáticos es **ILEGAL** bajo la CFAA 
(Computer Fraud and Abuse Act) y leyes equivalentes internacionales.

**Usuario responsable**: Cada usuario es responsable del uso legal de esta aplicación.

---

## 📞 Contacto & Soporte

Para problemas con:
- **Docker**: Ver [DOCKER_SETUP.md](DOCKER_SETUP.md)
- **Pentesting**: Ver [PENTESTING_GUIDE.md](PENTESTING_GUIDE.md)
- **Configuración**: Ver [README_PENTESTING.md](README_PENTESTING.md)

---

## 📄 Licencia

Este proyecto se proporciona "tal cual" para fines educativos y de testing autorizado.

---

## 🎯 Roadmap

- [x] Ecommerce funcional
- [x] Autenticación
- [x] Carrito y checkout
- [x] Docker ready
- [x] 14 vulnerabilidades para pentesting
- [x] Documentación completa
- [ ] CI/CD pipeline
- [ ] Monitoring y logging
- [ ] Rate limiting
- [ ] WAF rules

---

**Última actualización**: 2026-07-18
**Versión**: 2.0 (Pentesting Edition)
**Status**: Listo para testing autorizado

# ecommerce-django

Ecommerce web app de prueba construida con Django para la gestión de productos, carrito, pedidos y pagos.

## Características principales

- Catálogo de productos con detalle y categorías.
- Carrito de compras con ajuste de cantidad y eliminación de ítems.
- Checkout con cálculo de IGV, transporte y total.
- Gestión de pedidos y perfil de usuario.
- Autenticación con Django Allauth y soporte para Google Social Login.
- Integración con Izipay para generar tokens de pago.
- Configuración basada en variables de entorno.

## Requisitos

- Python 3.12+
- pip
- Virtual environment (recomendado)

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/ecommerce-django.git
cd ecommerce-django
```

2. Crea y activa un entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

4. Copia el archivo de ejemplo de configuración:

```bash
copy .env.example .env
```

5. Edita `.env` con tus valores reales.

6. Ejecuta migraciones:

```bash
python manage.py migrate
```

7. Crea un superusuario opcional:

```bash
python manage.py createsuperuser
```

8. Inicia el servidor:

```bash
python manage.py runserver
```

9. Abre el navegador en:

```text
http://127.0.0.1:8000/
```

## Variables de entorno

El proyecto lee valores sensibles y de configuración desde `.env` o variables del sistema.

- `DJANGO_SECRET_KEY`: clave secreta de Django.
- `DJANGO_DEBUG`: `True` o `False`.
- `DJANGO_ALLOWED_HOSTS`: hosts permitidos, separados por espacios.
- `EMAIL_BACKEND`: backend de correo (por ejemplo, `django.core.mail.backends.smtp.EmailBackend`).
- `EMAIL_HOST_PASSWORD`: contraseña o clave API del servicio SMTP.
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`: para login con Google.
- `IZIPAY_PUBLIC_KEY`, `IZIPAY_MERCHANT_CODE`: para la integración de pagos.

## Mejores prácticas

- No comites tus secretos ni el archivo `.env` al repositorio.
- Usa `python manage.py collectstatic` antes de desplegar en producción.
- Configura `DEBUG=False` y `ALLOWED_HOSTS` correctamente en entornos públicos.

## Mejoras introducidas

- Configuración segura desde `ENV`.
- Eliminación de claves sensibles hardcodeadas.
- Ajustes de `django-allauth` para autenticación por email.
- Validación de checkout y manejo de carrito vacío.
- Soporte de seguridad adicional cuando `DEBUG=False`.
- Nueva plantilla de `.env.example`.

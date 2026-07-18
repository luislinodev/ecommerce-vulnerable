from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import subprocess
import os
import json
from .models import DebugLog


# VULNERABLE: SQL Injection
@csrf_exempt
@require_http_methods(["GET", "POST"])
def sql_injection(request):
    """
    Vulnerable to SQL injection via 'user_id' parameter.
    Example: /api/debug/sql-injection/?user_id=1 OR 1=1
    """
    user_id = request.GET.get('user_id', '1')

    # VULNERABLE: Direct string concatenation in SQL query
    query = f"SELECT * FROM accounts_user WHERE id = {user_id}"

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return JsonResponse({
            "status": "success",
            "query": query,
            "result": result
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e),
            "query": query
        }, status=500)


# VULNERABLE: Command Injection
@csrf_exempt
@require_http_methods(["GET", "POST"])
def command_injection(request):
    """
    Vulnerable to OS command injection via 'cmd' parameter.
    Example: /api/debug/cmd-injection/?cmd=whoami;id;pwd
    """
    cmd = request.GET.get('cmd', 'whoami')

    try:
        # VULNERABLE: Direct command execution without sanitization
        result = subprocess.check_output(cmd, shell=True, text=True)
        return JsonResponse({
            "status": "success",
            "command": cmd,
            "output": result
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e),
            "command": cmd
        }, status=500)


# VULNERABLE: Path Traversal
@csrf_exempt
@require_http_methods(["GET"])
def file_read(request):
    """
    Vulnerable to path traversal via 'file' parameter.
    Example: /api/debug/read-file/?file=../../../../etc/passwd
    """
    file_path = request.GET.get('file', 'README.md')

    try:
        # VULNERABLE: No path validation - allows reading arbitrary files
        base_path = os.path.dirname(__file__)
        full_path = os.path.join(base_path, file_path)

        with open(full_path, 'r') as f:
            content = f.read()

        return JsonResponse({
            "status": "success",
            "file": file_path,
            "content": content[:5000]  # First 5000 chars
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e),
            "file": file_path
        }, status=500)


# VULNERABLE: XXE (XML External Entity)
@csrf_exempt
@require_http_methods(["POST"])
def xml_parser(request):
    """
    Vulnerable to XXE attacks via XML parsing.
    """
    try:
        xml_data = request.POST.get('xml', '<root></root>')

        # VULNERABLE: Using defusedxml not available, plain xml.etree
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_data)

        result = {}
        for child in root:
            result[child.tag] = child.text

        return JsonResponse({
            "status": "success",
            "parsed": result
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e)
        }, status=500)


# VULNERABLE: Information Disclosure
@csrf_exempt
@require_http_methods(["GET"])
def system_info(request):
    """
    Exposes sensitive system information without authentication.
    """
    import platform
    import django

    info = {
        "python_version": platform.python_version(),
        "os": platform.system(),
        "platform": platform.platform(),
        "django_version": django.get_version(),
        "installed_packages": [
            "django-allauth", "pillow", "djangorestframework"
        ],
        "debug_mode": os.environ.get("DJANGO_DEBUG", "True"),
        "secret_key_first_chars": os.environ.get("DJANGO_SECRET_KEY", "")[:20],
    }

    return JsonResponse(info)


# VULNERABLE: Weak Authentication
@csrf_exempt
@require_http_methods(["GET", "POST"])
def weak_auth(request):
    """
    Uses weak/hardcoded credentials for authentication.
    Credentials: admin:admin123 or admin:password
    """
    username = request.GET.get('username') or request.POST.get('username')
    password = request.GET.get('password') or request.POST.get('password')

    # VULNERABLE: Hardcoded credentials check
    if (username == "admin" and password in ["admin123", "password", "admin"]):
        return JsonResponse({
            "status": "authenticated",
            "message": "Welcome admin",
            "token": "weaktoken123456789"
        })

    return JsonResponse({
        "status": "unauthorized",
        "message": "Invalid credentials"
    }, status=401)


# VULNERABLE: Unsafe Deserialization
@csrf_exempt
@require_http_methods(["POST"])
def unsafe_pickle(request):
    """
    Vulnerable to pickle deserialization attacks.
    """
    import pickle
    import base64

    try:
        data = request.POST.get('data', '')
        # VULNERABLE: Using pickle.loads on user input
        decoded = base64.b64decode(data)
        obj = pickle.loads(decoded)

        return JsonResponse({
            "status": "success",
            "deserialized": str(obj)
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e)
        }, status=500)


# VULNERABLE: Debug Logging with Sensitive Data
@csrf_exempt
@require_http_methods(["POST"])
def log_data(request):
    """
    Logs all request data without filtering sensitive information.
    """
    try:
        # VULNERABLE: Logs all POST data including potential passwords
        DebugLog.objects.create(
            message=str(request.POST),
            user=request.GET.get('user', 'anonymous')
        )

        return JsonResponse({
            "status": "logged",
            "message": "Data logged successfully"
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "error": str(e)
        }, status=500)


# VULNERABLE: Debug Logs Exposure
@csrf_exempt
@require_http_methods(["GET"])
def get_logs(request):
    """
    Exposes all debug logs without authentication or filtering.
    """
    logs = DebugLog.objects.all().values()
    return JsonResponse({
        "status": "success",
        "logs": list(logs)
    })


# VULNERABLE: No Input Validation
@csrf_exempt
@require_http_methods(["POST"])
def process_data(request):
    """
    Processes user input without any validation or sanitization.
    """
    user_input = request.POST.get('data', '')

    # VULNERABLE: Direct use of unsanitized input
    result = eval(user_input)  # EXTREMELY DANGEROUS!

    return JsonResponse({
        "status": "success",
        "input": user_input,
        "result": str(result)
    })

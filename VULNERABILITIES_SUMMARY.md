# Pentesting Configuration - Vulnerabilities Summary

## ⚠️ FOR AUTHORIZED SECURITY TESTING ONLY

This document summarizes all intentional vulnerabilities implemented for penetration testing purposes.

---

## Modified Files

### 1. **z_app_fle_pruebas/settings.py**
**Changes**: Added intentional security misconfigurations

```python
# VULNERABLE: Hardcoded weak SECRET_KEY
SECRET_KEY = "django-insecure-a#%@9j5k3l2m1n0p9o8i7u6y5t4r3e2w1q0z9x8c7v6b5n4m3l2k1j0h9g8f7e6d5"

# VULNERABLE: DEBUG=True by default
DEBUG = True

# VULNERABLE: Wildcard in ALLOWED_HOSTS
ALLOWED_HOSTS = "*"

# VULNERABLE: CORS allows all origins with credentials
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# VULNERABLE: Security headers disabled
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
X_FRAME_OPTIONS = "ALLOW"
```

### 2. **z_app_fle_pruebas/urls.py**
**Changes**: Added debug endpoints routing

```python
path('api/debug/', include('debug_endpoints.urls'))
```

### 3. **requirements.txt**
**Changes**: Added dependencies for pentesting

```
psycopg2-binary==2.9.10
gunicorn==23.0.0
```

---

## New Files Created

### Core Pentesting App

#### **debug_endpoints/** (New Django App)
Vulnerable endpoints for security testing

##### **debug_endpoints/views.py**
Contains 10 vulnerable endpoints:

| # | Vulnerability | Function | Endpoint | Parameter |
|---|---|---|---|---|
| 1 | SQL Injection | `sql_injection()` | `/api/debug/sql-injection/` | `user_id` |
| 2 | Command Injection (RCE) | `command_injection()` | `/api/debug/cmd-injection/` | `cmd` |
| 3 | Path Traversal | `file_read()` | `/api/debug/read-file/` | `file` |
| 4 | XXE | `xml_parser()` | `/api/debug/xml-parser/` | `xml` (POST) |
| 5 | Info Disclosure | `system_info()` | `/api/debug/system-info/` | - |
| 6 | Weak Authentication | `weak_auth()` | `/api/debug/weak-auth/` | `username`, `password` |
| 7 | Unsafe Deserialization | `unsafe_pickle()` | `/api/debug/unsafe-pickle/` | `data` (POST) |
| 8 | Sensitive Logging | `log_data()` | `/api/debug/log-data/` | `data`, `user` |
| 9 | Unauthorized Access | `get_logs()` | `/api/debug/get-logs/` | - |
| 10 | Code Injection | `process_data()` | `/api/debug/process-data/` | `data` (POST) |

##### **debug_endpoints/models.py**
```python
class DebugLog(models.Model):
    message = models.TextField()          # Stores all data including sensitive
    user = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
```

##### **debug_endpoints/urls.py**
Routes for all vulnerable endpoints

##### **debug_endpoints/admin.py**
Admin interface for viewing debug logs

##### **debug_endpoints/apps.py**
App configuration

---

### Configuration Files

#### **`.env.pentesting`**
Pre-configured environment for testing with:
- Weak SECRET_KEY
- DEBUG=True
- Wildcard ALLOWED_HOSTS
- Weak database credentials
- Default admin credentials: `admin:admin123`

#### **`.env.prod.example`**
(Already existed - template for production)

---

### Docker Configuration

#### **`docker-compose.pentesting.yml`** (NEW)
Orchestrates vulnerable services:

```yaml
Services:
  - web: Django runserver (port 8000)
  - db: PostgreSQL (port 5432)
  - redis: Redis cache (port 6379)
  - pgadmin: Database admin tool (port 5050)
    - Credentials: admin@example.com / admin123
```

**Environment Variables**:
- DJANGO_DEBUG=True
- DJANGO_ALLOWED_HOSTS=*
- CORS_ALLOW_ALL_ORIGINS=True
- All security headers disabled

#### **`Dockerfile`**
(Already existed - unchanged, installs vulnerable dependencies)

---

### Documentation

#### **`PENTESTING_GUIDE.md`** (NEW)
Comprehensive penetration testing guide including:
- Detailed vulnerability descriptions
- Exploitation examples
- Impact analysis
- Remediation strategies
- CWE references
- OWASP mappings

#### **`README_PENTESTING.md`** (NEW)
Quick start guide for:
- Local deployment
- AWS deployment
- Vulnerable endpoints list
- Testing roadmap
- Common issues

#### **`aws-deploy.sh`** (NEW)
Automated AWS EC2 deployment script
- Updates system
- Installs Docker/Docker Compose
- Configures firewall
- Deploys application

---

## Vulnerability Matrix

### OWASP Top 10 Coverage

| # | Vulnerability | Type | Endpoint(s) | CWE |
|---|---|---|---|---|
| A01 | Broken Access Control | IDOR | `/api/debug/get-logs/` | CWE-639 |
| A02 | Cryptographic Failures | Weak Keys | All (SECRET_KEY) | CWE-326 |
| A03 | Injection | SQL | `/api/debug/sql-injection/` | CWE-89 |
| A03 | Injection | Command | `/api/debug/cmd-injection/` | CWE-78 |
| A03 | Injection | Code | `/api/debug/process-data/` | CWE-94 |
| A04 | Insecure Design | Weak Auth | `/api/debug/weak-auth/` | CWE-521 |
| A05 | Security Misconfiguration | DEBUG=True | Global | CWE-16 |
| A05 | Security Misconfiguration | CORS | Global | CWE-942 |
| A06 | Vulnerable Components | XXE | `/api/debug/xml-parser/` | CWE-611 |
| A08 | Software/Data Integrity | Deserialization | `/api/debug/unsafe-pickle/` | CWE-502 |

### CWE Coverage

- **CWE-16**: Configuration with a Hard-coded Network Resource
- **CWE-22**: Path Traversal
- **CWE-78**: OS Command Injection
- **CWE-89**: SQL Injection
- **CWE-94**: Code Injection
- **CWE-200**: Exposure of Sensitive Information
- **CWE-326**: Inadequate Encryption Strength
- **CWE-502**: Deserialization of Untrusted Data
- **CWE-521**: Weak Password Requirements
- **CWE-611**: XXE
- **CWE-639**: IDOR
- **CWE-942**: CORS Misconfiguration

---

## Testing Scenarios

### Quick Tests

```bash
# 1. Information Disclosure
curl http://localhost:8000/api/debug/system-info/

# 2. Weak Authentication
curl "http://localhost:8000/api/debug/weak-auth/?username=admin&password=admin123"

# 3. SQL Injection
curl "http://localhost:8000/api/debug/sql-injection/?user_id=1 OR 1=1"

# 4. Command Injection
curl "http://localhost:8000/api/debug/cmd-injection/?cmd=whoami"

# 5. Access Debug Logs
curl http://localhost:8000/api/debug/get-logs/
```

### Admin Access

```
URL: http://localhost:8000/admin/
Username: admin
Password: admin123
```

### Database Access

```
pgAdmin URL: http://localhost:5050/
Email: admin@example.com
Password: admin123

PostgreSQL:
  Host: db
  Port: 5432
  Username: ecommerce_user
  Password: ecommerce_pass
  Database: ecommerce_db
```

---

## Security Control Assessment

### Disabled/Misconfigured Controls

| Control | Status | Impact |
|---------|--------|--------|
| DEBUG Mode | **ENABLED** | Stack traces expose code/env vars |
| SECRET_KEY | **WEAK** | Predictable, hardcoded |
| ALLOWED_HOSTS | **WILDCARD** | Host header injection possible |
| CORS | **MISCONFIGURED** | Origin spoofing, credential theft |
| Session Cookies | **INSECURE** | No Secure/HttpOnly/SameSite |
| CSRF Protection | **DISABLED** | @csrf_exempt on all endpoints |
| SSL/TLS | **DISABLED** | No SECURE_SSL_REDIRECT |
| HSTS | **DISABLED** | No browser HTTPS enforcement |
| X-Frame-Options | **ALLOW** | Clickjacking possible |
| Input Validation | **NONE** | Direct user input in dangerous functions |
| SQL Queries | **UNPARAMETERIZED** | String concatenation used |
| Subprocess | **shell=True** | Command injection possible |
| Pickle | **ENABLED** | Deserialization attacks possible |
| XML Parsing | **UNSAFE** | XXE attacks possible |
| Path Handling | **NO VALIDATION** | Path traversal possible |
| Logging | **UNRESTRICTED** | Sensitive data logged |

---

## Deployment Options

### Option 1: Local Testing
```bash
docker-compose -f docker-compose.pentesting.yml up -d
```

### Option 2: AWS EC2
```bash
./aws-deploy.sh
```

### Option 3: Manual
```bash
cp .env.pentesting .env
docker-compose -f docker-compose.pentesting.yml up -d
```

---

## Ports Exposed

| Port | Service | Purpose |
|------|---------|---------|
| 8000 | Django App | Web application |
| 5432 | PostgreSQL | Database |
| 6379 | Redis | Cache |
| 5050 | pgAdmin | Database admin |

---

## Sensitive Endpoints

### Admin Panel
- URL: `/admin/`
- Auth: `admin:admin123` (weak)
- Contains: User management, database config

### Debug Endpoints
- Base: `/api/debug/`
- No authentication required
- Intentionally vulnerable

### pgAdmin
- Port: 5050
- Auth: `admin@example.com:admin123` (weak)
- Database access: Full control

---

## Testing Checklist

For authorized penetration testers:

### Reconnaissance
- [ ] Identify all services (port scan)
- [ ] Enumerate running applications
- [ ] Collect version information
- [ ] Find debug endpoints

### Vulnerability Discovery
- [ ] SQL Injection testing
- [ ] Command injection testing
- [ ] Authentication weakness
- [ ] CORS misconfiguration
- [ ] Information disclosure
- [ ] Weak session management

### Exploitation
- [ ] Execute SQL queries
- [ ] Execute system commands
- [ ] Access unauthorized data
- [ ] Bypass authentication
- [ ] Escalate privileges

### Post-Exploitation
- [ ] Maintain persistent access
- [ ] Document findings
- [ ] Create PoC code
- [ ] Assess business impact

---

## Support Files

### Documentation
- `PENTESTING_GUIDE.md` - Detailed vulnerability guide
- `README_PENTESTING.md` - Quick start guide
- `DOCKER_SETUP.md` - Docker documentation
- `VULNERABILITIES_SUMMARY.md` - This file

### Deployment
- `aws-deploy.sh` - AWS deployment script
- `docker-compose.pentesting.yml` - Testing environment
- `.env.pentesting` - Testing configuration

### Application
- `debug_endpoints/` - Vulnerable Django app
- Modified `settings.py` - Insecure configuration

---

## Remediation Steps (For Production)

1. ✅ Set `DEBUG = False`
2. ✅ Use strong `SECRET_KEY`
3. ✅ Configure `ALLOWED_HOSTS` whitelist
4. ✅ Restrict `CORS` origins
5. ✅ Enable secure session cookies
6. ✅ Use `@ensure_csrf_cookie`
7. ✅ Enforce HTTPS
8. ✅ Enable HSTS
9. ✅ Set `X-Frame-Options: DENY`
10. ✅ Remove debug endpoints
11. ✅ Implement input validation
12. ✅ Use parameterized queries
13. ✅ Disable `shell=True` in subprocess
14. ✅ Avoid `pickle.loads()`
15. ✅ Use `defusedxml`
16. ✅ Implement proper logging

---

## Legal Disclaimer

⚠️ **IMPORTANT**:

- This application is intentionally vulnerable for authorized testing only
- Unauthorized access to computer systems is illegal under the Computer Fraud and Abuse Act (CFAA) and equivalent international laws
- User must obtain written authorization before performing any security testing
- User assumes all responsibility for the lawful use of this application

**This is for:**
- ✅ Authorized penetration testing
- ✅ Security training
- ✅ Controlled lab environments
- ✅ Educational purposes

**This is NOT for:**
- ❌ Unauthorized testing
- ❌ Production use
- ❌ Illegal hacking
- ❌ Malicious purposes

---

## References

- [OWASP Top 10 2021](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Django Security Documentation](https://docs.djangoproject.com/en/6.0/topics/security/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)

---

**Created**: 2026-07-18
**Version**: 1.0
**Status**: FOR AUTHORIZED TESTING ONLY

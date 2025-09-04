# ALX Backend Security

This project demonstrates common **security practices in Django** through a series of tasks.  
It includes IP blacklisting, geolocation logging, and rate limiting by IP.

---

## Features

### 1. IP Blacklisting

- Block requests from specific IP addresses.
- Managed via `BlockedIP` model and a custom middleware.
- Includes a management command to add IPs:
  ```bash
  python manage.py block_ip 192.168.1.100 --reason="Suspicious activity"
  ```

### 2. IP Geolocation Analytics

- Logs request details including **country, city, latitude, longitude**.
- Uses a geolocation service (API-based) with caching for performance.
- Skips private/local IP addresses.

### 3. Rate Limiting

- Prevents brute-force and abuse using **django-ratelimit**.
- Limits:
  - **Anonymous users**: 5 requests/minute.
  - **Authenticated users**: 10 requests/minute.
- Applied to sensitive views (e.g., login).

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/alx-backend-security.git
   cd alx-backend-security
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the server:
   ```bash
   python manage.py runserver
   ```

---

## Configuration

- **Middleware**  
  Add to `settings.py`:

  ```python
  MIDDLEWARE = [
      ...
      "ip_tracking.middleware.IPLoggingMiddleware",
  ]
  ```

- **Ratelimit**  
  Make sure `django-ratelimit` is installed and configured.

- **Database**  
  Default: SQLite (for development). Can be swapped with Postgres/MySQL.

---

## Example Flow

1. User makes a request → Middleware checks if IP is blocked.
2. If allowed → Request is logged with IP, path, method, and geolocation.
3. Rate limit applied on sensitive views (e.g., login).

---

## License

MIT License

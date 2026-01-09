# Ansible Role: Monica CRM

Installs and configures the Monica CRM application behind Nginx with PHP-FPM. The role is cross-distro and supports Debian-based and RedHat-based systems.

## Supported platforms
- Debian 12
- Enterprise Linux 8 (Rocky/Alma/CentOS Stream)

Minimum Ansible version: 2.10

## Requirements
- Target host must have network access to clone the Monica repository and install packages.
- A MySQL/MariaDB instance reachable with credentials you provide in `.env` (template included). The role does not provision the database server.
- Docker is required only for running Molecule tests locally.

## Role Variables
Common defaults (see `defaults/main.yml`):

| Variable | Default | Description |
|---|---|---|
| `monica_version` | `"3.10.0"` | Monica upstream version string (currently informational). |
| `monica_db_name` | `"monica"` | DB name used in template `.env`. |
| `nginx_server_name` | `"_"` | Server name in Nginx vhost. |
| `monica_app_env` | `"production"` | Sets `APP_ENV` in `.env` (production or local). |

OS-specific variables are loaded automatically based on distribution and OS family (see files in `vars/`). You normally do not need to change these:

| Variable | Debian example | EL example | Purpose |
|---|---|---|---|
| `monica_packages` | `nginx, php8.2, php8.2-cli, php8.2-fpm, php8.2-mysql, git` | `nginx, php, php-cli, php-fpm, php-mysqlnd, git` | Required packages. |
| `monica_web_group` | `www-data` | `nginx` | Group owning Monica files. |
| `monica_service_name` | `nginx` | `nginx` | Web service to reload. |
| `php_fpm_service` | `php8.2-fpm` | `php-fpm` | PHP-FPM service name. |
| `php_fpm_fastcgi` | `unix:/var/run/php/php8.2-fpm.sock` | `127.0.0.1:9000` | Nginx `fastcgi_pass`. |
| `nginx_site_dest` | `/etc/nginx/sites-enabled/monica.conf` | `/etc/nginx/conf.d/monica.conf` | Where the vhost is installed. |
| `default_nginx_site_path` | `/etc/nginx/sites-enabled/default` | `` (empty) | Default site to remove, if present. |

Notes:
- Service reloads are implemented via handlers (`handlers/main.yml`).
- OS variables are included using a safe mechanism that checks file existence, so distributions like Rocky that don’t have a dedicated file still use family defaults.

## Handlers
- `reload php-fpm`
- `reload nginx`

## Example Playbook
```yaml
- hosts: all
  become: true
  roles:
    - role: ansible-role-monica
```

After applying the role, point your DNS to the server and configure DB credentials in `templates/env.j2` or override with extra vars.

## Molecule
The role ships with Molecule to test on Debian 12 and Rocky Linux 8.

Run locally:
```bash
molecule dependency -s default
molecule test -s default
```

By default, resource-intensive artisan steps are tagged `molecule-notest` and skipped during Molecule runs.

## Dependencies
- `geerlingguy.composer` (installed automatically by Molecule for tests or pull it via Ansible Galaxy in your env)
- `config_encoder_filters` (used in scenarios; see `molecule/default/requirements.yml`)

## License
Apache 2.0

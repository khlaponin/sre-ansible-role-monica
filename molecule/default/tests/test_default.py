import os
import pytest


def test_packages_installed(host):
    os_family = host.system_info.distribution.lower()

    if 'debian' in os_family or 'ubuntu' in os_family:
        pkgs = ['nginx', 'php8.2', 'php8.2-cli', 'php8.2-fpm']
    else:
        # RedHat family (Rocky, Alma, CentOS, etc.)
        pkgs = ['nginx', 'php', 'php-cli', 'php-fpm']

    for pkg in pkgs:
        p = host.package(pkg)
        assert p.is_installed, f"Package {pkg} should be installed"


def test_services_running_and_enabled(host):
    # Web service is nginx on both families in this role
    svc = host.service('nginx')
    assert svc.is_enabled, 'nginx should be enabled'
    # In containers, systemd may be limited; allow running OR listening port
    assert (
        svc.is_running or host.socket('tcp://0.0.0.0:80').is_listening
    ), 'nginx should be running or port 80 should be listening'


@pytest.mark.parametrize('path', [
    '/srv/monicahq',
    '/srv/monicahq/storage',
])
def test_directories_exist(host, path):
    f = host.file(path)
    assert f.exists, f"{path} should exist"
    assert f.is_directory, f"{path} should be a directory"


def test_nginx_site_config_exists(host):
    os_family = host.system_info.distribution.lower()

    if 'debian' in os_family or 'ubuntu' in os_family:
        dest = '/etc/nginx/sites-enabled/monica.conf'
    else:
        dest = '/etc/nginx/conf.d/monica.conf'

    f = host.file(dest)
    assert f.exists, f"nginx vhost config should exist at {dest}"
    assert f.size > 0, 'nginx vhost config should not be empty'

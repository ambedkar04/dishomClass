"""
Tailwind CSS Configuration Verification Script
Checks that all Tailwind components are properly configured
"""

import os
import sys
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def check_file(path, description):
    """Check if a file exists"""
    if Path(path).exists():
        print(f"{Colors.GREEN}✓{Colors.END} {description}: {Colors.BOLD}{path}{Colors.END}")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.END} {description}: {Colors.BOLD}{path}{Colors.END} (NOT FOUND)")
        return False

def check_setting(setting_name):
    """Check if a Django setting exists"""
    try:
        from django.conf import settings
        value = getattr(settings, setting_name, None)
        if value:
            print(f"{Colors.GREEN}✓{Colors.END} Setting {Colors.BOLD}{setting_name}{Colors.END} = {value}")
            return True
        else:
            print(f"{Colors.RED}✗{Colors.END} Setting {Colors.BOLD}{setting_name}{Colors.END} not found")
            return False
    except Exception as e:
        print(f"{Colors.RED}✗{Colors.END} Error checking {setting_name}: {e}")
        return False

def main():
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}Tailwind CSS Configuration Verification{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    checks_passed = 0
    total_checks = 0
    
    # Check Django settings
    print(f"{Colors.YELLOW}Checking Django Settings...{Colors.END}")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dishom.settings')
    import django
    django.setup()
    
    total_checks += 1
    if check_setting('TAILWIND_APP_NAME'):
        checks_passed += 1
    
    total_checks += 1
    if check_setting('INSTALLED_APPS'):
        from django.conf import settings
        if 'tailwind' in settings.INSTALLED_APPS and 'theme' in settings.INSTALLED_APPS:
            print(f"  {Colors.GREEN}✓{Colors.END} 'tailwind' and 'theme' in INSTALLED_APPS")
            checks_passed += 1
        else:
            print(f"  {Colors.RED}✗{Colors.END} 'tailwind' or 'theme' missing from INSTALLED_APPS")
    
    print()
    
    # Check theme files
    print(f"{Colors.YELLOW}Checking Theme Files...{Colors.END}")
    
    files_to_check = [
        ('theme/tailwind.config.js', 'Tailwind Config'),
        ('theme/postcss.config.js', 'PostCSS Config'),
        ('theme/package.json', 'Package.json'),
        ('theme/static_src/src/styles.css', 'Source CSS'),
        ('theme/static/css/styles.css', 'Compiled CSS'),
        ('theme/README.md', 'Theme README'),
    ]
    
    for file_path, description in files_to_check:
        total_checks += 1
        if check_file(file_path, description):
            checks_passed += 1
    
    print()
    
    # Check documentation
    print(f"{Colors.YELLOW}Checking Documentation...{Colors.END}")
    
    docs_to_check = [
        ('TAILWIND_CONFIG.md', 'Configuration Summary'),
        ('DEPLOYMENT.md', 'Deployment Guide'),
        ('deploy.sh', 'Linux Deploy Script'),
        ('deploy.bat', 'Windows Deploy Script'),
    ]
    
    for file_path, description in docs_to_check:
        total_checks += 1
        if check_file(file_path, description):
            checks_passed += 1
    
    print()
    
    # Check CSS file size
    print(f"{Colors.YELLOW}Checking CSS File Size...{Colors.END}")
    css_file = Path('theme/static/css/styles.css')
    if css_file.exists():
        size_kb = css_file.stat().st_size / 1024
        total_checks += 1
        if size_kb < 100:
            print(f"{Colors.GREEN}✓{Colors.END} CSS file size: {Colors.BOLD}{size_kb:.1f} KB{Colors.END} (Optimized)")
            checks_passed += 1
        else:
            print(f"{Colors.YELLOW}⚠{Colors.END} CSS file size: {Colors.BOLD}{size_kb:.1f} KB{Colors.END} (Consider optimization)")
            checks_passed += 1
    
    print()
    
    # Check node_modules
    print(f"{Colors.YELLOW}Checking Node Dependencies...{Colors.END}")
    total_checks += 1
    if Path('theme/node_modules').exists():
        print(f"{Colors.GREEN}✓{Colors.END} Node modules installed")
        checks_passed += 1
    else:
        print(f"{Colors.RED}✗{Colors.END} Node modules not installed (run 'npm install' in theme/)")
    
    print()
    
    # Summary
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}")
    percentage = (checks_passed / total_checks) * 100
    
    if percentage == 100:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All checks passed! ({checks_passed}/{total_checks}){Colors.END}")
        print(f"{Colors.GREEN}Your Tailwind CSS configuration is production-ready!{Colors.END}")
    elif percentage >= 80:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ Most checks passed ({checks_passed}/{total_checks}){Colors.END}")
        print(f"{Colors.YELLOW}Review the failed checks above{Colors.END}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some checks failed ({checks_passed}/{total_checks}){Colors.END}")
        print(f"{Colors.RED}Please fix the issues above{Colors.END}")
    
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.END}\n")
    
    # Next steps
    if percentage == 100:
        print(f"{Colors.BOLD}Next Steps:{Colors.END}")
        print(f"1. Start development: {Colors.BLUE}cd theme && npm run dev{Colors.END}")
        print(f"2. Or use Django: {Colors.BLUE}python manage.py tailwind start{Colors.END}")
        print(f"3. For production: {Colors.BLUE}npm run prod && python manage.py collectstatic{Colors.END}")
        print()
    
    return 0 if percentage == 100 else 1

if __name__ == '__main__':
    sys.exit(main())

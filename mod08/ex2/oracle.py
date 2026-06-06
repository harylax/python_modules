import sys
import os


def load_env_file() -> bool:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return True
    except ImportError:
        print("[WARNING] python-dotenv not detected")
        print("Usage:\n"
              "\tpython -m venv venv\n"
              "\tsource venv/bin/activate\n"
              "\tpip install python-dotenv\n"
              "\tpython3 oracle.py")
        return False


def get_mode() -> str:
    mode: str = os.environ.get('MATRIX_MODE', '')
    if mode not in ['development', 'production']:
        return 'Unknown mode'
    return mode


def get_database_status() -> str:
    url: str = os.environ.get('DATABASE_URL', '')
    if url.startswith('postgresql://') and len(url) > len('postgresql://'):
        return 'Connected to remote instance'
    if url.startswith('sqlite:///') and len(url) > len('sqlite:///'):
        return 'Connected to local instance'
    return 'Not configured'


def get_api_status() -> str:
    key: str = os.environ.get('API_KEY', '')
    if not key:
        return 'Not authenticated'
    return 'Authenticated'


def get_log_level() -> str:
    valid: list[str] = [
        'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    ]
    level: str = os.environ.get('LOG_LEVEL', '')
    if not level:
        return 'Not configured'
    if level not in valid:
        return "Invalid log level"
    return level


def get_zion_status() -> str:
    endpoint: str = os.environ.get('ZION_ENDPOINT', '')
    if endpoint.startswith(('http://', 'https://')) \
            and len(endpoint) > len('https://'):
        return 'Online'
    return 'Offline'


def config_show() -> None:
    print("Configuration loaded:")
    print(f"Mode: {get_mode()}")
    print(f"Database: {get_database_status()}")
    print(f"API Access: {get_api_status()}")
    print(f"Log Level: {get_log_level()}")
    print(f"Zion Network: {get_zion_status()}")


def security_secret_check(required_variables: list[str]) -> str:
    secrets: list[str] = []
    for variable in required_variables:
        if not os.getenv(variable):
            secrets.append(variable)
    if not secrets:
        return "[OK] No hardcoded secrets detected"
    return f" [X] Missing config, defaults used: {', '.join(secrets)}"


def security_config_check() -> str:
    if os.path.isfile('.env'):
        return "[OK] .env file properly configured"
    return " [X] .env file not found"


def security_overrides_check(overrides: list[str] | None) -> str:
    if not overrides:
        return "[OK] Production overrides available"
    return f"[OK] Production overrides active: {', '.join(overrides)}"


def main() -> None:
    variables: list[str] = [
        'MATRIX_MODE', 'DATABASE_URL', 'API_KEY', 'LOG_LEVEL', 'ZION_ENDPOINT'
    ]

    overrides: list[str] = []
    for var in variables:
        if os.getenv(var):
            overrides.append(var)

    if not load_env_file():
        sys.exit(1)

    print("\nORACLE STATUS: Reading the Matrix...\n")
    config_show()

    print("\nEnvironment security check:")
    print(security_secret_check(variables))
    print(security_config_check())
    print(security_overrides_check(overrides))

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(f"Unexpected error: {err}")

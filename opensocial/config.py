class ConfigAPI:
    database = "sqlite:///opensocial.db"
    server = {
        "host": '127.0.0.1',
        'port': 8000,
        'debug': True
    }
    secret_key = "testkey"
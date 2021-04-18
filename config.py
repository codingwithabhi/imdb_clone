def get_config():
    return {
        "PORT": 5000,
        "DEBUG": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///imdb.sqlite3",
        "SECRET": "Kisi_ko_batana_nhi",
        "SALT": "secure"
    }

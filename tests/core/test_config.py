import os

from app.core.config import Settings


def test_normalize_database_dialect(mocker):
    mocker.patch.dict(os.environ, {'DATABASE_URL': 'postgres://'})
    settings = Settings()
    assert settings.DATABASE_URL == 'postgresql://'

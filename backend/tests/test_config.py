"""Test configuration validation"""
import pytest
import os
from unittest.mock import patch
from app.config import Settings, validate_storage_config


pytestmark = pytest.mark.unit


def test_local_storage_config_valid():
    """Test local storage config is valid with minimal settings"""
    with patch.dict(os.environ, {"STORAGE_BACKEND": "local"}, clear=True):
        settings = Settings()
        # Should not raise
        validate_storage_config("local", settings)


def test_qdrant_neo4j_config_missing_params():
    """Test qdrant_neo4j config validation fails when params missing"""
    with patch.dict(os.environ, {"STORAGE_BACKEND": "qdrant_neo4j"}, clear=True):
        settings = Settings()

        with pytest.raises(ValueError, match="requires"):
            validate_storage_config("qdrant_neo4j", settings)


def test_qdrant_neo4j_config_valid():
    """Test qdrant_neo4j config is valid with all params"""
    with patch.dict(
        os.environ,
        {
            "STORAGE_BACKEND": "qdrant_neo4j",
            "QDRANT_URL": "http://localhost:6333",
            "NEO4J_URI": "bolt://localhost:7687",
            "NEO4J_USER": "neo4j",
            "NEO4J_PASSWORD": "password",
        },
        clear=True,
    ):
        settings = Settings()
        # Should not raise
        validate_storage_config("qdrant_neo4j", settings)

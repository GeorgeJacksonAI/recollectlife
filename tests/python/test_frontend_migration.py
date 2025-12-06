"""
Integration tests for frontend migration and backend API
Tests the complete system integration after frontend migration
"""

import json
import os
import subprocess
import time
from pathlib import Path

import pytest
import requests

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8080"
PROJECT_ROOT = Path(
    __file__
).parent.parent.parent  # tests/python/test_frontend_migration.py -> project root


class TestBackendAPI:
    """Test backend API endpoints"""

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data

    def test_create_message(self):
        """Test creating a message via POST"""
        payload = {"role": "user", "content": "Test message from pytest"}
        response = requests.post(
            f"{BASE_URL}/api/messages/",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["role"] == "user"
        assert data["content"] == "Test message from pytest"

    def test_list_messages(self):
        """Test listing messages via GET"""
        response = requests.get(f"{BASE_URL}/api/messages/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "id" in data[0]
            assert "role" in data[0]
            assert "content" in data[0]
            assert "created_at" in data[0]

    def test_list_messages_pagination(self):
        """Test message pagination"""
        response = requests.get(f"{BASE_URL}/api/messages/?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2

    def test_cors_headers(self):
        """Test CORS configuration"""
        response = requests.options(
            f"{BASE_URL}/api/messages/",
            headers={
                "Origin": "http://localhost:8080",
                "Access-Control-Request-Method": "POST",
            },
        )
        # Should allow the origin
        assert response.status_code in [200, 204]


class TestFrontendStructure:
    """Test frontend directory structure and configuration"""

    def test_frontend_directory_exists(self):
        """Test that frontend directory exists"""
        frontend_dir = PROJECT_ROOT / "frontend"
        assert frontend_dir.exists()
        assert frontend_dir.is_dir()

    def test_frontend_package_json_exists(self):
        """Test package.json exists"""
        package_json = PROJECT_ROOT / "frontend" / "package.json"
        assert package_json.exists()

    def test_frontend_env_files_exist(self):
        """Test environment files exist"""
        env_example = PROJECT_ROOT / "frontend" / ".env.example"
        env_file = PROJECT_ROOT / "frontend" / ".env"
        assert env_example.exists()
        assert env_file.exists()

    def test_frontend_env_config(self):
        """Test .env file has correct API URL"""
        env_file = PROJECT_ROOT / "frontend" / ".env"
        content = env_file.read_text()
        assert "VITE_API_URL" in content
        assert "8000" in content  # Backend port

    def test_api_integration_layer_exists(self):
        """Test API integration layer file exists"""
        api_file = PROJECT_ROOT / "frontend" / "src" / "lib" / "api.js"
        assert api_file.exists()
        content = api_file.read_text()
        assert "apiService" in content
        assert "messages" in content
        assert "health" in content

    def test_index_html_references_correct_file(self):
        """Test index.html references main.jsx not main.tsx"""
        index_html = PROJECT_ROOT / "frontend" / "index.html"
        content = index_html.read_text()
        assert "/src/main.jsx" in content
        assert "/src/main.tsx" not in content

    def test_tailwind_config_correct(self):
        """Test TailwindCSS is configured correctly"""
        postcss_config = PROJECT_ROOT / "frontend" / "postcss.config.js"
        assert postcss_config.exists()
        content = postcss_config.read_text()
        assert "tailwindcss" in content
        assert "autoprefixer" in content

    def test_index_css_uses_correct_syntax(self):
        """Test index.css uses Tailwind v3 syntax"""
        index_css = PROJECT_ROOT / "frontend" / "src" / "index.css"
        content = index_css.read_text()
        assert "@tailwind base" in content
        assert "@tailwind components" in content
        assert "@tailwind utilities" in content
        # Should NOT have v4 syntax
        assert '@import "tailwindcss"' not in content


class TestDockerConfiguration:
    """Test Docker and docker-compose configuration"""

    def test_docker_compose_file_exists(self):
        """Test docker-compose.yml exists"""
        docker_compose = PROJECT_ROOT / "docker-compose.yml"
        assert docker_compose.exists()

    def test_docker_compose_has_frontend_service(self):
        """Test docker-compose has frontend service defined"""
        docker_compose = PROJECT_ROOT / "docker-compose.yml"
        content = docker_compose.read_text()
        assert "frontend:" in content
        assert "8080:8080" in content

    def test_docker_compose_has_correct_network(self):
        """Test docker-compose uses app-network"""
        docker_compose = PROJECT_ROOT / "docker-compose.yml"
        content = docker_compose.read_text()
        assert "app-network" in content

    def test_backend_service_running(self):
        """Test backend Docker service is running"""
        result = subprocess.run(
            ["sudo", "docker-compose", "ps", "backend"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert "Up" in result.stdout

    def test_redis_service_running(self):
        """Test Redis service is running"""
        result = subprocess.run(
            ["sudo", "docker-compose", "ps", "redis"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert "Up" in result.stdout


class TestBackendCode:
    """Test backend code changes"""

    def test_cors_origins_updated(self):
        """Test CORS origins include port 8080"""
        main_py = PROJECT_ROOT / "backend" / "app" / "main.py"
        content = main_py.read_text()
        assert "8080" in content
        assert "origins" in content

    def test_message_response_model_exists(self):
        """Test MessageResponse model is defined"""
        messages_py = (
            PROJECT_ROOT / "backend" / "app" / "api" / "endpoints" / "messages.py"
        )
        content = messages_py.read_text()
        assert "MessageResponse" in content
        assert "orm_mode = True" in content or "from_attributes = True" in content

    def test_init_db_script_exists(self):
        """Test database initialization script exists"""
        init_db = PROJECT_ROOT / "scripts" / "init_db.py"
        assert init_db.exists()
        content = init_db.read_text()
        assert "init_db" in content
        assert "create_all" in content


class TestFrontendBuild:
    """Test frontend build process"""

    def test_frontend_build_succeeds(self):
        """Test that frontend builds without errors"""
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=PROJECT_ROOT / "frontend",
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert result.returncode == 0
        assert (
            "error" not in result.stderr.lower() or "0 error" in result.stderr.lower()
        )

    def test_build_output_exists(self):
        """Test that build creates dist directory"""
        dist_dir = PROJECT_ROOT / "frontend" / "dist"
        assert dist_dir.exists()
        index_html = dist_dir / "index.html"
        assert index_html.exists()


class TestDatabaseInitialization:
    """Test database initialization"""

    def test_messages_table_exists(self):
        """Test messages table exists by trying to insert"""
        # This is tested indirectly through create_message test
        # If table doesn't exist, the POST would fail
        payload = {"role": "system", "content": "Database test"}
        response = requests.post(f"{BASE_URL}/api/messages/", json=payload)
        assert response.status_code == 200


class TestEndToEndIntegration:
    """End-to-end integration tests"""

    def test_full_message_lifecycle(self):
        """Test complete message creation and retrieval"""
        # Create a unique message
        test_content = f"E2E test message {time.time()}"
        create_payload = {"role": "user", "content": test_content}

        # Create message
        create_response = requests.post(
            f"{BASE_URL}/api/messages/", json=create_payload
        )
        assert create_response.status_code == 200
        created_message = create_response.json()
        message_id = created_message["id"]

        # List messages and verify it exists
        list_response = requests.get(f"{BASE_URL}/api/messages/")
        assert list_response.status_code == 200
        messages = list_response.json()

        # Find our message
        found = any(msg["id"] == message_id for msg in messages)
        assert found, f"Message {message_id} not found in list"

    def test_api_service_layer_structure(self):
        """Test that API service layer is properly structured"""
        api_file = PROJECT_ROOT / "frontend" / "src" / "lib" / "api.js"
        content = api_file.read_text()

        # Check for required API sections
        assert "apiService" in content
        assert "health" in content
        assert "messages" in content
        assert "stories" in content  # Even if not implemented
        assert "auth" in content  # Even if not implemented

        # Check for proper structure
        assert "list:" in content
        assert "create:" in content
        assert "console.warn" in content  # For unimplemented features


class TestMigrationCleanup:
    """Test that migration was clean"""

    def test_migrations_directory_removed(self):
        """Test that migrations directory was removed"""
        migrations_dir = PROJECT_ROOT / "migrations"
        assert not migrations_dir.exists()

    def test_no_duplicate_vite_configs(self):
        """Test that only one vite config exists"""
        vite_js = PROJECT_ROOT / "frontend" / "vite.config.js"
        vite_ts = PROJECT_ROOT / "frontend" / "vite.config.ts"

        # Should have .ts, not .js
        assert not vite_js.exists()
        assert vite_ts.exists()

    def test_readme_files_organized(self):
        """Test README files are properly organized"""
        readme = PROJECT_ROOT / "frontend" / "README.md"
        readme_lovable = PROJECT_ROOT / "frontend" / "README.lovable.md"

        assert readme.exists()
        assert readme_lovable.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

"""
Basic tests for the Field Hockey Broadcasting Platform
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "🏑 Field Hockey Broadcasting Platform"

def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "field-hockey-broadcasting-platform"

def test_docs_endpoint():
    """Test that the docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200

def test_streams_list_endpoint():
    """Test the streams list endpoint."""
    response = client.get("/api/v1/streams/list")
    assert response.status_code == 200
    data = response.json()
    assert "streams" in data
    assert "page" in data
    assert "limit" in data

def test_auth_endpoints():
    """Test authentication endpoints."""
    # Test login endpoint
    response = client.post("/api/v1/auth/login")
    assert response.status_code == 422  # Missing required fields
    
    # Test register endpoint
    response = client.post("/api/v1/auth/register")
    assert response.status_code == 422  # Missing required fields

if __name__ == "__main__":
    # Run basic tests
    test_root_endpoint()
    test_health_endpoint()
    test_docs_endpoint()
    test_streams_list_endpoint()
    test_auth_endpoints()
    print("✅ All basic tests passed!") 
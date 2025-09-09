import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    """Test the hello endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Hello, World!'

def test_health_endpoint(client):
    """Test the health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'memory_usage' in data
    assert 'cpu_usage' in data

def test_cpu_intensive_endpoint(client):
    """Test the CPU intensive endpoint"""
    response = client.get('/cpu-intensive')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'execution_time' in data
    assert 'cpu_usage' in data

def test_parallel_task_endpoint(client):
    """Test the parallel task endpoint"""
    response = client.get('/parallel-task')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'results' in data
    assert 'execution_time' in data
    assert len(data['results']) == 4

def test_memory_test_endpoint(client):
    """Test the memory test endpoint"""
    response = client.get('/memory-test')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'items_created' in data
    assert 'execution_time' in data
    assert 'memory_usage' in data

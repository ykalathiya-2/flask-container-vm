from flask import Flask, jsonify, request
import time
import os
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor
import json
import logging
from datetime import datetime

# Configure logging for ELK Stack
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple metrics storage (in production, use Prometheus)
metrics = {
    'request_count': 0,
    'total_response_time': 0,
    'error_count': 0
}

@app.before_request
def log_request():
    """Log each request for ELK Stack"""
    request.start_time = time.time()
    metrics['request_count'] += 1
    logger.info(f"Request started: {request.method} {request.path}")

@app.after_request
def log_response(response):
    """Log response and update metrics"""
    if hasattr(request, 'start_time'):
        response_time = time.time() - request.start_time
        metrics['total_response_time'] += response_time
        
        # Log structured data for ELK Stack
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': 'INFO',
            'message': 'Request completed',
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'response_time': response_time,
            'user_agent': request.headers.get('User-Agent', 'Unknown')
        }
        logger.info(json.dumps(log_data))
    
    return response

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello, World!',
        'timestamp': time.time(),
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'memory_usage': psutil.virtual_memory().percent,
        'cpu_usage': psutil.cpu_percent(),
        'timestamp': time.time()
    })

@app.route('/cpu')
def cpu_intensive():
    """CPU intensive task for benchmarking"""
    start_time = time.time()
    result = 0
    for i in range(1000000):
        result += i * i
    end_time = time.time()
    
    execution_time = end_time - start_time
    logger.info(f"CPU task completed in {execution_time:.3f} seconds")
    
    return jsonify({
        'result': result,
        'execution_time': execution_time,
        'cpu_usage': psutil.cpu_percent(),
        'timestamp': time.time()
    })

@app.route('/memory')
def memory_test():
    """Memory intensive task for benchmarking"""
    start_time = time.time()
    data = []
    for i in range(100000):
        data.append({'id': i, 'value': 'x' * 100})
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    logger.info(f"Memory task completed in {execution_time:.3f} seconds")
    
    return jsonify({
        'items_created': len(data),
        'execution_time': execution_time,
        'memory_usage': psutil.virtual_memory().percent,
        'timestamp': time.time()
    })

@app.route('/parallel')
def parallel_task():
    """Parallel processing task for benchmarking"""
    start_time = time.time()
    
    def worker_task(n):
        result = 0
        for i in range(n):
            result += i * i
        return result
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(worker_task, 100000) for _ in range(4)]
        results = [future.result() for future in futures]
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    logger.info(f"Parallel task completed in {execution_time:.3f} seconds")
    
    return jsonify({
        'results': results,
        'execution_time': execution_time,
        'cpu_usage': psutil.cpu_percent(),
        'timestamp': time.time()
    })

@app.route('/metrics')
def prometheus_metrics():
    """Prometheus-compatible metrics endpoint"""
    avg_response_time = 0
    if metrics['request_count'] > 0:
        avg_response_time = metrics['total_response_time'] / metrics['request_count']
    
    # Prometheus format
    metrics_text = f"""# HELP flask_requests_total Total number of requests
# TYPE flask_requests_total counter
flask_requests_total {metrics['request_count']}

# HELP flask_errors_total Total number of errors
# TYPE flask_errors_total counter
flask_errors_total {metrics['error_count']}

# HELP flask_response_time_seconds Average response time
# TYPE flask_response_time_seconds gauge
flask_response_time_seconds {avg_response_time}

# HELP flask_memory_usage_percent Memory usage percentage
# TYPE flask_memory_usage_percent gauge
flask_memory_usage_percent {psutil.virtual_memory().percent}

# HELP flask_cpu_usage_percent CPU usage percentage
# TYPE flask_cpu_usage_percent gauge
flask_cpu_usage_percent {psutil.cpu_percent()}
"""
    
    return metrics_text, 200, {'Content-Type': 'text/plain'}

@app.route('/status')
def status():
    """Detailed status endpoint for monitoring"""
    return jsonify({
        'status': 'running',
        'uptime': time.time() - app.start_time if hasattr(app, 'start_time') else 0,
        'memory': {
            'total': psutil.virtual_memory().total,
            'available': psutil.virtual_memory().available,
            'percent': psutil.virtual_memory().percent
        },
        'cpu': {
            'count': psutil.cpu_count(),
            'percent': psutil.cpu_percent()
        },
        'metrics': metrics,
        'timestamp': time.time()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    metrics['error_count'] += 1
    logger.error(f"404 error: {request.path}")
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    metrics['error_count'] += 1
    logger.error(f"500 error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.start_time = time.time()
    logger.info("Flask application starting...")
    app.run(host='0.0.0.0', port=5000, debug=False)
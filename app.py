from flask import Flask, jsonify, request
import time
import os
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello, World!',
        'timestamp': time.time(),
        'environment': os.environ.get('ENVIRONMENT', 'development')
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'memory_usage': psutil.virtual_memory().percent,
        'cpu_usage': psutil.cpu_percent()
    })

@app.route('/cpu-intensive')
def cpu_intensive():
    """CPU intensive task for benchmarking"""
    start_time = time.time()
    result = 0
    for i in range(1000000):
        result += i * i
    end_time = time.time()
    
    return jsonify({
        'result': result,
        'execution_time': end_time - start_time,
        'cpu_usage': psutil.cpu_percent()
    })

@app.route('/parallel-task')
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
    
    return jsonify({
        'results': results,
        'execution_time': end_time - start_time,
        'cpu_usage': psutil.cpu_percent()
    })

@app.route('/memory-test')
def memory_test():
    """Memory intensive task for benchmarking"""
    start_time = time.time()
    data = []
    for i in range(100000):
        data.append({'id': i, 'value': 'x' * 100})
    
    end_time = time.time()
    
    return jsonify({
        'items_created': len(data),
        'execution_time': end_time - start_time,
        'memory_usage': psutil.virtual_memory().percent
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

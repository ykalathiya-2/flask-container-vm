#!/usr/bin/env python3
"""
Performance benchmarking script for VM vs Container comparison
"""

import time
import requests
import psutil
import subprocess
import json
import statistics
from concurrent.futures import ThreadPoolExecutor
import argparse

class BenchmarkRunner:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.results = {}

    def measure_startup_time(self):
        """Measure application startup time"""
        print("Measuring startup time...")
        start_time = time.time()
        
        # Try to connect to the service
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                response = requests.get(f"{self.base_url}/health", timeout=1)
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                time.sleep(1)
        
        end_time = time.time()
        startup_time = end_time - start_time
        
        self.results['startup_time'] = startup_time
        print(f"Startup time: {startup_time:.2f} seconds")
        return startup_time

    def measure_memory_usage(self):
        """Measure memory usage during idle state"""
        print("Measuring memory usage...")
        
        # Get memory usage from the application
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                memory_usage = data.get('memory_usage', 0)
            else:
                memory_usage = 0
        except requests.exceptions.RequestException:
            memory_usage = 0
        
        self.results['memory_usage_idle'] = memory_usage
        print(f"Memory usage (idle): {memory_usage}%")
        return memory_usage

    def measure_cpu_utilization(self):
        """Measure CPU utilization under load"""
        print("Measuring CPU utilization...")
        
        # Get baseline CPU usage
        baseline_cpu = psutil.cpu_percent(interval=1)
        
        # Run CPU intensive task and measure
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/cpu-intensive", timeout=30)
            if response.status_code == 200:
                data = response.json()
                execution_time = data.get('execution_time', 0)
                app_cpu_usage = data.get('cpu_usage', 0)
            else:
                execution_time = 0
                app_cpu_usage = 0
        except requests.exceptions.RequestException:
            execution_time = 0
            app_cpu_usage = 0
        
        end_time = time.time()
        total_time = end_time - start_time
        
        self.results['cpu_execution_time'] = execution_time
        self.results['cpu_usage_under_load'] = app_cpu_usage
        self.results['total_cpu_time'] = total_time
        print(f"CPU execution time: {execution_time:.2f} seconds")
        print(f"CPU usage under load: {app_cpu_usage}%")
        return execution_time, app_cpu_usage

    def measure_throughput(self, num_requests=100, concurrency=10):
        """Measure throughput and response times"""
        print(f"Measuring throughput with {num_requests} requests, concurrency {concurrency}...")
        
        def make_request():
            start = time.time()
            try:
                response = requests.get(f"{self.base_url}/", timeout=10)
                end = time.time()
                return {
                    'status_code': response.status_code,
                    'response_time': end - start,
                    'success': response.status_code == 200
                }
            except requests.exceptions.RequestException as e:
                end = time.time()
                return {
                    'status_code': 0,
                    'response_time': end - start,
                    'success': False,
                    'error': str(e)
                }
        
        # Run concurrent requests
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in futures]
        end_time = time.time()
        
        # Calculate metrics
        total_time = end_time - start_time
        successful_requests = [r for r in results if r['success']]
        response_times = [r['response_time'] for r in successful_requests]
        
        throughput = len(successful_requests) / total_time
        avg_response_time = statistics.mean(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        success_rate = len(successful_requests) / num_requests * 100
        
        self.results['throughput_rps'] = throughput
        self.results['avg_response_time'] = avg_response_time
        self.results['min_response_time'] = min_response_time
        self.results['max_response_time'] = max_response_time
        self.results['success_rate'] = success_rate
        self.results['total_requests'] = num_requests
        self.results['successful_requests'] = len(successful_requests)
        
        print(f"Throughput: {throughput:.2f} requests/second")
        print(f"Average response time: {avg_response_time:.3f} seconds")
        print(f"Success rate: {success_rate:.1f}%")
        
        return throughput, avg_response_time, success_rate

    def measure_parallel_processing(self):
        """Measure parallel processing performance"""
        print("Measuring parallel processing performance...")
        
        try:
            response = requests.get(f"{self.base_url}/parallel-task", timeout=30)
            if response.status_code == 200:
                data = response.json()
                execution_time = data.get('execution_time', 0)
                cpu_usage = data.get('cpu_usage', 0)
            else:
                execution_time = 0
                cpu_usage = 0
        except requests.exceptions.RequestException:
            execution_time = 0
            cpu_usage = 0
        
        self.results['parallel_execution_time'] = execution_time
        self.results['parallel_cpu_usage'] = cpu_usage
        print(f"Parallel execution time: {execution_time:.2f} seconds")
        print(f"Parallel CPU usage: {cpu_usage}%")
        return execution_time, cpu_usage

    def measure_memory_intensive(self):
        """Measure memory intensive task performance"""
        print("Measuring memory intensive task...")
        
        try:
            response = requests.get(f"{self.base_url}/memory-test", timeout=30)
            if response.status_code == 200:
                data = response.json()
                execution_time = data.get('execution_time', 0)
                memory_usage = data.get('memory_usage', 0)
                items_created = data.get('items_created', 0)
            else:
                execution_time = 0
                memory_usage = 0
                items_created = 0
        except requests.exceptions.RequestException:
            execution_time = 0
            memory_usage = 0
            items_created = 0
        
        self.results['memory_execution_time'] = execution_time
        self.results['memory_usage_peak'] = memory_usage
        self.results['memory_items_created'] = items_created
        print(f"Memory execution time: {execution_time:.2f} seconds")
        print(f"Peak memory usage: {memory_usage}%")
        print(f"Items created: {items_created}")
        return execution_time, memory_usage, items_created

    def run_full_benchmark(self, num_requests=100, concurrency=10):
        """Run complete benchmark suite"""
        print(f"Starting full benchmark for {self.base_url}")
        print("=" * 50)
        
        # Wait for service to be ready
        self.measure_startup_time()
        
        # Run all tests
        self.measure_memory_usage()
        self.measure_cpu_utilization()
        self.measure_throughput(num_requests, concurrency)
        self.measure_parallel_processing()
        self.measure_memory_intensive()
        
        print("=" * 50)
        print("Benchmark completed!")
        return self.results

    def save_results(self, filename):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Benchmark Flask application')
    parser.add_argument('--url', default='http://localhost:5000', help='Base URL of the application')
    parser.add_argument('--requests', type=int, default=100, help='Number of requests for throughput test')
    parser.add_argument('--concurrency', type=int, default=10, help='Concurrency level for throughput test')
    parser.add_argument('--output', default='benchmark_results.json', help='Output file for results')
    
    args = parser.parse_args()
    
    benchmark = BenchmarkRunner(args.url)
    results = benchmark.run_full_benchmark(args.requests, args.concurrency)
    benchmark.save_results(args.output)
    
    return results

if __name__ == '__main__':
    main()

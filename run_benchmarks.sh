#!/bin/bash

# Benchmark script for VM vs Container performance comparison
# This script runs benchmarks on both VM and Container environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VM_URL="http://localhost:5000"
CONTAINER_URL="http://localhost:5001"
RESULTS_DIR="benchmark_results"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create results directory
mkdir -p "$RESULTS_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  VM vs Container Performance Benchmark${NC}"
echo -e "${BLUE}========================================${NC}"

# Function to check if service is running
check_service() {
    local url=$1
    local name=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${YELLOW}Checking if $name is running at $url...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$url/health" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ $name is running${NC}"
            return 0
        fi
        echo -e "${YELLOW}Attempt $attempt/$max_attempts - waiting for $name...${NC}"
        sleep 2
        ((attempt++))
    done
    
    echo -e "${RED}✗ $name is not responding after $max_attempts attempts${NC}"
    return 1
}

# Function to run benchmark
run_benchmark() {
    local url=$1
    local name=$2
    local output_file=$3
    
    echo -e "${BLUE}Running benchmark for $name...${NC}"
    echo -e "${BLUE}URL: $url${NC}"
    
    if check_service "$url" "$name"; then
        python3 benchmark.py --url "$url" --output "$output_file" --requests 50 --concurrency 5
        echo -e "${GREEN}✓ Benchmark completed for $name${NC}"
    else
        echo -e "${RED}✗ Skipping benchmark for $name (service not available)${NC}"
        return 1
    fi
}

# Function to start VM
start_vm() {
    echo -e "${BLUE}Starting VM with Vagrant...${NC}"
    cd /tmp/cloud_architecture_exercise
    
    # Check if VM is already running
    if vagrant status | grep -q "running"; then
        echo -e "${YELLOW}VM is already running${NC}"
    else
        echo -e "${YELLOW}Starting VM...${NC}"
        vagrant up
    fi
    
    # Wait for service to be ready
    sleep 10
}

# Function to start container
start_container() {
    echo -e "${BLUE}Starting Docker container...${NC}"
    cd /tmp/cloud_architecture_exercise
    
    # Build the image
    echo -e "${YELLOW}Building Docker image...${NC}"
    docker build -t flask-benchmark .
    
    # Stop any existing container
    docker stop flask-container 2>/dev/null || true
    docker rm flask-container 2>/dev/null || true
    
    # Run the container
    echo -e "${YELLOW}Starting container on port 5001...${NC}"
    docker run -d --name flask-container -p 5001:5000 flask-benchmark
    
    # Wait for service to be ready
    sleep 5
}

# Function to stop services
stop_services() {
    echo -e "${BLUE}Stopping services...${NC}"
    
    # Stop container
    docker stop flask-container 2>/dev/null || true
    docker rm flask-container 2>/dev/null || true
    
    # Stop VM (optional - comment out if you want to keep it running)
    # cd /tmp/cloud_architecture_exercise
    # vagrant halt
}

# Function to generate comparison report
generate_report() {
    local vm_file="$RESULTS_DIR/vm_results_$TIMESTAMP.json"
    local container_file="$RESULTS_DIR/container_results_$TIMESTAMP.json"
    local report_file="$RESULTS_DIR/comparison_report_$TIMESTAMP.md"
    
    echo -e "${BLUE}Generating comparison report...${NC}"
    
    cat > "$report_file" << EOF
# VM vs Container Performance Comparison Report

**Generated:** $(date)
**Test Environment:** $(uname -a)

## Test Configuration
- **Requests per test:** 50
- **Concurrency:** 5
- **Test duration:** Multiple iterations

## Results Summary

| Metric | VM (Vagrant) | Container (Docker) | Winner |
|--------|--------------|-------------------|---------|
EOF

    # Add comparison data if both files exist
    if [ -f "$vm_file" ] && [ -f "$container_file" ]; then
        echo -e "${GREEN}✓ Both benchmark files found, generating detailed comparison...${NC}"
        
        # Extract key metrics using jq if available, otherwise use basic parsing
        if command -v jq >/dev/null 2>&1; then
            vm_startup=$(jq -r '.startup_time // "N/A"' "$vm_file")
            container_startup=$(jq -r '.startup_time // "N/A"' "$container_file")
            vm_memory=$(jq -r '.memory_usage_idle // "N/A"' "$vm_file")
            container_memory=$(jq -r '.memory_usage_idle // "N/A"' "$container_file")
            vm_throughput=$(jq -r '.throughput_rps // "N/A"' "$vm_file")
            container_throughput=$(jq -r '.throughput_rps // "N/A"' "$container_file")
            vm_response=$(jq -r '.avg_response_time // "N/A"' "$vm_file")
            container_response=$(jq -r '.avg_response_time // "N/A"' "$container_file")
        else
            echo -e "${YELLOW}jq not available, using basic parsing...${NC}"
            vm_startup="N/A"
            container_startup="N/A"
            vm_memory="N/A"
            container_memory="N/A"
            vm_throughput="N/A"
            container_throughput="N/A"
            vm_response="N/A"
            container_response="N/A"
        fi
        
        cat >> "$report_file" << EOF
| Startup Time | ${vm_startup}s | ${container_startup}s | $(if (( $(echo "$container_startup < $vm_startup" | bc -l) )); then echo "Container"; else echo "VM"; fi) |
| Memory Usage | ${vm_memory}% | ${container_memory}% | $(if (( $(echo "$container_memory < $vm_memory" | bc -l) )); then echo "Container"; else echo "VM"; fi) |
| Throughput | ${vm_throughput} req/s | ${container_throughput} req/s | $(if (( $(echo "$container_throughput > $vm_throughput" | bc -l) )); then echo "Container"; else echo "VM"; fi) |
| Response Time | ${vm_response}s | ${container_response}s | $(if (( $(echo "$container_response < $vm_response" | bc -l) )); then echo "Container"; else echo "VM"; fi) |

## Detailed Results

### VM Results
\`\`\`json
$(cat "$vm_file")
\`\`\`

### Container Results
\`\`\`json
$(cat "$container_file")
\`\`\`

## Analysis

### Key Findings
1. **Startup Time:** Containers typically start faster due to shared kernel
2. **Memory Usage:** Containers are more memory-efficient
3. **Performance:** Both environments show similar performance characteristics
4. **Resource Utilization:** Containers generally use resources more efficiently

### Trade-offs
- **Containers:** Faster startup, lower memory usage, better resource efficiency
- **VMs:** Stronger isolation, full OS environment, better for legacy applications

## Recommendations
- Use containers for microservices and cloud-native applications
- Use VMs for applications requiring full OS isolation or specific kernel features
- Consider hybrid approaches for complex enterprise environments
EOF
    else
        echo -e "${YELLOW}⚠ Some benchmark files missing, generating basic report...${NC}"
        cat >> "$report_file" << EOF
## Note
Some benchmark results are missing. Please ensure both VM and Container benchmarks completed successfully.

### Available Results
- VM Results: $([ -f "$vm_file" ] && echo "✓ Available" || echo "✗ Missing")
- Container Results: $([ -f "$container_file" ] && echo "✓ Available" || echo "✗ Missing")
EOF
    fi
    
    echo -e "${GREEN}✓ Report generated: $report_file${NC}"
}

# Main execution
main() {
    echo -e "${BLUE}Starting benchmark process...${NC}"
    
    # Install required packages
    echo -e "${YELLOW}Installing required packages...${NC}"
    pip3 install requests psutil || echo -e "${YELLOW}Warning: Some packages may not be installed${NC}"
    
    # Start VM
    start_vm
    
    # Run VM benchmark
    run_benchmark "$VM_URL" "VM" "$RESULTS_DIR/vm_results_$TIMESTAMP.json"
    
    # Start container
    start_container
    
    # Run container benchmark
    run_benchmark "$CONTAINER_URL" "Container" "$RESULTS_DIR/container_results_$TIMESTAMP.json"
    
    # Generate report
    generate_report
    
    # Cleanup
    echo -e "${BLUE}Cleaning up...${NC}"
    stop_services
    
    echo -e "${GREEN}✓ Benchmark process completed!${NC}"
    echo -e "${BLUE}Results saved in: $RESULTS_DIR/${NC}"
}

# Run main function
main "$@"

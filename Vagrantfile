# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Use Ubuntu 20.04 LTS
  config.vm.box = "ubuntu/focal64"
  
  # Configure VM resources
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 2
  end

  # Port forwarding
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # Provision the VM
  config.vm.provision "shell", inline: <<-SHELL
    # Update system
    apt-get update
    apt-get upgrade -y

    # Install Python and pip
    apt-get install -y python3 python3-pip python3-venv curl

    # Install system dependencies
    apt-get install -y gcc

    # Create application directory
    mkdir -p /app
    cd /app

    # Copy application files (this will be done by the provisioning script)
    # The actual files will be copied by the sync_folder or by the provisioning script

    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install Python dependencies
    pip install --upgrade pip
    pip install -r requirements.txt

    # Set environment variable
    echo 'export ENVIRONMENT=vm' >> /etc/environment

    # Create systemd service for the Flask app
    cat > /etc/systemd/system/flask-app.service << 'EOF'
[Unit]
Description=Flask App
After=network.target

[Service]
Type=simple
User=vagrant
WorkingDirectory=/app
Environment=PATH=/app/venv/bin
ExecStart=/app/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    # Enable and start the service
    systemctl daemon-reload
    systemctl enable flask-app
    systemctl start flask-app

    # Wait for service to start
    sleep 10

    # Check if service is running
    systemctl status flask-app
  SHELL

  # Sync the current directory to /app in the VM
  config.vm.synced_folder ".", "/app", type: "rsync", rsync__exclude: [".git/", "node_modules/", ".vagrant/"]

  # Enable SSH agent forwarding
  config.ssh.forward_agent = true
end

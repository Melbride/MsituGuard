#!/bin/bash

# Install Rust
curl https://sh.rustup.rs -sSf | sh -s -- -y

# Load Rust into the current shell
source $HOME/.cargo/env

# Set Rust to use the latest stable version
rustup default stable

# Now install your Python dependencies
pip install -r requirements.txt

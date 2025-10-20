# syscall_fetch
A colorful lightweight Python CLI tool to **fetch Linux syscall details** and **calling conventions** for x86, x64, ARM, and ARM64 architectures  using the [syscall.sh API](https://api.syscall.sh).

## Installation

git clone https://github.com/nyxFault/syscall_fetch.git
cd syscall_fetch
pip install -r requirements.txt
chmod +x syscall_fetch.py
./syscall_fetch.py -s write -a x86

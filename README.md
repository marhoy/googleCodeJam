# googleCodeJam
Solving problems from Google Code Jam

# Setting up the same Python environment as Google uses
The Google environment is running 64-bit Debian 9.8 (stretch). For Python 3, this means:
- 3.5.3 (package: python3.5)
 - numpy 1.16.2 (pip install numpy)
 - scipy 1.2.1 (pip install scipy) 

## For Mac OS X:
- Download and install Python 3.5.3
```bash
# Create and activate a virtual environment
python3.5 -m venv venvCJ
source ./venvCJ/bin/activate

# Upgrade pip to newer version to solve ssl issues
curl https://bootstrap.pypa.io/get-pip.py | python

# Upgrade setuptools to newest version
pip install -U setuptools

# Install numpy and scipy
pip install numpy==1.16.2 scipy==1.2.1

# Optionally install Jupyter so you can use Jupyter Notebooks
pip install jupyter
```

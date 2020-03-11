# googleCodeJam
Solving problems from Google Code Jam

# Setting up the same Python environment as Google
The Google environment is running 64-bit Debian 9.8 (stretch). For Python 3, this means:
- 3.5.3 (package: python3.5)
 - numpy 1.16.2
 - scipy 1.2.1

## For Mac OS X:
```bash
# Install Python 3.5.3
pyenv install 3.5.3

# Create a virtual environment
pyenv virtualenv 3.5.3 GoogleCJ
pyenv activate GoogleCJ

# Upgrade pip and setuptools to latest versions
pip install -U pip
pip install -U setuptools

# Install numpy and scipy
pip install numpy==1.16.2 scipy==1.2.1

# Optionally install Jupyter so you can use Jupyter Notebooks
pip install jupyter
```

from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Function to find all .py files in the project
def find_pyx_files(directory):
    pyx_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and not file.startswith('__init__'):
                pyx_files.append(os.path.join(root, file))
    return pyx_files

pyx_files = find_pyx_files(".")

# Convert file paths to module names
def convert_to_extension(file):
    # Convert file path to module path
    module_name = file.replace(".py", "")
    module_name = module_name.replace("/", ".").replace("\\", ".")
    return Extension(module_name, [file])

extensions = [convert_to_extension(file) for file in pyx_files]

setup(
    name="JARVIS",
    ext_modules=cythonize(extensions),
    zip_safe=False,
)

# Project Installation Guide

This guide provides step-by-step instructions to install and build the project on your system.

## Prerequisites

- **Git**: Ensure Git is installed to clone the repository.
- **CMake**: Required for building the project (version 3.10 or higher recommended).
- **Make**: Needed for compiling the project.
- **C++ Compiler**: A compatible C++ compiler (e.g., GCC, Clang) that supports C++17.
- **Armadillo Library**: The project uses the Armadillo library for linear algebra, which will be built from source.

## Installation Steps

### 1. Clone the Repository
Start by cloning the project repository to your local machine using the following command:

```bash
git clone <repository-url>
cd <project-directory>
cd third_party/armadillo-code/
cmake .
make
cd ../
mkdir build
cd build
cmake ..
make

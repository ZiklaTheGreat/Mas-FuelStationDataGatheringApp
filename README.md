# Project Installation Guide

This guide provides step-by-step instructions to install and build the project on your system.

## Installation Steps

### 1. Clone the Repository
Start by cloning the project repository to your local machine using the following command:

```bash
git clone https://github.com/ZiklaTheGreat/Statistics-library
cd <project-directory>
```

### 2. Build the Armadillo Library
The project depends on the Armadillo library, which is included in the third_party/armadillo-code/ directory. Follow these steps to build it:

```bash
cd third_party/armadillo-code/
cmake .
make
```

### 3. Build the Main Project
Create a build directory and compile the main project using the following commands:

```bash
cd ../
mkdir build
cd build
cmake ..
make
```

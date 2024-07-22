<p align="center">
    <img src="./brain.png" alt="Logo" width=80>
    <h2 align="center">UA OPC Interface</h2>
</p>

## Overview

UA OPC Interface is a Python-based application that provides a graphical user interface (GUI) for interacting with an OPC UA server. The application allows users to create, execute, and manage a sequence of actions for pumps connected to the OPC UA server.

## Features

- Connect to an OPC UA server.
- Add, remove, and manage pump actions.
- Execute the program and monitor execution status and elapsed time.
- Graphical user interface with Tkinter and ttkbootstrap.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.6 or later.
- You have access to an OPC UA server.
- You have installed the necessary Python packages listed in `requirements.txt`.

## Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/yourusername/ua-opc-interface.git
    cd ua-opc-interface
    ```

2. Install the required Python packages:

    ```shell
    pip install -r requirements.txt
    ```

## Usage

1. Start the application:

    ```shell
    python main.py
    ```

2. Use the GUI to connect to the OPC UA server and manage pump actions.

## Files

- `main.py`: The main script to run the application.
- `requirements.txt`: List of Python packages required to run the application.
- `brain.png`: Application icon.
- `pump.png`, `stop.png`, `clean.png`, `empty.png`, `fill.png`, `time.png`, `submit.png`: Icons used in the GUI.

## Technologies & Tools

- [Python](https://www.python.org/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Standard GUI toolkit for Python.
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/en/latest/) - A theming extension for Tkinter.
- [python-opcua](https://github.com/FreeOpcUa/python-opcua) - OPC UA implementation in Python.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OPC UA](https://opcfoundation.org/about/opc-technologies/opc-ua/) - Foundation for interoperability standard.

---

![Python](https://img.shields.io/badge/python-%2314354C.svg?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-%23FF6F00.svg?style=for-the-badge&logo=python&logoColor=white)
![ttkbootstrap](https://img.shields.io/badge/ttkbootstrap-%230081CB.svg?style=for-the-badge&logo=python&logoColor=white)
![OPC UA](https://img.shields.io/badge/OPC%20UA-%230046A6.svg?style=for-the-badge&logo=opc%20foundation&logoColor=white)

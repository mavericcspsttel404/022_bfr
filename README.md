# Breakfast Report revamped

## How to use

1. Make sure you have uv preinstalled
2. Clone the project
3. Open terminal and input below commands in order
   1. uv sync
   2. .venv\Scripts\activate.bat
   3. uv run main.py

## Initial thought process

1. Use latest stable libraries for better stability and performance
2. Use Bulk endpoints to reduce API calls usage in salesforce
3. Use uv for fast and simple package management
4. Use folders similar to a package to keep root clean

## Changelog

- 2025-06-04 - Start with above thought

```code
E:\03_RAM\022_BREAKFAST_REPORT
├───.venv
├───logs
├───output
├───reports
└───utils
    ├───db
    ├───excel
    └───mail
```

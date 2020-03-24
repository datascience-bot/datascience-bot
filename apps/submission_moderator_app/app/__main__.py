# -*- coding: utf-8 -*-
from waitress import serve

from app import app


if __name__ == "__main__":
    serve(app, listen="*:8080")

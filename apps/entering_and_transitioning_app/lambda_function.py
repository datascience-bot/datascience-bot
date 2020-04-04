# -*- coding: utf-8 -*-
"""Entrypoint for AWS Lambda function
"""
from apps.entering_and_transitioning_app import main


def lambda_handler(event, context):
    main()

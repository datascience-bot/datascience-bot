# -*- coding: utf-8 -*-
"""Entrypoint for AWS Lambda function
"""
from apps.submission_moderator_app import main


def lambda_handler(event, context):
    main()

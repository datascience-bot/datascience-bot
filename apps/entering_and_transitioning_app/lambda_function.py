# -*- coding: utf-8 -*-
"""Entrypoint for AWS Lambda function
"""
from datetime import datetime

from libs.entering_and_transitioning_app import main


def lambda_handler(event, context):
    try:
        time_string = event["body"]["time"]
        validate = event["body"]["validate"]
    except KeyError:
        main()
    else:
        time = datetime.strptime(time_string, "%Y-%m-%d")
        main(time=time, validate=validate)

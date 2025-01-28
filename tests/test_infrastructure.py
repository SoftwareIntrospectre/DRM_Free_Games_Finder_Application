import pytest
import json
import boto3

def test_cloudwatch_logs():
    client = boto3.client('logs', region_name='us-west-2')
    log_group = "/ecs/drm-game-comparison"
    logs = client.describe_log_streams(logGroupName=log_group)
    assert len(logs['logStreams']) > 0

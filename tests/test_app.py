import os
import sys
import json
import pytest
from unittest.mock import patch
from flask import request
from .data import data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Subscriptions.subscription import create_subscription
from app import app
from .data import plandef
from Subscriptions.Process_subscriptions.process import extract_reference_values
from dotenv import load_dotenv
load_dotenv()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_extract_reference_values_dict():
    data = {"reference": "value"}
    result = extract_reference_values(data)
    assert result == ["value"]

def test_extract_reference_values_nested_dict():
    data = {"key": {"reference": "value"}}
    result = extract_reference_values(data)
    assert result == ["value"]

def test_extract_reference_values_list():
    data = [{"reference": "value1"}, {"reference": "value2"}]
    result = extract_reference_values(data)
    assert result == ["value1", "value2"]

def test_extract_reference_values_nested_list():
    data = [{"key": {"reference": "value1"}}, {"key": {"reference": "value2"}}]
    result = extract_reference_values(data)
    assert result == ["value1", "value2"]

def test_extract_reference_values_mixed():
    data = {"reference": "value1", "key": [{"reference": "value2"}]}
    result = extract_reference_values(data)
    assert result == ["value1", "value2"]

def test_extract_reference_values_no_reference():
    data = {"key": "value"}
    result = extract_reference_values(data)
    assert result == []

def test_extract_reference_values_empty_input():
    data = None
    result = extract_reference_values(data)
    assert result == []


@patch('requests.get')
def test_route_plandefinition_get(mock_get, client):
    base_url = os.getenv("data_source")
    mock_get.return_value.json.return_value = {"key": "value"}
    response = client.get('/PlanDefinition')
    print(response.json)
    
    mock_get.assert_called_once_with(url=f"{base_url}/PlanDefinition", headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert response.json == {"key": "value"}

@patch('requests.post')
def test_route_plandefinition_post(mock_post, client):
    base_url = os.getenv("data_source")
    mock_post.return_value.json.return_value = data()
    json_data = data()
    response = client.post('/PlanDefinition', json=json_data)
    
    #mock_post.assert_called_once_with(url=f"{base_url}/PlanDefinition", headers={"Content-Type": "application/json"}, data=json.dumps(json_data))
    assert response.status_code == 201
    assert response.json == data()

def test_create_subscription():
    status = "active"
    trigger = "encounter-end"
    apisix_gateway = "https://example.org/apisix"

    expected_subscription = {
        "resourceType": "Subscription",
        "status": status,
        "reason": "Creation of subscription based on encounter-end trigger event from PlanDefintiion.",
        "criteria": "Encounter?status=Finished",
        "channel": {
            "type": "rest-hook",
            "endpoint": apisix_gateway,
            "payload": "application/fhir+json",
            "header": [
                "Authorization: Basic dGVzdDp0ZXN0"
                ]      
        }
    }

    subscription_json = create_subscription(status, trigger, apisix_gateway)
    actual_subscription = json.loads(subscription_json)

    assert actual_subscription == expected_subscription


@patch('app.requests.get')
def test_get_plandefinition(mock_get, client):
    # Mock the external API response
    mock_get.return_value.json.return_value = {'sample': 'data'}

    response = client.get('/PlanDefinition')
    assert response.status_code == 200
    assert json.loads(response.data) == {'sample': 'data'}

    

@patch('app.requests.post')
def test_post_plandefinition(mock_post, client):
    # Mock the external API response
    mock_post.return_value.json.return_value = {'sample': 'data'}

    data = plandef()
    response = client.post('/PlanDefinition', json=data)
    assert response.status_code == 201
    assert json.loads(response.data) == {'sample': 'data'}

    

@patch('app.requests.get')
def test_get_plandefinition_id(mock_get, client):
    # Mock the external API response
    mock_get.return_value.json.return_value = {'sample': 'data'}

    response = client.get('/PlanDefinition/1')
    assert response.status_code == 200
    assert json.loads(response.data) == {'sample': 'data'}

    

    






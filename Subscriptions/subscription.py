import json
import os

# Create the FHIR Subscription resource as a dictionary
trigger_codes = {}


# Define variables
id = "encounter-end-subscription-example"
status = "active"
channel_endpoint = "https://example.org/Endpoints/d7dcc004-808d-452b-8030-3a3a13cd871d"


# Create the FHIR Subscription resource dictionary
def create_subscription(status, trigger, apisix_gateway):
     
    triggers = {
    "encounter-change" : "Encounter?status=Finished",
    "encounter-start" : "Encounter?status=in-progress",
    "encounter-end" : "Encounter?status=Finished",
    "encounter-modified" : "Encounter?status=in-progress",
    "diagnosis-change" : "Condition?verification-status=confirmed",
    "new-diagnosis" : "Condition?verification-status=confirmed",
    "modified-diagnosis" : "Encounter?status=in-progress",
    }

    fhir_subscription = {
        "resourceType": "Subscription",
        "status": status,
        "reason": "Creation of subscription based on encounter-end trigger event from PlanDefintiion.",
        "criteria": triggers[trigger],
        "channel": {
            "type": "rest-hook",
            "endpoint": apisix_gateway,
            "payload": "application/fhir+json",
            "header": [
                "Authorization: Basic dGVzdDp0ZXN0"
                ]      
        }
    }
    return json.dumps(fhir_subscription, indent=3)

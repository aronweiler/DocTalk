from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.conf import settings
import requests
import json
import os

channel_layer = get_channel_layer()

@shared_task
def get_response(channel_name, input_data):
    # Make a GET request to the /query endpoint    
    request_url = os.getenv("AI_BACKEND", "http://host.docker.internal:8100")
    response = requests.get(f"{request_url}/query?query={input_data['text']}")

    # Check the response status code
    if response.status_code == 200:
        # Access the response data
        response = response.json()
    else:
        raise ValueError(f"Error querying the API, status_code: {response.status_code}")
    
    async_to_sync(channel_layer.send)(
        channel_name,
        {
            "type": "chat.message",
            "text": {"msg": response["result"]["result"], "source": "bot", "source_documents": response["result"]["source_documents"]},
        },
    )



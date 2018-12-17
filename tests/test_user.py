import pytest
import os
import json
from ..app import create_app, db

def test_hello(client):
    response = client.get('/')
    assert response.data == b'Congratulations! Your part 2 endpoint is working'
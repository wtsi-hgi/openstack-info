import json
import os

TEST_USERNAME = "user"
TEST_PASSWORD = "pass"
TEST_AUTH_URL = "http://example.com:5000/v2.0/"
TEST_TENANT_NAME = "tenant"

RESOURCES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")

with open(os.path.join(RESOURCES_PATH, "information-indexed-by-type.json"), "r") as file:
    INFORMATION_INDEXED_BY_TYPE = json.load(file)
with open(os.path.join(RESOURCES_PATH, "information-indexed-by-id.json"), "r") as file:
    INFORMATION_INDEXED_BY_ID = json.load(file)

import os

TEST_USERNAME = "user"
TEST_PASSWORD = "pass"
TEST_AUTH_URL = "http://example.com:5000/v2.0/"
TEST_TENANT_NAME = "tenant"

RESOURCES_PATH = "resources"

with open(os.path.join(RESOURCES_PATH, "information-indexed-by-type.json"), "r") as file:
    INFORMATION_INDEXED_BY_TYPE = file.read()
with open(os.path.join(RESOURCES_PATH, "information-indexed-by-id.json"), "r") as file:
    INFORMATION_INDEXED_BY_ID = file.read()


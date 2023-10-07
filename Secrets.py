from google.cloud import secretmanager
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class Secrets():
    def __init__(self):
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url="https://moonquakeapi.vault.azure.net/", credential=credential)
        self.mongoConnectionString = client.get_secret("mongoConnectionString").value
        self.appClientId = client.get_secret("appClientId").value
        self.appClientSecret = client.get_secret("appClientSecret").value
        
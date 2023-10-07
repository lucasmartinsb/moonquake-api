from google.cloud import secretmanager
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class Secrets():
    def __init__(self):
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url="https://moonquakeapi.vault.azure.net/", credential=credential)
        self.mongoConnectionString = self.getSecret(projectId="rising-apricot-401312", secretId="mongoConnectionString", versionId=1)
        self.appClientId = client.get_secret("appClientId").value
        self.appClientSecret = client.get_secret("appClientSecret").value
        
    def getSecret(self, projectId : str, secretId : str, versionId : int):
        name = f"projects/{projectId}/secrets/{secretId}/versions/{versionId}"
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(name=name)
        payload = response.payload.data.decode("UTF-8")
        return payload 
    

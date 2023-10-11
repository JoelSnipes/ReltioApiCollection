import requests

modules = ["Configuration", "Data Ingestion", "Data Operation", "Integration", "Tenant Management"]

for module in modules:
    url = "https://developer.reltio.com/groupmodules?groupfor=" + module

    payload = {}
    headers = {
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    #Save to File in openApiSpec folder
    filename = "openApiSpec/" + module + ".json"
    with open(filename, "w") as f:
        f.write(response.text)
    #print(response.text)


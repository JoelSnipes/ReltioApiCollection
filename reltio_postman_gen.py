import requests
import sys
import os
import json

def get_openapi_specs():

    modules = ["Configuration", "Data Ingestion", "Data Operation", "Integration", "Tenant Management"]

    for module in modules:
        url = "https://developer.reltio.com/groupmodules?groupfor=" + module

        payload = {}
        headers = {
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        #Save to File in openApiSpec folder
        filename = "openApiSpec/" + module + ".json"
        with open(filename, "w+") as f:
            f.write(response.text)
        #print(response.text)



   
##TODO
## Make the function take a the file path as a parameter
## Make the function take a list of variables to replace
## Remove services from all paths

def post_process(path):
    remove_path_variable(path, 'services')
    #Need to figure out how to remote oauth when it appears in the path twice 
    
    #remove_path_variable(path, 'oauth')

    replace_param_variable(path, 'tenantId', "{{tenant}}")
    replace_param_variable(path, 'customerId', "{{customerId}}")

    replace_name_variable(path, '/services', "")
    replace_name_variable(path, '/reltio', "")
    replace_name_variable(path, '/api', "")
    replace_name_variable(path, '/:tenantId', "")  
    #replace_name_variable(path, '/:customerId', "")
    replace_name_variable(path, '/:clientId', "")
    replace_name_variable(path, '/v1', "")
    replace_name_variable(path, '/oauth', "")



    set_auth(path, 'oath2')

def remove_path_variable(path, variable):

    collection= load_collection(path)
    for folder in collection.get('item'):
        endpoints = folder.get('item')
        #if endpoint is not in a folder
        if endpoints is None:
            try:
                  
                folder.get('request').get('url').get('path').remove(variable)
                
            except:
                pass
            break

        else:
            try:
                for endpoint in endpoints:                                
                    endpoint.get('request').get('url').get('path').remove(variable)
                    
            except:
                pass  
                
        folder = endpoints
    write_collection(collection, path)

def replace_param_variable(path, find, replace):

    collection= load_collection(path)
    for folder in collection.get('item'):
        endpoints = folder.get('item')
        if endpoints is None:
            try:
                endpoint.get('request').get('url').get('variable')["value"] = replace
            except:
                pass
            break
        for endpoint in endpoints:
            for variable in endpoint.get('request').get('url').get('variable'):
                 if variable["key"] == find:
                        variable["value"] = replace
        folder = endpoints
    write_collection(collection, path)

def replace_name_variable(path, find, replace):

    collection = load_collection(path)
    for folder in collection.get('item'):
        endpoints = folder.get('item')
        if endpoints is not None:
            for endpoint in endpoints:
                endpoint['name'] = endpoint['name'].replace(find, replace)
                
          
    write_collection(collection, path)


def set_auth(path, auth_type):
    
    collection= load_collection(path)
    collection['auth']  = auth_type
    write_collection(collection, path)    

def load_collection(path):
    with open( path, 'r') as f:
        collection = json.load(f)
    return collection

def write_collection(collection, path):
    with open(path, 'w+') as f:
        json.dump(collection, f, indent=4)

def main(args):
    if args[0] == "get_openapi_specs":
        get_openapi_specs()
    elif args[0] == "post_process":
        post_process(args[1])



if __name__ == "__main__":
     main(sys.argv[1:])



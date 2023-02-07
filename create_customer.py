import argparse
from scraper import getWebsiteInfo
import json



def create_deployment(customer_name, customer_url, deployment_type):
    result = {
        "name":customer_name,
        "template":deployment_type,
        "entities":[],
        "website":getWebsiteInfo(customer_url, 50)
    }
    f = open(f"./configs/{customer_name}.json", "w")
    f.write(json.dumps(result, indent=4))
    f.close()
    

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-n", "--name", help="Customer name")
    argParser.add_argument("-t", "--template", help="Customer template", choices=["faq","reservation"])
    argParser.add_argument("-u", "--url", help="Customer url")

    args = argParser.parse_args()
    create_deployment(args.name, args.url, args.template)
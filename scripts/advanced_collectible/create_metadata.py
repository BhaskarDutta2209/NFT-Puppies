import json
import os
from brownie import AdvancedCollectible, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_breed
from pathlib import Path
import requests

def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible)-1]

    number_of_tokens = advanced_collectible.tokenCounter()
    print("The number of tokens deployed is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, advanced_collectible)

def write_metadata(number_of_tokens, nft_contract):
    for tokenId in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        breed = get_breed(nft_contract.tokenIdToBreed(tokenId))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active()) + str(tokenId)
            + "-" + breed + ".json"
        ) 
        # ./metadata/rinkeby/0-SHIBA_INU.json
        if Path(metadata_file_name).exists():
            print("{} already found".format(metadata_file_name))
        else:
            print("Creating Metadata File {}".format(metadata_file_name))
            collectible_metadata["name"] = get_breed(nft_contract.tokenIdToBreed(tokenId))
            collectible_metadata["description"] = "An adorable {} pip!".format(collectible_metadata["name"])
            print(collectible_metadata)

            image_to_upload = None

            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(breed.lower().replace("_","-"))
                image_to_upload = upload_to_ipfs(image_path)
            
            collectible_metadata['image'] = image_to_upload

            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)

            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)       

def upload_to_ipfs(filepath):
    print(filepath)
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]

        uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)
        print(uri)
        return uri
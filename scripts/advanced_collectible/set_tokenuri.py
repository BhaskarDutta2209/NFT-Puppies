from brownie import AdvancedCollectible, network, accounts, config
from scripts.helpful_scripts import get_breed


dog_metadata_dic = {
    "PUB": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"

def main():
    print("Working on " + network.show_active())
    advancedCollectible = AdvancedCollectible[len(AdvancedCollectible)-1]
    number_of_advanced_collectibles = advancedCollectible.tokenCounter()
    print("The number of tokens you have deployed is " + str(number_of_advanced_collectibles))

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advancedCollectible.tokenIdToBreed(token_id))
        if not advancedCollectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, advancedCollectible, dog_metadata_dic[breed])
        else:
            print("Skipping {}, we have already set that tokenURI!".format(token_id))

def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config['wallets']['from_key'])
    nft_contract.setTokenURI(token_id, tokenURI, {"from":dev})
    print (
        "Awesome! You can now view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print("Please give upto 20minutes, and hit the 'refresh metadata' button")

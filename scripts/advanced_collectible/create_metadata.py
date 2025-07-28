from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path


def main():
    advance_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advance_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advance_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        if Path(metadata_file_name).exists():
            print(f" {metadata_file_name} already exist! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")

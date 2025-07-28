from brownie import (
    accounts,
    network,
    config,
    LinkToken,
    VRFCoordinatorMock,
    Contract,
    MockV3Aggregator,
    interface,
)
from brownie import LinkToken

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
DECIMALS = 8
INITIAL_VALUE = 200000000000

contract_to_mock = {
    # "eth_usd_price_feed": MockV3Aggregator,  # Mock ETH/USD price feed
    "vrf_coordinator": VRFCoordinatorMock,  # Mock VRF Coordinator
    "link_token": LinkToken,  # Mock LINK token
}


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # Deploy a mock contract
            deploy_mocks()
        # Return the most recently deployed mock contract MockV3Aggregator
        contract = contract_type[-1]
    else:
        # # For live networks, get the address from the config
        # contract_address = config["networks"][network.show_active()][contract_name]
        # # Get the contract type from brownie
        # contract = Contract.from_abi(
        #     contract_type._name, contract_address, contract_type.abi
        # )
        try:
            contract_address = config["networks"][network.show_active()][contract_name]
            contract = Contract.from_abi(
                contract_type._name, contract_address, contract_type.abi
            )
        except KeyError:
            print(
                f"{network.show_active()} address not found, perhaps you should add it to the config or deploy mocks?"
            )
            print(
                f"brownie run scripts/deploy_mocks.py --network {network.show_active()}"
            )
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    print("Deploying Mock Link Token...")
    # MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print(f"Deployed to {mock_price_feed.address}")
    print("Deploying Mock VRFCoordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})

    print("Deploying Mock VRFCoordinator...")
    print("Mocks Deployed!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Funded contract with LINK!")
    print(f"Funded {contract_address}")
    return tx

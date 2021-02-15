import pytest
from brownie import config


@pytest.fixture
def tokenOwner(accounts):
    yield accounts[0]


@pytest.fixture
def tokenFactory(tokenOwner, Token):
    def factory():
        return tokenOwner.deploy(Token)

    yield factory


@pytest.fixture
def gov(accounts):
    yield accounts[1]


@pytest.fixture
def rewards(gov):
    yield gov


@pytest.fixture
def guardian(accounts):
    yield accounts[2]


@pytest.fixture
def user(accounts):
    yield accounts[3]


@pytest.fixture
def controllerFactoryV1(gov, StrategyControllerV2):
    def factory():
        controller = gov.deploy(
            StrategyControllerV2, "0x0000000000000000000000000000000000000000"
        )
        return controller

    yield factory


@pytest.fixture
def vaultFactoryV1(gov, yVault):
    def factory(token, controller):
        vault = gov.deploy(yVault, token, controller)
        return vault

    yield factory


@pytest.fixture
def vaultFactory(pm, gov, rewards, guardian):
    def factory(token):
        Vault = pm(config["dependencies"][0]).Vault
        vault = guardian.deploy(Vault)
        vault.initialize(token, gov, rewards, "", "", {"from": guardian})
        vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
        return vault

    yield factory


@pytest.fixture
def vaultSwap(guardian, VaultSwap):
    yield guardian.deploy(VaultSwap)

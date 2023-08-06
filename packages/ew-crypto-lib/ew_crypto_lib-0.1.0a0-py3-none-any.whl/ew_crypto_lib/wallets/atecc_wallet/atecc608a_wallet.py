from ew_crypto_lib.wallets.ew_wallet import Wallet

class ATECC608aWallet(Wallet):
    def __init__(self, path: str = '/dev/i2c-1') -> None:
        self.path=path
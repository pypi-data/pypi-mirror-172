import base64
from sha3 import keccak_256

from ew_crypto_lib.entities.jwt_header_entity import JWTHeader
from ew_crypto_lib.entities.wallet_type import INFINEON
from ew_crypto_lib.wallets.ew_wallet import Wallet
from ew_crypto_lib.wallets.file_wallet.file_wallet import FileWallet
from ew_crypto_lib.wallets.atecc_wallet.atecc608a_wallet import ATECC608aWallet
from ew_crypto_lib.wallets.infineon_wallet.infineon_wallet import InfineonWallet

wallets = {
    'file': FileWallet,
    'atecc': ATECC608aWallet,
    'infineon': InfineonWallet,
}

class CryptoService:

    def __init__(self) -> None:
        self.__wallet:Wallet = None

    def __base64_url_encode(self, string:str) -> str:
        encoded = base64.urlsafe_b64encode(string.encode('utf-8')).decode('utf-8')
        return encoded.rstrip("=")
    
    def __base64_url_decode(self, string:str) -> str:
        padding = 4 - (len(string) % 4)
        string = string + ("=" * padding)
        return base64.urlsafe_b64decode(string.encode('utf-8')).decode('utf-8')
    
    def public_key(self) -> str:
        return self.__wallet.get_public_key()
    
    def create_jwt(self, payload:str) -> str:
        header:JWTHeader = JWTHeader(
            alg='ES256',
            typ='JWT'
        )
        encoded_header:str = self.__base64_url_encode(header.to_json())

        encoded_payload:str = self.__base64_url_encode(payload)

        message:str = "".join([encoded_header, '.', encoded_payload])

        k = keccak_256()
        k.update(bytes(message, 'utf-8'))
        signature = self.__wallet.sign(k.hexdigest())
        encoded_signature:str = self.__base64_url_encode(str(signature))

        jwt_token:str = "".join([encoded_header, '.', encoded_payload, '.', encoded_signature])
        return jwt_token

    def verify_jwt(self, jwt:str, public_key = None ) -> bool:
        pass

    @property
    def wallet(self) -> Wallet:
        return self.__wallet
    @wallet.setter
    def wallet(self, wallet_type:str):
        self.__wallet=wallets[wallet_type]()

    def set_wallet_key_slot(self, slot=0) -> None:
        self.__wallet.set_key_slot(slot)

if __name__ == '__main__':
    crypto_service = CryptoService()
    crypto_service.wallet = INFINEON
    crypto_service.set_wallet_key_slot()
    crypto_service.public_key()
    crypto_service.create_jwt('testing')

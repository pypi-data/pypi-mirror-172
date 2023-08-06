import binascii
import eth_keys
import secrets
from sha3 import keccak_256
from ew_crypto_lib.wallets.ew_wallet import Wallet


class FileWallet(Wallet):

    def __init__(self, path:str = '.env') -> None:
        #TODO check path and raise exception
        self._path=path
        self.set_key_slot()
        #TODO get from path
        self.__set_pk('')
    
    def set_key_slot(self, slot=0) -> None:
        self._key_slot = None
    
    def get_public_key(self) -> str:
        if not self.pk:
            self.generate_key()

        eth_pk = eth_keys.keys.PrivateKey(binascii.unhexlify(self.pk))
        eth_pub = eth_pk.public_key
        return str(eth_pub)

    def generate_key(self) -> str:
        self.pk = keccak_256(secrets.token_bytes(32)).digest()
        #TODO write to file

    def sign(self, payload:str) -> str:
        signer = eth_keys.keys.PrivateKey(binascii.unhexlify(self.pk))
        signature = signer.sign_msg(payload.encode('utf-8'))
        return signature
    
    def verify(self, signature:str, public_key=None) -> bool:
        pass

    @property
    def pk(self) -> str:
        pass
    @property
    def path(self):
        return self._path
    @property
    def key_slot(self) -> int:
        return self._key_slot
    
    def __set_pk(self, private_key:str)->None:
        self.pk = private_key
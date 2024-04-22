from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


modes_mapping = {
    "ECB": AES.MODE_ECB,
    "CBC": AES.MODE_CBC
}

class KnownCipherRandomMode():
    def __init__(self, mode):
        # modes = [AES.MODE_ECB, AES.MODE_CBC]
        # self.mode = random.choice(modes)
        if mode not in modes_mapping.keys():
            raise ValueError("Invalid mode")
        self.mode = modes_mapping[mode]

        self.key = get_random_bytes(32)
        if self.mode == AES.MODE_ECB:
            self.iv = None
            self.cipher = AES.new(key=self.key, mode=self.mode)
        else:
            self.iv = get_random_bytes(16)
            self.cipher = AES.new(key=self.key, iv=self.iv, mode=self.mode)
        
    def encrypt(self, data):
        return self.cipher.encrypt(data)
    
    def decrypt(self, data):
        return self.cipher.decrypt(data)

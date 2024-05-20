from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
# from secret import flag
from Crypto.PublicKey import RSA
import sys
sys.path.append('../../rsa_textbook_attacks')
from common_modulus import common_modulus_attack
from basic_rsa import decrypt

# p,q = getPrime(512), getPrime(512)
# n = p*q
# e = [31,71]
# print(n)
# m = bytes_to_long(flag)
# print([pow(m,ee,n) for ee in e])

n = 74127062592257379832681970870208459545927212876474945408181055721483431144118749449983805496907327519686009984113230515437169786731373036071335230064283343801130988057490937279732537899866535311631000990092668325335053279896045043314501128208259798187003002650817314007262825084594642234582964348500474384789
ciphers = [
        24226980988773997507073115936081752432469234074309070603829150651361400993090238408437733187516125091349349900636015110297875050668189314924814632263843789027833184643836128394396861399990327927221587362355128056287769156124240066559919680659298140935321396733182876952727302612009590208802133940956113028197,
        11894067048854576466109342934305835296168604754031192140834815754346495031539560484115416761045937477048684043863029512406579476058237650009484290949671784749114768244628343374294343124582303966158022954978947123786419579160186053349059585106024649979366538138598020496831198952443712050184382867584908984705
    ]

m = common_modulus_attack(ciphers[0], ciphers[1], 31, 71, n)
print(long_to_bytes(m).decode())
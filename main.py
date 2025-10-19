import gzip
import base64
import binascii
import colorama
import time

class CastleGzipCodec:
    @staticmethod
    def decode(data: str, encoding: str = 'hex') -> str:
        data = ''.join(data.strip().split())
        if encoding == 'hex':
            if len(data) % 2 != 0:
                data = '0' + data
            if data.startswith('0x'):
                data = data[2:]
            compressed = binascii.unhexlify(data)
        elif encoding == 'base64':
            compressed = base64.b64decode(data)
        else:
            raise ValueError('Unsupported encoding: ' + encoding)
        decompressed = gzip.decompress(compressed)
        return decompressed.decode('utf-8')

    @staticmethod
    def encode(json_str: str, encoding: str = 'hex') -> str:
        compressed = gzip.compress(json_str.encode('utf-8'))
        if encoding == 'hex':
            return binascii.hexlify(compressed).decode('ascii')
        elif encoding == 'base64':
            return base64.b64encode(compressed).decode('ascii')
        else:
            raise ValueError('Unsupported encoding: ' + encoding)

if __name__ == '__main__':
    with open('fp.json', 'r', encoding='utf-8') as f:
        original = f.read().strip()
        
    encoded = CastleGzipCodec.encode(original, 'hex')
    print(colorama.Fore.GREEN + 'Encoded (hex):', encoded, colorama.Style.RESET_ALL)


    decoded = CastleGzipCodec.decode(encoded, 'hex')
    print(colorama.Fore.GREEN + 'Decoded:', decoded, colorama.Style.RESET_ALL)


    from requests import post

    request = post("https://analytics.castle.io/e/?ip=0&_=1760817666054&ver=1.275.3&compression=gzip-js", data=bytes.fromhex(encoded), headers= {
        "Connection": "keep-alive",
        "content-type": "text/plain",
        "Host": "analytics.castle.io",
        "Origin": "https://castle.io",
        "Referer": "https://castle.io/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    }).json()

    print(colorama.Fore.GREEN + 'Status:', request['status'], colorama.Style.RESET_ALL)

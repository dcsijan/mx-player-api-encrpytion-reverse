
import uuid

# Equivalent to the JavaScript code that generates and formats the UUID
m = uuid.uuid4().hex


import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt_request_data(data, key):
    # Convert data to JSON string and then to bytes
    data_json = json.dumps(data).encode('utf-8')
    
    # Pad the data to be compatible with AES block size
    padded_data = pad(data_json, AES.block_size)
    
    # Create AES cipher object with ECB mode
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)
    
    # Return base64 encoded result
    return base64.b64encode(encrypted_data).decode('utf-8')

# Your specific key (note this is treated as UTF-8 string, not hex)
SECRET_KEY = m.encode('utf-8')

# Usage example
request_data = {}
encrypted = encrypt_request_data(request_data, SECRET_KEY)
print('Encrypted:', encrypted)

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Util import Padding
import base64

# Public Key (PEM Format)
public_key_pem = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl4CJiMro7S7EwvCjnpET
YoVkScgSC7ezawi28IT5AToVc14kkMCImOrtByuZZ+GWfyXGiX1b3qOZnTERhn5k
1SgHEK9rhSVcL7z65ixQ0fwyNUG37HyWT/A1ITatfdgeURUwkkvfu1rG4Yj6L+Jz
TUgstRoisLC7bwQq/EO67G53C/rSfbgWv2y1FUzeoxzEqaXiMXhM98KheR+PvC8s
GSZ7GYZjF/YXIfrB+LMFX9Ohqp4P2AAJBtruiz7tt2lbQXrqCAyJ/9K5hANgiiZ8
If2jQn2UOi66ACwbP6TA2grmocFwmEAhXQ71lPeU4m+rOD5Uq1XZoKkfq1YatgpK
LwIDAQAB
-----END PUBLIC KEY-----'''

# Data to encrypt (string t)
t = m

# Load public key
public_key = RSA.import_key(public_key_pem)

# Create a cipher object using the public key
cipher = PKCS1_v1_5.new(public_key)

# Encrypt the data
encrypted_data = cipher.encrypt(t.encode('utf-8'))

# Base64 encode the encrypted data
encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')

# Output the encrypted data in base64 format
print(encrypted_base64)


import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

encrypted_data = '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'
key = m.encode('utf-8')

# Decode Base64 encrypted data
ciphertext = base64.b64decode(encrypted_data)

# Initialize AES cipher in ECB mode
cipher = AES.new(key, AES.MODE_ECB)

# Decrypt and unpad
decrypted_padded = cipher.decrypt(ciphertext)
decrypted = unpad(decrypted_padded, AES.block_size).decode('utf-8')

print('Decrypted data:', decrypted)
















########################################################
#############################
######################
##################
#############
#######
######



proxy_url = "http://as77hs6qjikh4xg-country-in:neatfbj2cw4f37g@rp.scrapegw.com:6060"
proxies = {
    "http": proxy_url,
    "https": proxy_url,
}


from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/movies', methods=['GET'])
def get_movie():
    movie_name = request.args.get('movie_name')
    import uuid,requests,json
    m = uuid.uuid4().hex



    import json
    import base64
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad

    def encrypt_request_data(data, key):
        # Convert data to JSON string and then to bytes
        data_json = json.dumps(data).encode('utf-8')
    
        # Pad the data to be compatible with AES block size
        padded_data = pad(data_json, AES.block_size)
    
        # Create AES cipher object with ECB mode
        cipher = AES.new(key, AES.MODE_ECB)
    
        # Encrypt the data
        encrypted_data = cipher.encrypt(padded_data)
    
        # Return base64 encoded result
        return base64.b64encode(encrypted_data).decode('utf-8')

    # Your specific key (note this is treated as UTF-8 string, not hex)
    SECRET_KEY = m.encode('utf-8')

    # Usage example
    request_data = {}
    encrypted = encrypt_request_data(request_data, SECRET_KEY)
    print('Encrypted:', encrypted)

    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.Util import Padding
    import base64

    # Public Key (PEM Format)
    public_key_pem = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl4CJiMro7S7EwvCjnpET
    YoVkScgSC7ezawi28IT5AToVc14kkMCImOrtByuZZ+GWfyXGiX1b3qOZnTERhn5k
    1SgHEK9rhSVcL7z65ixQ0fwyNUG37HyWT/A1ITatfdgeURUwkkvfu1rG4Yj6L+Jz
    TUgstRoisLC7bwQq/EO67G53C/rSfbgWv2y1FUzeoxzEqaXiMXhM98KheR+PvC8s
    GSZ7GYZjF/YXIfrB+LMFX9Ohqp4P2AAJBtruiz7tt2lbQXrqCAyJ/9K5hANgiiZ8
    If2jQn2UOi66ACwbP6TA2grmocFwmEAhXQ71lPeU4m+rOD5Uq1XZoKkfq1YatgpK
    LwIDAQAB
    -----END PUBLIC KEY-----'''

    # Data to encrypt (string t)
    t = m

    # Load public key
    public_key = RSA.import_key(public_key_pem)

    # Create a cipher object using the public key
    cipher = PKCS1_v1_5.new(public_key)

    # Encrypt the data
    encrypted_data = cipher.encrypt(t.encode('utf-8'))

    # Base64 encode the encrypted data
    encrypted_base64 = base64.b64encode(encrypted_data).decode('utf-8')



    def extract(data):

        import base64
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad

        encrypted_data =data
        key = m.encode('utf-8')

        # Decode Base64 encrypted data
        ciphertext = base64.b64decode(encrypted_data)

        # Initialize AES cipher in ECB mode
        cipher = AES.new(key, AES.MODE_ECB)

        # Decrypt and unpad
        decrypted_padded = cipher.decrypt(ciphertext)
        decrypted = unpad(decrypted_padded, AES.block_size).decode('utf-8')

  
        return decrypted


    # URL and headers for the request
    url = f"https://api.mxplayer.in/v1/web/search/resultv2?query={movie_name}&&platform=com.mxplay.desktop&content-languages=hi,en&kids-mode-enabled=false"
    headers = {
        'Host': 'api.mxplayer.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'x-guard-flag': 'true',
        'x-guard-key': encrypted_base64,
        'Origin': 'https://www.mxplayer.in',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.mxplayer.in/',
    }

    data={
	    "requestBody": encrypted
    }


    # Making the GET request
    response = requests.post(url, headers=headers,json=data,proxies=proxies)

    # Checking the response status and content
    if response.status_code == 200:
   
        response= response.json()['response']
        output = extract(response)
        data=json.loads(output)
       
        import json

        BASE_URL = 'https://d3sgzbosmwirao.cloudfront.net/'

        def c(e, t):
            """Helper function to concatenate base URL if needed"""
            if t and 'https://' not in t and 'http://' not in t:
                return e + t
            return t

        def l(e):
            """Check if third party provider is sun_tv"""
            return e and e.get('provider') == 'thirdParty' and e.get('thirdParty', {}).get('name') == 'sun_tv'

        def s(e, t):
            """Process stream information to extract HLS and DASH URLs"""
            n = e.get('provider')
            a = e.get(n, {}) if n else {}
            is_sun_tv = l(e)
            result = {'hls': {}, 'dash': {}}
    
            if not a:
                return result
    
            if is_sun_tv:
                result['hls']['url'] = a.get('webHlsUrl')
                return result
    
            # Process HLS
            hls_source = a.get('hlsUrl') or a.get('hls')
            hls_url = None
            if isinstance(hls_source, dict):
                hls_main = hls_source.get('main') or hls_source.get('base') or hls_source.get('high')
                if n == 'mxplay' and hls_main:
                    hls_url = c(t, hls_main)
                else:
                    hls_url = hls_main
            elif hls_source:
                hls_url = c(t, hls_source) if n == 'mxplay' else hls_source
    
            # Process DASH
            dash_source = a.get('dashUrl') or a.get('dash')
            dash_url = None
            if isinstance(dash_source, dict):
                dash_main = dash_source.get('main') or dash_source.get('base') or dash_source.get('high')
                if n == 'mxplay' and dash_main:
                    dash_url = c(t, dash_main)
                else:
                    dash_url = dash_main
            elif dash_source:
                dash_url = c(t, dash_source) if n == 'mxplay' else dash_source

    
            result['hls'].update({
                'url': hls_url,
                'hlsId': a.get('hlsId')
            })
    
            result['dash'].update({
                'url': dash_url,
                'dashId': a.get('dashId')
            })
    
            return result

        def get_movie_or_tv_show_streams(api_response):
            """Main function to process API response and extract streaming info"""
            results = []
            for section in api_response.get('sections', []):
                for item in section.get('items', []):
                    if item.get('type') == 'movie':
                        stream_info = s(item.get('stream', {}), BASE_URL)
                  
                        results.append({
                            'title': item.get('title'),
                            'image':item.get('imageInfo', [None])[0]['url'],
                            'type': item.get('type'),
                            'hlsUrl': stream_info['hls'].get('url'),
                            'dashUrl': stream_info['dash'].get('url'),
                      
                        })

                    elif item.get('type')  == 'tvshow':
                        tv_link = item.get('firstVideo')['id']
                      

                        play_link = 'https://api.mxplayer.in/v1/web/detail/video?type=episode&id='+tv_link+'&device-density=2&platform=com.mxplay.desktop&content-languages=hi,en&kids-mode-enabled=false'
                        ep =  requests.get(play_link,headers=headers)
                        stream_info = s(ep.json().get('stream', {}), BASE_URL)
                    
                        results.append({
                            'title': item.get('title'),
                            'image':item.get('imageInfo', [None])[0]['url'],
                            'videoCount':item.get('videoCount'),
                            'type': item.get('type'),
                            'hlsUrl': stream_info['hls'].get('url'),
                            'dashUrl': stream_info['dash'].get('url'),
                            'container_id':ep.json()['container']['id']
                  
                        })


            return results

        
        results = get_movie_or_tv_show_streams(data)
        print(json.dumps(results, indent=2))
        return jsonify(results)
        
 

   
   
    else:
        print(f"Error: {response.status_code}")

#@app.route('/episode', methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)


#import requests

#s = requests.Session()
#proxy_url = "http://as77hs6qjikh4xg-country-in:neatfbj2cw4f37g@rp.scrapegw.com:6060"
#proxies = {
#    "http": proxy_url,
#    "https": proxy_url,
#}
        
#headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
#        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#        "Accept-Language": "en-US,en;q=0.5",
#        "Upgrade-Insecure-Requests": "1",
#        "Sec-Fetch-Dest": "document",
#        "Host":"api.mxplayer.in",
#        "Sec-Fetch-Mode": "navigate",
#        "Sec-Fetch-Site": "none",
#        "Sec-Fetch-User": "?1",
#        "Priority": "u=0, i",
#        }

##url = 'https://www.mxplayer.in'

##response = s.get(url,headers=headers,proxies=proxies)
##print(response.headers)

##print(response.text)

## URL to request
#url = "https://api.mxplayer.in/v1/web/detail/video?type=movie&id=cf4148eed2c0bbdde82aa8e3164f91c6&device-density=2&platform=com.mxplay.desktop&content-languages=hi,en&kids-mode-enabled=false"

#response = s.get(url,headers=headers,allow_redirects=True,proxies=proxies)
#print(f"Status Code: {response.status_code}")
#print(f"Response Content: {response.text}")

#response = requests.get('http://ip-api.com/json/',proxies=proxies)
#print(f"Status Code: {response.status_code}")
#print(f"Response Content: {response.json()}")

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, uuid, json, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

app = Flask(__name__)
CORS(app)

# Setup your proxy (if needed)
proxy_url = "http://as77hs6qjikh4xg-country-in:neatfbj2cw4f37g@rp.scrapegw.com:6060"
proxies = {
    "http": proxy_url,
    "https": proxy_url,
}
proxies = None

def encrypt_request_data(data, key):
    data_json = json.dumps(data).encode('utf-8')
    padded_data = pad(data_json, AES.block_size)
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode('utf-8')

def extract(encrypted_data, key):
    ciphertext = base64.b64decode(encrypted_data)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_padded = cipher.decrypt(ciphertext)
    decrypted = unpad(decrypted_padded, AES.block_size).decode('utf-8')
    return decrypted

def get_headers(encrypted_key):
    return {
        'Host': 'api.mxplayer.in',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Content-Type': 'application/json',
        'x-guard-flag': 'true',
        'x-guard-key': encrypted_key,
        'Origin': 'https://www.mxplayer.in',
        'DNT': '1',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://www.mxplayer.in/',
    }

@app.route('/movies', methods=['GET'])
def get_movie():
    movie_name = request.args.get('movie_name')
    if not movie_name:
        return jsonify({"error": "movie_name parameter is required"}), 400

    # Generate a random key for encryption
    m = uuid.uuid4().hex
    SECRET_KEY = m.encode('utf-8')
    encrypted_payload = encrypt_request_data({}, SECRET_KEY)

    # RSA encrypt the key (m) using the provided public key
    public_key_pem = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl4CJiMro7S7EwvCjnpET
YoVkScgSC7ezawi28IT5AToVc14kkMCImOrtByuZZ+GWfyXGiX1b3qOZnTERhn5k
1SgHEK9rhSVcL7z65ixQ0fwyNUG37HyWT/A1ITatfdgeURUwkkvfu1rG4Yj6L+Jz
TUgstRoisLC7bwQq/EO67G53C/rSfbgWv2y1FUzeoxzEqaXiMXhM98KheR+PvC8s
GSZ7GYZjF/YXIfrB+LMFX9Ohqp4P2AAJBtruiz7tt2lbQXrqCAyJ/9K5hANgiiZ8
If2jQn2UOi66ACwbP6TA2grmocFwmEAhXQ71lPeU4m+rOD5Uq1XZoKkfq1YatgpK
LwIDAQAB
-----END PUBLIC KEY-----'''
    public_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_v1_5.new(public_key)
    encrypted_key = base64.b64encode(cipher_rsa.encrypt(m.encode('utf-8'))).decode('utf-8')

    headers = get_headers(encrypted_key)
    data_payload = {"requestBody": encrypted_payload}
    url = f"https://api.mxplayer.in/v1/web/search/resultv2?query={movie_name}&&platform=com.mxplay.desktop&content-languages=hi,en&kids-mode-enabled=false"
    
    response = requests.post(url, headers=headers, json=data_payload, proxies=proxies)
    if response.status_code == 200:
        resp_json = response.json()
        encrypted_response = resp_json.get('response')
        if not encrypted_response:
            return jsonify({"error": "No response found"}), 500
        output = extract(encrypted_response, SECRET_KEY)
        data = json.loads(output)

        BASE_URL = 'https://d3sgzbosmwirao.cloudfront.net/'

        def c(e, t):
            if t and 'https://' not in t and 'http://' not in t:
                return e + t
            return t

        def s(e, t):
            n = e.get('provider')
            a = e.get(n, {}) if n else {}
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
            return {'hls': {'url': hls_url}, 'dash': {'url': dash_url}}

        def get_movie_or_tv_show_streams(api_response):
            results = []
            for section in api_response.get('sections', []):
                for item in section.get('items', []):
                    if item.get('type') == 'movie':
                        stream_info = s(item.get('stream', {}), BASE_URL)
                        results.append({
                            'title': item.get('title'),
                            'image': item.get('imageInfo', [None])[0]['url'] if item.get('imageInfo') else '',
                            'type': item.get('type'),
                            'hlsUrl': stream_info['hls'].get('url'),
                            'dashUrl': stream_info['dash'].get('url'),
                        })
                    elif item.get('type') == 'tvshow':
                        seasons = []
                        tv_link = item.get('firstVideo', {}).get('id')
                        if tv_link:
                            season_url = f"https://api.mxplayer.in/v1/web/detail/video?type=episode&id={tv_link}"
                            headers_simple = {
                                'User-Agent': 'Mozilla/5.0',
                                'Accept': 'application/json'
                            }
                            season_res = requests.get(season_url, headers=headers_simple, proxies=proxies)
                            if season_res.status_code == 200:
                                season_data = season_res.json()
                               
            return season_data

        results = get_movie_or_tv_show_streams(data)
        print(results)
        return jsonify(results)
    else:
        return jsonify({"error": "Failed to fetch data", "status": response.status_code}), response.status_code

@app.route('/tv', methods=['GET'])
def get_tv():
    container_id = request.args.get('container_id')
    finalId = request.args.get('finalId')
    pageDirection = request.args.get('pageDirection', "0")
    
    if not container_id:
        return jsonify({"error": "container_id parameter is required"}), 400

    tv_api_url = f"https://api.mxplayer.in/v1/web/detail/tab/tvshowepisodes?type=season&pageDirection={pageDirection}&id={container_id}&sortOrder=0"
    if finalId:
        tv_api_url += f"&finalId={finalId}"

    headers_simple = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }
    tv_response = requests.get(tv_api_url, headers=headers_simple, proxies=proxies)
    if tv_response.status_code == 200:
        return jsonify(tv_response.json())
    else:
        return jsonify({"error": "Failed to fetch TV episodes", "status": tv_response.status_code}), tv_response.status_code

if __name__ == '__main__':
    app.run(debug=True)

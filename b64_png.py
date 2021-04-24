import base64
with open('base64_test', 'rb') as b64:
    with open('test.png', 'wb+') as img:
        img.write(base64.b64decode(b64.read()))
from Crypto.Cipher import AES
from hashlib import md5
from PIL import Image

while True:
    print('Which operation do you want ? :\n\t1- Encryption\n\t2- Decryption')
    wanted_operation = input('enter your choice: ')
    if wanted_operation not in ['1', '2']:
        break
        
    image_path = input('Please, enter the image path: ')
    
    key = input('please enter the AES key: ')
    
    key_hash = md5(key.encode('ascii')).digest()
    
    cipher = AES.new(key_hash, AES.MODE_GCM, nonce=b'0')
    if(wanted_operation == '1'):
        img = Image.open(image_path)
        imgGray = img.convert('L')
        imgGray.save(image_path)
    with open(image_path, 'rb') as input_image:
        image_bytes = input_image.read()
        
        if wanted_operation == '1':
            new_image_bytes = cipher.encrypt(image_bytes)
        else:
            new_image_bytes = cipher.decrypt(image_bytes)
    
    with open(image_path, 'wb') as output_image:
        output_image.write(new_image_bytes)
        print('DONE!')
        break
        

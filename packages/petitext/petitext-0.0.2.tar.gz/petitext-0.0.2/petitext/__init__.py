import os, sys, json, base64, hashlib
import cryptography.exceptions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import serialization

try:
	from cryptography.fernet import Fernet
except:
	os.system(str(sys.executable) + " -m pip install cryptography")
	from cryptography.fernet import Fernet

def sign_file(private_key, foil, foil_signature=None):
	#https://stackoverflow.com/questions/50608010/how-to-verify-a-signed-file-in-python
	# Load the private key. 
	with open(private_key, 'rb') as key_file: 
		private_key = serialization.load_pem_private_key(
			key_file.read(),
			password = None,
			backend = default_backend(),
		)

	# Load the contents of the file to be signed.
	with open(foil, 'rb') as f:
		payload = f.read()

	# Sign the payload file.
	signature = base64.b64encode(
		private_key.sign(
			payload,
			padding.PSS(
				mgf = padding.MGF1(hashes.SHA256()),
				salt_length = padding.PSS.MAX_LENGTH,
			),
			hashes.SHA256(),
		)
	)
	if foil_signature is None:
		foil_signature = foil + ".sig"
	with open(foil_signature, 'wb') as f:
		f.write(signature)

	return foil_signature

def verify_file(public_key, foil, foil_signature):
	#https://stackoverflow.com/questions/50608010/how-to-verify-a-signed-file-in-python
	# Load the public key.
	with open(public_key, 'rb') as f:
		public_key = load_pem_public_key(f.read(), default_backend())

	# Load the payload contents and the signature.
	with open(foil, 'rb') as f:
		payload_contents = f.read()
	with open(foil_signature, 'rb') as f:
		signature = base64.b64decode(f.read())

	# Perform the verification.
	try:
		public_key.verify(
			signature,
			payload_contents,
			padding.PSS(
				mgf = padding.MGF1(hashes.SHA256()),
				salt_length = padding.PSS.MAX_LENGTH,
			),
			hashes.SHA256(),
		)
		return True
	except cryptography.exceptions.InvalidSignature as e:
		print('ERROR: Payload and/or signature files failed verification!')
		return False

def hash_file(file, hash = hashlib.sha512):
    sha = hash()
    with open(file, 'rb') as f:
        while True:
            data = f.read(65536)
            if data:
                sha.update(data)
            else:
                break
    return str(sha.hexdigest())

def str_to_base64(string, encoding:str='utf-8'):
    try:
        return base64.b64encode(string.encode(encoding)).decode(encoding)
    except Exception as e:
        print(e)
        return None

def base64_to_str(b64, encoding:str='utf-8'):
     return base64.b64decode(b64).decode(encoding)

def file_to_base64(file: str):
    with open(file,'r') as reader:
        contents = reader.readlines()
    return str_to_base64(''.join(contents))

def base64_to_file(contents,file='result.txt'):
    string_contents = base64_to_str(contents)
    with open(file,'w+') as writer:
        writer.write(string_contents)
    return string_contents

def jsonl_of_dir(directory, outputfile=None, find_lambda=None):
	if find_lambda is None:
		find_lambda = lambda _: True
	content = []

	try:
		for root, directories, filenames in os.walk(directory):
			for filename in filenames:
					foil = os.path.join(root, filename)

					if find_lambda(foil):
						try:
							mini = file_to_base64(foil)
						except:
							mini = None

						current_file_info = {
							'header':False,
							'file':foil,
							'hash':hash(foil),
							'base64':mini
						}

						cur = str(json.dumps(current_file_info))
						content += [cur]

		if outputfile is not None:
			with open(outputfile, 'w+') as writer:
				for cur in content:
					writer.write(cur+"\n")

	except Exception as e:
		print(f"Issue with creating the jsonl file: {e}")

	return content

def base64_of_dir(directory, find_lambda=None):
	return str_to_base64( str(jsonl_of_dir(directory, find_lambda=find_lambda)) )
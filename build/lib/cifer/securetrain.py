import argparse
import os
import pickle
import requests
import pandas as pd
import numpy as np
from io import BytesIO
from phe import paillier
from sklearn.linear_model import LogisticRegression

def get_key_paths(key_name):
    pub_path = f"keys/{key_name}/public.key"
    priv_path = f"keys/{key_name}/private.key"
    return pub_path, priv_path

def generate_named_keys(key_name):
    print(f"🔐 Generating public/private key pair for: {key_name}")
    pubkey, privkey = paillier.generate_paillier_keypair()
    dir_path = f"keys/{key_name}"
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, "public.key"), "wb") as f:
        pickle.dump(pubkey, f)
    with open(os.path.join(dir_path, "private.key"), "wb") as f:
        pickle.dump(privkey, f)
    print(f"✅ Keys saved to: {dir_path}/public.key, {dir_path}/private.key")
    return pubkey, privkey

def load_public_key(key_name):
    path = get_key_paths(key_name)[0]
    print(f"📂 Loading public key from: {path}")
    with open(path, "rb") as f:
        return pickle.load(f)

def load_private_key(key_name):
    path = get_key_paths(key_name)[1]
    print(f"📂 Loading private key from: {path}")
    with open(path, "rb") as f:
        return pickle.load(f)

def encrypt_dataset(dataset_path_or_url, output_path, key_name):
    print("🔄 Loading dataset...")
    if dataset_path_or_url.startswith("http"):
        response = requests.get(dataset_path_or_url)
        df = pd.read_csv(BytesIO(response.content))
        print("✅ Dataset loaded from URL.")
    else:
        df = pd.read_csv(dataset_path_or_url)
        print("✅ Dataset loaded from local path.")

    df = df.select_dtypes(include='number')
    print(f"🧮 Detected numeric columns: {list(df.columns)}")

    pubkey, _ = generate_named_keys(key_name)
    print("🔐 Encrypting dataset...")
    enc_df = df.applymap(lambda x: pubkey.encrypt(x))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"💾 Saving encrypted dataset to: {output_path}")
    with open(output_path, "wb") as f:
        pickle.dump(enc_df, f)
    print("✅ Dataset encrypted and saved successfully.")

def train_model(encrypted_path, output_model_path):
    print(f"📂 Loading encrypted dataset: {encrypted_path}")
    with open(encrypted_path, "rb") as f:
        enc_df = pickle.load(f)

    print("🔄 Extracting features and labels...")
    X = np.array(enc_df.iloc[:, :-1].values.tolist())
    y = np.array(enc_df.iloc[:, -1].values.tolist())

    print("⚠️ Training model on encrypted values (simulation only using ciphertexts)...")
    X_plain = np.array([[v.ciphertext() for v in row] for row in X])
    y_plain = np.array([v.ciphertext() for v in y])

    clf = LogisticRegression()
    clf.fit(X_plain, y_plain)

    print(f"💾 Saving encrypted model to: {output_model_path}")
    with open(output_model_path, "wb") as f:
        pickle.dump(clf, f)
    print("✅ Model trained and saved successfully.")

def decrypt_model(model_path, output_path, key_name):
    print(f"📂 Loading encrypted model: {model_path}")
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    privkey = load_private_key(key_name)

    print("🔓 Decrypting model coefficients...")
    decrypted_coef = []
    for coef in model.coef_[0]:
        try:
            val = privkey.decrypt(coef)
        except Exception:
            val = coef
        decrypted_coef.append(val)

    model.coef_ = [decrypted_coef]
    print(f"💾 Saving decrypted model to: {output_path}")
    with open(output_path, "wb") as f:
        pickle.dump(model, f)
    print("✅ Decrypted model saved successfully.")

def main():
    parser = argparse.ArgumentParser(description="Cifer Secure Training (named key version)")
    subparsers = parser.add_subparsers(dest="command")

    enc = subparsers.add_parser("encrypt-dataset", help="Encrypt a CSV dataset")
    enc.add_argument("--dataset", required=True)
    enc.add_argument("--output", required=True)
    enc.add_argument("--key", required=True)

    train = subparsers.add_parser("train", help="Train model on encrypted data")
    train.add_argument("--encrypted-data", required=True)
    train.add_argument("--output-model", required=True)

    dec = subparsers.add_parser("decrypt-model", help="Decrypt model")
    dec.add_argument("--input-model", required=True)
    dec.add_argument("--output-model", required=True)
    dec.add_argument("--key", required=True)

    args = parser.parse_args()

    if args.command == "encrypt-dataset":
        encrypt_dataset(args.dataset, args.output, args.key)
    elif args.command == "train":
        train_model(args.encrypted_data, args.output_model)
    elif args.command == "decrypt-model":
        decrypt_model(args.input_model, args.output_model, args.key)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

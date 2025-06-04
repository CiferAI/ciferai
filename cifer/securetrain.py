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

    # ตรวจจับเฉพาะคอลัมน์ที่เป็นตัวเลขเท่านั้น
    df = df.select_dtypes(include='number')
    print(f"🧮 Detected numeric columns: {list(df.columns)}")

    # สร้าง key และเก็บไว้
    pubkey, _ = generate_named_keys(key_name)

    print("🔐 Encrypting dataset...")
    enc_df = df.copy()
    for col in enc_df.columns:
        enc_df[col] = enc_df[col].apply(lambda x: pubkey.encrypt(x))

    # บันทึกไฟล์
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"💾 Saving encrypted dataset to: {output_path}")
    with open(output_path, "wb") as f:
        pickle.dump(enc_df, f)

    print("✅ Dataset encrypted and saved successfully.")


def train_model(encrypted_path, output_model_path, key_name, feature_cols, label_col):
    print(f"📂 Loading encrypted dataset: {encrypted_path}")
    with open(encrypted_path, "rb") as f:
        enc_df = pickle.load(f)

    print("🔄 Extracting features and labels...")
    try:
        X_enc = enc_df[feature_cols].values.tolist()
        y_enc = enc_df[label_col].values.tolist()
    except KeyError as e:
        print(f"❌ Column error: {e}")
        return

    print(f"📂 Loading private key to decrypt data for training: {key_name}")
    privkey = load_private_key(key_name)

    print("🔓 Decrypting dataset before training...")
    try:
        X_plain = np.array([[privkey.decrypt(val) for val in row] for row in X_enc])
        y_plain = np.array([privkey.decrypt(val) for val in y_enc])
    except Exception as e:
        print(f"❌ Failed to decrypt: {e}")
        return

    print("✅ Label distribution:", np.unique(y_plain, return_counts=True))
    if len(np.unique(y_plain)) < 2:
        print("❌ Need at least 2 classes in the dataset for training.")
        return

    print("🧠 Training model using decrypted values...")
    clf = LogisticRegression()
    clf.fit(X_plain, y_plain)

    print(f"💾 Saving trained model to: {output_model_path}")
    os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
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

def decrypt_dataset(encrypted_input_path, output_path, key_name):
    print(f"📂 Loading encrypted dataset from: {encrypted_input_path}")
    with open(encrypted_input_path, "rb") as f:
        enc_df = pickle.load(f)

    privkey = load_private_key(key_name)

    print("🔓 Decrypting dataset...")
    dec_df = enc_df.applymap(lambda x: privkey.decrypt(x))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"💾 Saving decrypted dataset to: {output_path}")
    dec_df.to_csv(output_path, index=False)
    print("✅ Dataset decrypted and saved successfully.")


def main():
    parser = argparse.ArgumentParser(description="Cifer Secure Training (named key version)")
    subparsers = parser.add_subparsers(dest="command")

    enc = subparsers.add_parser("encrypt-dataset", help="Encrypt a CSV dataset")
    enc.add_argument("--dataset", required=True)
    enc.add_argument("--output", required=True)
    enc.add_argument("--key", required=True)

    decdata = subparsers.add_parser("decrypt-dataset", help="Decrypt encrypted dataset")
    decdata.add_argument("--input", required=True)
    decdata.add_argument("--output", required=True)
    decdata.add_argument("--key", required=True)

    train = subparsers.add_parser("train", help="Train model on encrypted data")
    train.add_argument("--encrypted-data", required=True)
    train.add_argument("--output-model", required=True)
    train.add_argument("--key", required=True)
    train.add_argument("--features", nargs="+", help="Feature column names", required=True)
    train.add_argument("--label", help="Label column name", required=True)

    dec = subparsers.add_parser("decrypt-model", help="Decrypt model")
    dec.add_argument("--input-model", required=True)
    dec.add_argument("--output-model", required=True)
    dec.add_argument("--key", required=True)

    args = parser.parse_args()
    if args.command == "encrypt-dataset":
        encrypt_dataset(args.dataset, args.output, args.key)
    elif args.command == "decrypt-dataset":
        decrypt_dataset(args.input, args.output, args.key)  # ✅ เพิ่มตรงนี้
    elif args.command == "train":
        train_model(
            args.encrypted_data,
            args.output_model,
            args.key,
            args.features,
            args.label)
    elif args.command == "decrypt-model":
        decrypt_model(args.input_model, args.output_model, args.key)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
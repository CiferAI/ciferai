import argparse
import os
import pickle
import requests
import pandas as pd
import numpy as np
from io import BytesIO
from phe import paillier
from sklearn.linear_model import LogisticRegression
from tensorflow.keras.models import load_model, save_model
from tqdm import tqdm
import subprocess
import uuid

def is_github_repo(url):
    return url.startswith("https://github.com/") and not url.endswith(".csv")

def clone_github_repo(url, suffix="repo"):
    print(f"🐙 Cloning GitHub repo: {url}")
    repo_id = str(uuid.uuid4())[:8]
    target_dir = f"temp_download/github_{suffix}_{repo_id}"
    try:
        subprocess.run(["git", "clone", "--depth", "1", url, target_dir], check=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("❌ Failed to clone GitHub repository.")
    return target_dir


def find_first_csv_file(directory):
    print(f"🔍 Searching for CSV in: {directory}")
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                csv_path = os.path.join(root, file)
                print(f"✅ Found CSV: {csv_path}")
                return csv_path
    raise FileNotFoundError("❌ No CSV file found in the GitHub repository.")


# def resolve_local_path(path_or_url, suffix="tmp"):
#     """
#     If path_or_url is a URL, download it and return the local temporary path.
#     Otherwise, return the original path.
#     """
#     if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
#         print(f"🌐 Downloading from URL: {path_or_url}")
#         response = requests.get(path_or_url, stream=True)
#         total_size = int(response.headers.get('content-length', 0))

#         os.makedirs("temp_download", exist_ok=True)
#         filename = os.path.join("temp_download", f"{suffix}_{os.path.basename(path_or_url).split('?')[0]}")

#         with open(filename, "wb") as f, tqdm(
#             desc=f"⬇️  Saving to {filename}",
#             total=total_size,
#             unit='B',
#             unit_scale=True,
#             unit_divisor=1024,
#         ) as bar:
#             for chunk in response.iter_content(chunk_size=8192):
#                 if chunk:
#                     f.write(chunk)
#                     bar.update(len(chunk))

#         print(f"✅ Download completed: {filename}")
#         return filename

#     return path_or_url

def resolve_local_path(path_or_url, suffix="tmp"):
    if is_github_repo(path_or_url):
        cloned_dir = clone_github_repo(path_or_url, suffix=suffix)
        return find_first_csv_file(cloned_dir)

    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        print(f"🌐 Downloading from URL: {path_or_url}")
        response = requests.get(path_or_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        os.makedirs("temp_download", exist_ok=True)
        filename = os.path.join("temp_download", f"{suffix}_{os.path.basename(path_or_url).split('?')[0]}")
        with open(filename, "wb") as f, tqdm(
            desc=f"⬇️  Saving to {filename}",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
        print(f"✅ Download completed: {filename}")
        return filename

    return path_or_url




def cleanup_temp_files():
    """Remove temp_download folder if exists"""
    import shutil
    if os.path.exists("temp_download"):
        shutil.rmtree("temp_download")


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
    path = os.path.join("keys", key_name, "private.key")
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

    # ตรวจจับคอลัมน์ตัวเลข
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    print(f"🧮 Detected numeric columns: {numeric_cols}")

    pubkey, _ = generate_named_keys(key_name)

    print("🔐 Encrypting numeric columns...")
    df_encrypted = df.copy()
    for col in numeric_cols:
        df_encrypted[col] = df_encrypted[col].apply(lambda x: pubkey.encrypt(x))

    # ✅ บันทึกเป็น DataFrame (ไม่ใช้ dict)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        pickle.dump(df_encrypted, f)

    print(f"✅ Dataset encrypted and saved successfully to: {output_path}")


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

def encrypt_model(input_model_path, output_model_path, key_name):
    print(f"📂 Loading plain model from: {input_model_path}")
    with open(input_model_path, "rb") as f:
        model = pickle.load(f)

    pubkey = load_public_key(key_name)

    print("🔐 Encrypting model coefficients...")
    encrypted_coef = []
    for coef in model.coef_[0]:
        try:
            val = pubkey.encrypt(coef)
        except Exception:
            val = coef
        encrypted_coef.append(val)

    model.coef_ = [encrypted_coef]
    os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
    with open(output_model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"✅ Encrypted model saved to: {output_model_path}")


def decrypt_dataset(input_path, output_path, key_name):
    print(f"📂 Loading encrypted dataset from: {input_path}")
    with open(input_path, "rb") as f:
        enc_df = pickle.load(f)

    if not isinstance(enc_df, pd.DataFrame):
        raise ValueError("❌ Encrypted file does not contain a pandas DataFrame. Got: " + str(type(enc_df)))

    privkey = load_private_key(key_name)  # ✅ FIXED

    print("🔓 Decrypting dataset...")

    dec_df = enc_df.copy()
    for col in dec_df.columns:
        dec_df[col] = dec_df[col].apply(lambda x: privkey.decrypt(x) if hasattr(x, 'ciphertext') else x)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    dec_df.to_csv(output_path, index=False)
    print(f"✅ Dataset decrypted and saved successfully to: {output_path}")


def decrypt_dataset(input_path, output_path, key_name):
    print(f"📂 Loading encrypted dataset from: {input_path}")
    with open(input_path, "rb") as f:
        enc_df = pickle.load(f)

    if not isinstance(enc_df, pd.DataFrame):
        raise ValueError("❌ Encrypted file does not contain a pandas DataFrame. Got: " + str(type(enc_df)))

    privkey = load_private_key(key_name)

    print("🔓 Decrypting dataset...")

    dec_df = enc_df.copy()
    for col in dec_df.columns:
        dec_df[col] = dec_df[col].apply(lambda x: privkey.decrypt(x) if hasattr(x, 'ciphertext') else x)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    dec_df.to_csv(output_path, index=False)
    print(f"✅ Dataset decrypted and saved successfully to: {output_path}")

def encrypt_keras_model(input_path, output_path, key_name):
    print(f"📂 Loading Keras model from: {input_path}")
    model = load_model(input_path)

    pubkey = load_public_key(key_name)

    print("🔐 Encrypting model weights...")
    weights = model.get_weights()
    encrypted_weights = [
        np.vectorize(lambda x: pubkey.encrypt(float(x)))(w) for w in weights
    ]

    model.set_weights(encrypted_weights)

    print(f"💾 Saving encrypted Keras model to: {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    model.save(output_path)
    print("✅ Keras model encrypted and saved.")

def decrypt_keras_model(input_path, output_path, key_name):
    print(f"📂 Loading encrypted Keras model from: {input_path}")
    model = load_model(input_path)

    privkey = load_private_key(key_name)

    print("🔓 Decrypting model weights...")
    encrypted_weights = model.get_weights()
    decrypted_weights = [
        np.vectorize(lambda x: privkey.decrypt(x) if hasattr(x, 'ciphertext') else x)(w)
        for w in encrypted_weights
    ]

    model.set_weights(decrypted_weights)

    print(f"💾 Saving decrypted Keras model to: {output_path}")
    model.save(output_path)
    print("✅ Decrypted Keras model saved.")

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

    encrypt_model_parser = subparsers.add_parser("encrypt-model", help="Encrypt model from external source")
    encrypt_model_parser.add_argument("--input-model", required=True)
    encrypt_model_parser.add_argument("--output-model", required=True)
    encrypt_model_parser.add_argument("--key", required=True)


    keras_enc = subparsers.add_parser("encrypt-keras-model", help="Encrypt a Keras .h5 model")
    keras_enc.add_argument("--input-model", required=True)
    keras_enc.add_argument("--output-model", required=True)
    keras_enc.add_argument("--key", required=True)

    keras_dec = subparsers.add_parser("decrypt-keras-model", help="Decrypt a Keras .h5 model")
    keras_dec.add_argument("--input-model", required=True)
    keras_dec.add_argument("--output-model", required=True)
    keras_dec.add_argument("--key", required=True)

    args = parser.parse_args()
    # if args.command == "encrypt-dataset":
    #     encrypt_dataset(args.dataset, args.output, args.key)
    # elif args.command == "decrypt-dataset":
    #     decrypt_dataset(args.input, args.output, args.key)  # ✅ เพิ่มตรงนี้
    # elif args.command == "encrypt-model":
    #     encrypt_model(args.input_model, args.output_model, args.key)
    # elif args.command == "train":
    #     train_model(
    #         args.encrypted_data,
    #         args.output_model,
    #         args.key,
    #         args.features,
    #         args.label)
    # elif args.command == "decrypt-model":
    #     decrypt_model(args.input_model, args.output_model, args.key)
    # elif args.command == "encrypt-keras-model":
    #     encrypt_keras_model(args.input_model, args.output_model, args.key)
    # elif args.command == "decrypt-keras-model":
    #     decrypt_keras_model(args.input_model, args.output_model, args.key)
    if args.command == "encrypt-dataset":
        dataset_path = resolve_local_path(args.dataset, suffix="dataset")
        encrypt_dataset(dataset_path, args.output, args.key)
        cleanup_temp_files()

    elif args.command == "decrypt-dataset":
        input_path = resolve_local_path(args.input, suffix="encdata")
        decrypt_dataset(input_path, args.output, args.key)
        cleanup_temp_files()

    elif args.command == "encrypt-model":
        input_path = resolve_local_path(args.input_model, suffix="model")
        encrypt_model(input_path, args.output_model, args.key)
        cleanup_temp_files()

    elif args.command == "decrypt-model":
        input_path = resolve_local_path(args.input_model, suffix="model")
        decrypt_model(input_path, args.output_model, args.key)
        cleanup_temp_files()

    elif args.command == "encrypt-keras-model":
        input_path = resolve_local_path(args.input_model, suffix="keras")
        encrypt_keras_model(input_path, args.output_model, args.key)
        cleanup_temp_files()

    elif args.command == "decrypt-keras-model":
        input_path = resolve_local_path(args.input_model, suffix="keras")
        decrypt_keras_model(input_path, args.output_model, args.key)
        cleanup_temp_files()

    elif args.command == "train":
        encrypted_path = resolve_local_path(args.encrypted_data, suffix="train")
        train_model(encrypted_path, args.output_model, args.key, args.features, args.label)
        cleanup_temp_files()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
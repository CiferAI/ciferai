Cifer-Fraud-Detection
1. dataset 
-encrypt-dataset
python -m cifer.securetrain encrypt-dataset \
  --dataset "datasets/decrypted_cifer_part1.csv" \
  --output datasets/encrypted_cifer_part1.pkl \
  --key alice

-decrypt-dataset
python -m cifer.securetrain decrypt-dataset \
  --input datasets/encrypted_cifer_part1.pkl \
  --output datasets/decrypted_cifer_part2.csv \
  --key alice

2. เทรนโมเดล (train)
python -m cifer.securetrain train \
  --encrypted-data datasets/encrypted_cifer_part1.pkl \
  --output-model models/encrypted_model_part1.pkl \
  --key alice \
  --features step amount oldbalanceOrg newbalanceOrig oldbalanceDest newbalanceDest \
  --label isFraud

3. เข้าหัสโมเดล (encrypt-model)
python -m cifer.securetrain encrypt-model \
  --input-model models/plain_model.pkl \
  --output-model models/encrypted_from_external.pkl \
  --key alice


3. ถอดรหัสโมเดล (decrypt-model)
python -m cifer.securetrain decrypt-model \
  --input-model models/encrypted_model_part1.pkl \
  --output-model models/decrypted_model_part1.pkl \
  --key alice


| พารามิเตอร์ | คำอธิบาย                                                           |
| ----------- | -------------------------------------------------------------   |
| `--input`   | ไฟล์ `.pkl` ที่เป็น dataset ที่ถูกเข้ารหัสไว้                             |
| `--output`  | Path สำหรับบันทึกไฟล์ CSV ที่ถอดรหัสแล้ว                                 |
| `--key`     | ชื่อ key ที่ใช้ในการถอดรหัส (ต้องมี `keys/alice/private.key`)           |


mixed_dummy_data
เข้ารหัส Dataset
python -m cifer.securetrain encrypt-dataset \
  --dataset datasets/mixed_dummy_data.csv \
  --output datasets/mixed_dummy_data.pkl \
  --key alice

ถอดรหัส Dataset
python -m cifer.securetrain decrypt-dataset \
  --input datasets/mixed_dummy_data.pkl \
  --output datasets/mixed_dummy_data.csv \
  --key alice

เทรนโมเดลจาก Dataset ที่เข้ารหัสแล้ว
python -m cifer.securetrain train \
  --encrypted-data datasets/mixed_dummy_data.pkl \
  --output-model models/mixed_dummy_data.pkl \
  --key alice \
  --features user_id age gender country amount is_premium \
  --label is_premium

 ถอดรหัสโมเดลหลังเทรน
 python -m cifer.securetrain decrypt-model \
  --input-model models/mixed_dummy_data.pkl \
  --output-model models/mixed_dummy_data_decrypt.pkl \
  --key alice



# Encrypt
python -m cifer.securetrain encrypt-keras-model \
  --input-model models/my_model.h5 \
  --output-model models/my_model_encrypted.h5 \
  --key alice

# Decrypt
python -m cifer.securetrain decrypt-keras-model \
  --input-model models/my_model_encrypted.h5 \
  --output-model models/my_model_decrypted.h5 \
  --key alice

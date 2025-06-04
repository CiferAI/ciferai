1. dataset 
-encrypt-dataset
python -m cifer.securetrain encrypt-dataset \
  --dataset "https://huggingface.co/datasets/CiferAI/Cifer-Fraud-Detection-Dataset-AF/resolve/main/part-1-14.csv" \
  --output datasets/encrypted_cifer_part1.pkl \
  --key alice

-decrypt-dataset
python -m cifer.securetrain decrypt-dataset \
  --input datasets/encrypted_cifer_part1.pkl \
  --output datasets/decrypted_cifer_part1.csv \
  --key alice

2. เทรนโมเดล (train)
python -m cifer.securetrain train \
  --encrypted-data datasets/encrypted_cifer_part1.pkl \
  --output-model models/encrypted_model_part1.pkl \
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



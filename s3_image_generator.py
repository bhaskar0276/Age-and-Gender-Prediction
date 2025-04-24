from s3_connector import s3
from PIL import Image
import numpy as np
from io import BytesIO
from tensorflow.keras.utils import Sequence
from urllib.parse import urlparse

class S3ImageGenerator(Sequence):
    def __init__(self, df, batch_size=32, target_size=(200, 200), shuffle=True):
        self.df = df.reset_index(drop=True)
        self.batch_size = batch_size
        self.target_size = target_size
        self.shuffle = shuffle
        self.s3 = s3
        self.indexes = np.arange(len(self.df))
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.df) / self.batch_size))

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __getitem__(self, idx):
        indexes = self.indexes[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch = self.df.iloc[indexes]

        X, y_age, y_gender = [], [], []

        for _, row in batch.iterrows():
            img_path = row.get('img', '')
            if not isinstance(img_path, str) or not img_path.startswith("s3://"):
                print(f"Skipping invalid S3 path: {img_path}")
                continue

            parsed = urlparse(img_path)
            bucket = parsed.netloc
            key = parsed.path.lstrip('/')

            if not bucket or not key:
                print(f"Skipping row: Missing bucket/key in path → {img_path}")
                continue

            try:
                obj = self.s3.get_object(Bucket=bucket, Key=key)
                img = Image.open(BytesIO(obj['Body'].read())).resize(self.target_size)
                img = np.asarray(img) / 255.0

                if img.shape[-1] == 4:
                    img = img[:, :, :3]

                X.append(img)
                y_age.append(row['age'])
                y_gender.append(row['gender'])

            except Exception as e:
                print(f" Failed to load image from {img_path}: {e}")
                continue

        return np.array(X), {
            'age': np.array(y_age, dtype=np.float32),
            'gender': np.array(y_gender, dtype=np.float32)
        }

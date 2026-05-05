# Image Restoration - MP1

## Nama
Rayyan Fathanza  
NRP: 5024241056

---

## Deskripsi
Tugas ini bertujuan untuk merestorasi citra Lena yang mengalami:
- Gaussian noise
- Salt-and-pepper noise
- Blur
- Low contrast

---

## Pipeline Restorasi

Pipeline yang digunakan terdiri dari beberapa tahap:

### 1. Median Filtering
Dilakukan sebanyak dua kali dengan kernel 5x5 untuk menghilangkan salt-and-pepper noise secara efektif.

### 2. Gaussian Filtering
Menggunakan kernel 7x7 untuk mereduksi Gaussian noise dan menghaluskan citra.

### 3. Smoothing Tambahan
Filtering tambahan untuk mengurangi noise residual yang masih tersisa.

### 4. Histogram Equalization (Soft)
Dilakukan dengan teknik blending untuk meningkatkan kontras tanpa memperkuat noise secara berlebihan.

### 5. Sharpening (Unsharp Masking)
Digunakan untuk mengembalikan detail citra, namun dengan intensitas rendah agar tidak memperkuat noise.

### 6. Color Quantization (Opsional)
Digunakan untuk mengurangi noise warna pada citra hasil.

---

## Hasil

### Sebelum
![before](input/test_image_lena_noisy.png)

### Sesudah
![after](output/lena_restored.png)

---

## Analisis

### Yang Berhasil:
- Noise salt-and-pepper berhasil dihilangkan
- Gaussian noise berkurang signifikan
- Citra menjadi lebih halus
- Warna tetap terjaga

### Kekurangan:
- Detail halus sedikit berkurang akibat smoothing yang kuat
- Tidak sepenuhnya sama dengan citra referensi karena noise sangat tinggi

---

## Cara Menjalankan

```bash
python restoration.py
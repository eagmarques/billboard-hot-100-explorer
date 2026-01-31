import kagglehub

# Download do dataset
path = kagglehub.dataset_download("thedevastator/billboard-hot-100-audio-features")
print("Path to dataset files:", path)
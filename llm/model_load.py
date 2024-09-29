from huggingface_hub import snapshot_download
# from modelscope import snapshot_download
model_dir = snapshot_download('TencentBAC/Conan-embedding-v1', cache_dir='/sdc/model')
env __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia vllm serve Qwen/Qwen3-0.6B \--host 127.0.0.1 --port 8000 \--dtype float16 \--gpu-memory-utilization 0.85 \--max-model-len 2048


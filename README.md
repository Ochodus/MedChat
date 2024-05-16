# Medical Chatbot with llama3
Cutting-edge medical chatbot model, powered by the llama3 platform and leveraging Prompt Engineering alongside the RAG (Retrieval-Augmented Generation) technique. This innovative approach revolutionizes the way medical inquiries are handled, offering a seamless and efficient interaction experience for both patients and healthcare providers.

## Quick Start

1. Clone and download this repository in a conda env with PyTorch / CUDA.

2. In the top-level directory run:
    ```bash
    pip install -e .
    ```
3. Execute chatbot server with streamlit
```bash
streamlit run app.py -- --model llama3:70b-instruct-q8_0 --prompt ollama_llama3 --translator deepL --max_q 10
```
4. Enter api key on terminal if using deepL translator 

**Note**
- Replace  `--model llama3:70b-instruct-q8_0` with the id of ollama models. It is also available to use huggingface models.
- max_q means the number of questions that allow to chatbot before diagnosing.
- You need to download ollama model to local first to use it by
```bash
ollama pull llama3:70b-instruct-q8_0
```

## License

Our model and weights are licensed for researchers and commercial entities, upholding the principles of openness. Our mission is to empower individuals and industry through this opportunity while fostering an environment of discovery and ethical AI advancements.

See the [LICENSE](LICENSE) file, as well as our accompanying [Acceptable Use Policy](USE_POLICY.md)

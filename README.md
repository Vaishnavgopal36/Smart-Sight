# **Smart Sight** <span style="font-size: rem; color: gray;"> — Discover, Search, and Navigate</span>


Welcome to the **Multimodal Search Chatbot** project! This is an advanced chatbot capable of processing **image**, **text**, and **multimodal (image + text)** inputs to provide intelligent and context-aware responses. Powered by **OpenAI's CLIP model**, **FAISS vector database**, and **LLM-based refinement**, this chatbot delivers a seamless and interactive user experience.

---

## 🎯 Features

- **Multimodal Input Support**: Accepts **image**, **text**, or **image + text** inputs.
- **CLIP Model Integration**: Leverages OpenAI's CLIP for generating embeddings.
- **FAISS Vector Database**: Efficiently stores and retrieves embeddings for fast search.
- **Web Scraping**: Performs Google searches to enhance response quality.
- **LLM-Powered Refinement**: Uses a Large Language Model to parse and refine results.
- **Dynamic Response Generation**: Returns **text**, **images**, or **both** based on user queries.

---

## 📊 Diagrams
### High-Level System Design  
![High-Level System Design](./High_Level_System_Design.png)

---
## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- OpenAI CLIP model
- FAISS library
- Google Search API (for web scraping)
- LLM (e.g., Gemini)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/multimodal-search-chatbot.git
   cd multimodal-search-chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   export GOOGLE_SEARCH_API_KEY="your_google_search_api_key"
   ```

4. Run the chatbot:
   ```bash
   python main.py
   ```

---

## 📂 Project Structure

```
multimodal-search-chatbot/
├── main.py                # Entry point for the chatbot
├── requirements.txt       # List of dependencies
├── README.md              # Project documentation
├── diagrams/              # Diagrams (system design, data flow, etc.)
├── modules/               # Core modules
│   ├── input_parsers.py   # Handles image, text, and multimodal inputs
│   ├── clip_model.py      # Generates embeddings using CLIP
│   ├── faiss_db.py        # Manages FAISS vector database
│   ├── web_scraper.py     # Performs Google searches
│   ├── llm.py             # Parses and refines results using LLM
│   └── response_gen.py    # Generates final responses
└── tests/                 # Unit and integration tests
```

---


## 🧩 Modules

### 1. Input Parsers
- **Image Parser**: Processes image inputs.
- **Text Parser**: Processes text inputs.
- **Multimodal Parser**: Handles combined image + text inputs.

### 2. CLIP Model
- Generates embeddings for images, text, and multimodal inputs.

### 3. FAISS Vector Database
- Stores and retrieves embeddings for efficient search.

### 4. Web Scraper
- Performs Google searches based on retrieved results.

### 5. LLM
- Parses and refines scraped results to generate meaningful responses.

### 6. Response Generator
- Formats the final output (text, images, or both).

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenAI for the CLIP model.
- Facebook AI Research (FAIR) for FAISS.
- Google for the Search API.

---

Made with ❤️ by Smart Sight

# Myanmar Agri-Med AI: Multilingual RAG System

**A Retrieval-Augmented Generation (RAG) platform designed for rural accessibility in Myanmar.**

----------

## 📌 Project Overview

The **Myanmar Agri-Med AI** is a specialized chatbot built to provide verified information in the Burmese language for two critical domains: **Agriculture** and **Medicine**.

Unlike standard LLMs that may hallucinate, this system uses **Retrieval-Augmented Generation (RAG)**. It maps user queries to a high-dimensional vector space and retrieves answers only from a curated, expert-verified knowledge base.

----------

## 🚀 Key Features

-   **Dual-Domain Logic:** Seamlessly toggle between Agricultural and Medical databases.
    
-   **Multilingual Embeddings:** Utilizes a fine-tuned `paraphrase-multilingual-MiniLM-L12-v2` transformer for high-accuracy Burmese semantic search.
    
-   **Safety Guardrails:** * **Similarity Thresholding:** Rejects queries with a Euclidean distance $> 15.0$ to prevent misinformation.
    
    -   **Ethical Injection:** Automatic medical disclaimers on all health-related responses.
        
-   **Resource Efficiency:** Optimized for low-bandwidth environments in rural Myanmar.
    

----------

## 🛠️ Technical Stack

-   **Frontend:** Streamlit
    
-   **Vector Database:** Meta FAISS (Facebook AI Similarity Search)
    
-   **Embedding Model:** Sentence-Transformers (HuggingFace)
    
-   **Deployment:** Git LFS (Large File Storage) + Streamlit Community Cloud / Vercel
    

----------

## 📂 Project Structure

Plaintext

```
├── my_project_data/
│   ├── fine_tuned_burmese_model/  # Model weights and config
│   ├── agriculture_faiss.index   # Vectorized agri-knowledge
│   ├── medicine_faiss.index      # Vectorized medical-knowledge
│   ├── agriculture_answers.pkl   # Agri-answer bank
│   └── medicine_answers.pkl      # Medical-answer bank
├── streamlit_app.py              # Main application logic
├── Master_Notebook.ipynb         # Data preprocessing & training pipeline
├── requirements.txt              # Dependencies
└── vercel.json                  # Deployment configuration

```

----------

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    
    Bash
    
    ```
    git clone https://github.com/PhoneMinKhant203/MM_AI.git
    cd MM_AI
    
    ```
    
2.  **Install Git LFS (Required for Model/Index files):**
    
    Bash
    
    ```
    git lfs install
    git lfs pull
    
    ```
    
3.  **Install dependencies:**
    
    Bash
    
    ```
    pip install -r requirements.txt
    
    ```
    
4.  **Run the application:**
    
    Bash
    
    ```
    streamlit run streamlit_app.py
    
    ```
    

----------

## ⚖️ Ethical Considerations

This tool is an **Information Retrieval System**, not a diagnostic tool. In compliance with AI Ethics standards:

1.  All medical queries include a mandatory disclaimer.
    
2.  The system is designed to "fail-safe" by refusing to answer rather than providing a low-confidence guess.
    
3.  No personal user data is stored; session history is cleared upon refresh.
    

----------

## 👤 Author

**Phone Min Khant** 

_Focus: AI for Social Impact & Multilingual NLP_

    

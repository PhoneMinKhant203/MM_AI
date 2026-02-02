import streamlit as st
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import datetime 


st.set_page_config(page_title="Myanmar AI Chatbot", page_icon="🤖")


SIMILARITY_THRESHOLD = 15.0 
MEDICAL_DISCLAIMER = "ဤအချက်အလက်သည် အထွေထွေ သိရှိရန်သာဖြစ်ပြီး ဆရာဝန်အစား မဖြစ်ပါ။"

# LOAD EMBEDDING MODEL
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("./fine_tuned_burmese_model")

embed_model = load_embedding_model()


# LOAD FAISS DATA
@st.cache_resource
def load_medicine():
    index = faiss.read_index("medicine_faiss.index")
    with open("medicine_answers.pkl", "rb") as f:
        answers = pickle.load(f)
    return index, answers

@st.cache_resource
def load_agriculture():
    index = faiss.read_index("agriculture_faiss.index")
    with open("agriculture_answers.pkl", "rb") as f:
        answers = pickle.load(f)
    return index, answers

med_index, med_answers = load_medicine()
agri_index, agri_answers = load_agriculture()


# HELPER FUNCTIONS
def search_faiss(query, index, answers):
    q_vec = embed_model.encode([query])
    D, I = index.search(q_vec, 1)
    
    idx = I[0][0]
    if idx == -1:
        return 999, "Error: Index out of bounds"
        
    return D[0][0], answers[idx]

def check_greeting(text):
    greetings = ["hi", "hello", "hey", "mingalabar", "မင်္ဂလာပါ", "နေကောင်းလား"]
    for w in greetings:
        if w in text.lower():
            return True
    return False


# STREAMLIT UI
st.title("Myanmar Agri-Med AI")
st.caption("Fine-Tuned Retrieval Augmented Generation (RAG) System")

# SIDEBAR CONTROLS
with st.sidebar:
    st.header("Setting")
    domain = st.selectbox("Choose domain", ["Medicine","Agriculture"])
    
    # Button to Clear History
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    # Button to Download History
    # Combine all messages into one long text string
    chat_text = "Myanmar AI Chatbot - Conversation Log\n"
    chat_text += f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    chat_text += "="*40 + "\n\n"
    
    if "messages" in st.session_state:
        for msg in st.session_state.messages:
            role = "USER" if msg["role"] == "user" else "AI"
            chat_text += f"{role}: {msg['content']}\n\n"
            
    st.download_button(
        label="📥 Download",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )

# CHAT LOGIC

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Enter your question (Burmese)..."):
    
    # Show User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Response
    response = ""
    
    if check_greeting(prompt):
        response = "မင်္ဂလာပါခင်ဗျာ! ကျွန်တော်က ကျန်းမာရေးနဲ့ စိုက်ပျိုးရေးဆိုင်ရာ အကူအညီပေးတဲ့ AI ပါ။ ဘာများကူညီပေးရမလဲ?"
    else:
        if domain == "Medicine":
            dist, answer = search_faiss(prompt, med_index, med_answers)
        else:
            dist, answer = search_faiss(prompt, agri_index, agri_answers)

        if dist <= SIMILARITY_THRESHOLD:
            response = answer
            if domain == "Medicine":
                response += f"\n\n_({MEDICAL_DISCLAIMER})_"
        else:
            response = "တောင်းပန်ပါတယ်၊ အဲဒီအကြောင်းအရာနဲ့ ပတ်သက်ပြီး ကျွန်တော့် ဒေတာထဲမှာ မတွေ့ပါဘူး။"

    # Show Assistant Message
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
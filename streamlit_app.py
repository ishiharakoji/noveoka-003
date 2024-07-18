import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("ノベオカ AIアシスタント")
st.write("AIがあなたの質問にお応えします。")

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai_api_key = st.secrets.OpenAIAPI.openai_api_key

# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

system_prompt = """
あなたは優秀な英語を教える講師です。
英作文や英会話、リスニングやリーディングなど、生徒の要望に合わせて英語の上達のためのアドバイスを行ってください。
あなたの役割は生徒の英語力を向上させることなので、例えば以下のような英語以外のことを聞かれても、絶対に答えないでください。
* 旅行
* 芸能人
* 映画
* 科学
* 歴史
* 政治
* 戦争
"""

if "system_messages" not in st.session_state:
    st.session_state.system_messages = [
        {"role": "system", "content": system_prompt}
        ]
    
# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("ここに質問を入力してください"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        system_messages=system_messages
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
from dotenv import load_dotenv
import os
import html
import re
import base64
from google import genai


# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY is missing in your .env file")
    st.stop()

client = genai.Client(api_key=api_key)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🌸",
    layout="centered"
)


# =========================================================
# IMAGE PATH
# =========================================================

# CHANGE THIS TO YOUR FLOWER IMAGE PATH

image_file = r"C:\Users\K NANDINI\OneDrive\Desktop\flower_bg.png"


# =========================================================
# LOAD IMAGE
# =========================================================

if os.path.exists(image_file):

    with open(image_file, "rb") as file:
        image_data = base64.b64encode(file.read()).decode()

    background_image = f"data:image/png;base64,{image_data}"

else:

    background_image = ""


# =========================================================
# CSS
# =========================================================

st.markdown(
    f"""
<style>


/* =====================================================
   FLOWER IMAGE BACKGROUND
===================================================== */

.stApp {{

    min-height: 100vh;

    background-image:
        linear-gradient(
            rgba(25, 25, 70, 0.25),
            rgba(25, 25, 70, 0.25)
        ),
        url("{background_image}");

    background-size: cover;

    background-position: center;

    background-repeat: no-repeat;

    background-attachment: fixed;

    overflow-x: hidden;
}}


/* =====================================================
   MAIN CONTENT
===================================================== */

.block-container {{

    max-width: 850px;

    padding-top: 30px;

    padding-bottom: 40px;

    position: relative;

    z-index: 5;
}}


/* =====================================================
   ROBOT
===================================================== */

.robot {{

    text-align: center;

    font-size: 58px;

    margin-bottom: 5px;

    filter:
        drop-shadow(0 0 8px white)
        drop-shadow(0 0 20px #ff1493);

    animation: robotFloat 3s ease-in-out infinite;
}}


@keyframes robotFloat {{

    0%, 100% {{
        transform: translateY(0);
    }}

    50% {{
        transform: translateY(-10px);
    }}
}}


/* =====================================================
   TITLE
===================================================== */

.title {{

    text-align: center;

    font-size: 46px;

    font-weight: 900;

    color: white;

    text-shadow:
        0 3px 8px rgba(0,0,0,0.95),
        0 0 15px #ff1493,
        0 0 30px #7b2cff;

    margin-bottom: 8px;
}}


/* =====================================================
   SUBTITLE
===================================================== */

.subtitle {{

    text-align: center;

    color: white;

    font-size: 18px;

    font-weight: 800;

    margin-top: 8px;

    margin-bottom: 30px;

    text-shadow:
        0 2px 7px rgba(0,0,0,0.95);
}}


/* =====================================================
   LABEL
===================================================== */

label {{

    color: white !important;

    font-size: 18px !important;

    font-weight: 900 !important;

    text-shadow:
        0 2px 6px black;
}}


/* =====================================================
   QUESTION BOX
===================================================== */

textarea {{

    background: rgba(255,255,255,0.88) !important;

    color: #111827 !important;

    border: 3px solid white !important;

    border-radius: 18px !important;

    padding: 14px !important;

    font-size: 17px !important;

    font-weight: 600 !important;

    box-shadow:
        0 6px 20px rgba(0,0,0,0.40),
        0 0 20px rgba(255,20,147,0.70);

    backdrop-filter: blur(10px);

    -webkit-backdrop-filter: blur(10px);

    transition: 0.3s;
}}


textarea::placeholder {{

    color: #374151 !important;

    opacity: 1 !important;
}}


textarea:focus {{

    background: rgba(255,255,255,0.96) !important;

    border-color: #ff1493 !important;

    box-shadow:
        0 0 15px #ff1493,
        0 0 35px #7b2cff;
}}


/* =====================================================
   BUTTON
===================================================== */

.stButton > button {{

    width: 100%;

    height: 55px;

    margin-top: 12px;

    border: 3px solid white;

    border-radius: 18px;

    color: white;

    font-size: 18px;

    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #ff1493,
            #7b2cff,
            #008cff
        );

    box-shadow:
        0 6px 20px rgba(0,0,0,0.35),
        0 0 25px rgba(255,20,147,0.70);

    transition: 0.3s;
}}


.stButton > button:hover {{

    transform:
        translateY(-3px)
        scale(1.02);

    background:
        linear-gradient(
            90deg,
            #ff006e,
            #6a00ff,
            #00bfff
        );

    box-shadow:
        0 0 20px white,
        0 0 40px #ff1493;
}}


/* =====================================================
   ANSWER HEADING
===================================================== */

.answer-heading {{

    margin-top: 28px;

    padding: 16px 20px;

    border-radius: 18px;

    color: white;

    font-size: 22px;

    font-weight: 900;

    background:
        linear-gradient(
            90deg,
            #ff1493,
            #7b2cff,
            #008cff
        );

    border: 2px solid white;

    box-shadow:
        0 6px 25px rgba(0,0,0,0.40),
        0 0 25px rgba(255,20,147,0.70);

    text-shadow:
        0 2px 5px rgba(0,0,0,0.80);
}}


/* =====================================================
   ANSWER BOX
===================================================== */

.answer-box {{

    margin-top: 15px;

    padding: 22px;

    min-height: 70px;

    border-radius: 18px;

    background: rgba(255,255,255,0.90);

    color: #111827;

    font-size: 18px;

    font-weight: 600;

    line-height: 1.7;

    border: 3px solid white;

    box-shadow:
        0 6px 25px rgba(0,0,0,0.40),
        0 0 25px rgba(255,20,147,0.65);

    backdrop-filter: blur(12px);

    -webkit-backdrop-filter: blur(12px);

    word-wrap: break-word;

    overflow-wrap: break-word;
}}


/* =====================================================
   ANSWER BOLD TEXT
===================================================== */

.answer-box strong {{

    color: #6a00ff;

    font-weight: 900;
}}


/* =====================================================
   ERROR BOX
===================================================== */

.error-box {{

    margin-top: 20px;

    padding: 16px;

    border-radius: 16px;

    background: rgba(180,0,60,0.90);

    border: 2px solid white;

    color: white;

    font-weight: 800;

    box-shadow:
        0 0 20px rgba(255,0,80,0.70);
}}


/* =====================================================
   FOOTER
===================================================== */

.footer {{

    text-align: center;

    color: white;

    font-size: 14px;

    font-weight: 800;

    margin-top: 30px;

    text-shadow:
        0 2px 7px black;
}}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="robot">🤖</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="title">Gemini AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">🌈 Ask questions • Explore ideas • Discover answers ✨</div>',
    unsafe_allow_html=True
)


# =========================================================
# QUESTION
# =========================================================

prompt = st.text_area(
    "💬 Ask Gemini",
    placeholder="✨ Type your question here...",
    height=85
)


# =========================================================
# GENERATE RESPONSE
# =========================================================

if st.button("🚀 Generate AI Response"):

    if prompt.strip():

        response = None
        error_message = None

        # =================================================
        # FIRST MODEL
        # =================================================

        try:

            with st.spinner("🧠 Gemini is thinking... ✨"):

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

        except Exception:

            # =================================================
            # SECOND MODEL
            # =================================================

            try:

                with st.spinner("🔄 Trying Gemini Flash..."):

                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )

            except Exception as e:

                error_message = str(e)


        # =================================================
        # DISPLAY ANSWER
        # =================================================

        if response:

            answer = response.text

            # Escape HTML
            answer = html.escape(answer)

            # Convert **bold** text
            answer = re.sub(
                r"\*\*(.*?)\*\*",
                r"<strong>\1</strong>",
                answer
            )

            # Convert new lines
            answer = answer.replace("\n", "<br>")


            # =================================================
            # ANSWER HEADING + ANSWER BOX
            # =================================================

            st.markdown(
                f"""
                <div class="answer-heading">
                    🤖✨ Gemini's Answer
                </div>

                <div class="answer-box">
                    {answer}
                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # ERROR
        # =================================================

        elif error_message:

            st.markdown(
                f"""
                <div class="error-box">
                    ❌ Unable to generate the response.
                    <br><br>
                    🔄 Please try again.
                </div>
                """,
                unsafe_allow_html=True
            )


    else:

        st.warning("⚠️ Please enter a question first!")


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        🌸 Powered by Google Gemini
        &nbsp; • &nbsp;
        💻 Built with Streamlit
        &nbsp; • &nbsp;
        🚀 AI Technology

    </div>
    """,
    unsafe_allow_html=True
)
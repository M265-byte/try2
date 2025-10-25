import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import time

# -------------------- Helper Functions -------------------- #
def load_image(file_name):
    return Image.open(f"images/{file_name}")

def speech(text, speaker_img=None):
    col1, col2 = st.columns([1,4])
    if speaker_img:
        with col1:
            st.image(load_image(speaker_img), width=80)
        with col2:
            st.info(text)
    else:
        st.info(text)

# -------------------- Session State Init -------------------- #
if 'page' not in st.session_state: st.session_state.page = 'menu'
if 'character' not in st.session_state: st.session_state.character = None
if 'character_img' not in st.session_state: st.session_state.character_img = None
if 'score' not in st.session_state: st.session_state.score = 0
if 'hearts' not in st.session_state: st.session_state.hearts = 4
if 'pearl_question' not in st.session_state: st.session_state.pearl_question = 0
if 'crew_index' not in st.session_state: st.session_state.crew_index = 0
if 'quiz_index' not in st.session_state: st.session_state.quiz_index = 0
if 'start_time' not in st.session_state: st.session_state.start_time = None

# -------------------- Menu -------------------- #
if st.session_state.page == 'menu':
    st.image(load_image("background.png"))
    st.title("Welcome to Ancient Tales")
    if st.button("Enter"):
        st.session_state.page = 'login'

# -------------------- Login -------------------- #
elif st.session_state.page == 'login':
    st.image(load_image("background.png"))
    st.title("Login / Register")
    email = st.text_input("Enter your email")
    password = st.text_input("Create a password", type="password")
    verification = st.text_input("Enter verification code")
    if st.button("Verify"):
        if email and password and verification:
            st.session_state.page = 'character_select'

# -------------------- Character Selection -------------------- #
elif st.session_state.page == 'character_select':
    st.image(load_image("background.png"))
    st.title("Choose your character")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Nahyan"):
            st.session_state.character = "Nahyan"
            st.session_state.character_img = "nahyan.png"
            st.session_state.page = 'seacoast'
    with col2:
        if st.button("Dhabia"):
            st.session_state.character = "Dhabia"
            st.session_state.character_img = "dhabia.png"
            st.session_state.page = 'seacoast'

# -------------------- Seacoast Scene -------------------- #
elif st.session_state.page == 'seacoast':
    st.image(load_image("seacoast.png"))
    speech(f"Hello {st.session_state.character}, you see kids playing.", "robot.png")
    st.image(load_image("kids.png"), width=300)
    
    q1 = st.radio("Which game are the kids playing?", ("Tile", "Qubba", "Salam bil Aqaal", "Khusah bi Bousah"))
    if st.button("Submit Game Answer"):
        if q1 == "Tile":
            st.session_state.score += 1
        st.session_state.page = 'ship_intro'

# -------------------- Ship Intro Scene -------------------- #
elif st.session_state.page == 'ship_intro':
    st.image(load_image("ship.png"))
    st.title("Meet the Crew")
    crew = [
        ("Captain Naukhada", "Captain of the ship, leads the journey.", "naukhada.png"),
        ("Al-Ghais (Diver)", "Main pearl diver, strong and can hold breath long.", "ghais.png"),
        ("Al-Seeb (Puller)", "Pulls the diver up with rope.", "seeb.png"),
        ("Al-Nahham (Singer)", "Sings to motivate crew and keep rhythm.The song 'Ooh Ya Mal' is sung during pearl diving to motivate and communicate", "nahham.png"),
        ("Al-Jallas (Pearl Opener)", "Opens oysters carefully.", "jallas.png"),
        ("Al-Sukouni (Helmsman)", "Controls the rudder based on Captain orders.", "sukouni.png"),
        ("Al-Cook (Cook)", "Responsible for preparing meals.", "cook.png"),
        ("Al-Radif (Apprentice)", "Young trainee helping crew.", "radif.png")
    ]
    i = st.session_state.crew_index
    st.subheader(crew[i][0])
    st.write(crew[i][1])
    st.image(load_image(crew[i][2]), width=150)
    
    if st.button("Next Crew Member"):
        if i < len(crew)-1:
            st.session_state.crew_index += 1
        else:
            st.session_state.page = 'underwater'

# -------------------- Underwater Pearl Game with Timer & Hearts -------------------- #
elif st.session_state.page == 'underwater':
    st.image(load_image("underwater.png"))
    st.title("Pearl Diving Game")
    
    # Initialize timer
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    
    elapsed = int(time.time() - st.session_state.start_time)
    remaining_time = max(0, 120 - elapsed)  # 2 min countdown
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    st.write(f"Time Remaining: {minutes:02d}:{seconds:02d}")
    
    # Hearts update every 30 seconds
    hearts_lost = elapsed // 30
    st.session_state.hearts = max(0, 4 - hearts_lost)
    
    col1, col2 = st.columns([1,1])
    with col1:
        st.write("Hearts:")
        for i in range(st.session_state.hearts):
            st.image(load_image("heart_full.png"), width=30)
        for i in range(4 - st.session_state.hearts):
            st.image(load_image("heart_empty.png"), width=30)
    with col2:
        st.write(f"Score: {st.session_state.score}")
    
    if st.session_state.hearts <= 0 or remaining_time == 0:
        st.warning("You lost all your hearts!")
        if st.button("Restart the Pearl Game"):
            st.session_state.hearts = 4
            st.session_state.score = 0
            st.session_state.start_time = time.time()
        st.stop()
    
    # Canvas for movement placeholder
    st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=0,
        background_image=load_image("underwater.png"),
        width=600,
        height=400,
        drawing_mode="freedraw",
        key="canvas"
    )
    st.image(load_image(st.session_state.character_img), width=80)
    
    # Pearl buttons (4 pearls)
    pearl_positions = [(100,100), (250,150), (400,200), (350,300)]
    for idx in range(4):
        if st.button(f"Click Pearl {idx+1}"):
            st.session_state.pearl_question = idx
            st.session_state.page = 'pearl_question'

# -------------------- Pearl Questions -------------------- #
elif st.session_state.page == 'pearl_question':
    questions = [
        ("What is the knife used to open oysters called?", ["Sukaria", "Mafak", "Tasa"], "Sukaria"),
        ("Which pearl is large and pure white with slight pink or silver tint?", ["Danah", "Yaqooti", "Jiwan"], "Danah"),
        ("The smaller pearl, shiny like a ruby?", ["Yaqooti", "Yeka", "Mooz"], "Yaqooti"),
        ("The pearl with yellowish or light blue tint?", ["Batniyah", "Qimashi", "Raasiyah"], "Qimashi")
    ]
    idx = st.session_state.pearl_question
    q, options, ans = questions[idx]
    user_ans = st.radio(q, options)
    if st.button("Submit Answer"):
        if user_ans == ans: st.session_state.score += 1
        if idx < len(questions)-1:
            st.session_state.page = 'underwater'
        else:
            st.session_state.page = 'ship_quiz'

# -------------------- Ship Quiz Scene -------------------- #
elif st.session_state.page == 'ship_quiz':
    st.image(load_image("ship.png"))
    quizzes = [
        ("What is the Captain Naukhada’s role?", ["Captain / Leader", "Main Diver", "Puller"], "Captain / Leader"),
        ("What is Al-Nahham’s role?", ["Singer / Motivator", "Main Diver", "Pearl Opener", "Cook"], "Singer / Motivator"),
        ("Who controls the ship's rudder based on orders?", ["Radif", "Sukouni", "Nahham", "Seeb"], "Sukouni"),
        ("The song 'Ooh Ya Mal' is sung during…", ["Pearl Diving", "Fishing", "Exploration", "Short Trips"], "Pearl Diving"),
        ("Why was 'Ooh Ya Mal' sung?", ["To celebrate sea beauty", "To communicate and motivate", "No reason"], "To communicate and motivate")
    ]
    q_idx = st.session_state.quiz_index
    q, opts, ans = quizzes[q_idx]
    user_ans = st.radio(q, opts)
    if st.button("Submit Quiz Answer"):
        if user_ans == ans: st.session_state.score += 1
        if q_idx < len(quizzes)-1:
            st.session_state.quiz_index += 1
        else:
            st.session_state.page = 'ending'

# -------------------- Ending -------------------- #
elif st.session_state.page == 'ending':
    st.title("Congratulations!")
    st.write(f"Final Score: {st.session_state.score}")
    speech(f"The robot says: Well done {st.session_state.character}, you successfully completed the first stage!", "robot.png")
    st.balloons()
    if st.button("Restart Game from Beginning"):
        st.session_state.page = 'menu'
        st.session_state.character = None
        st.session_state.character_img = None
        st.session_state.score = 0
        st.session_state.hearts = 4
        st.session_state.crew_index = 0
        st.session_state.quiz_index = 0
        st.session_state.pearl_question = 0
        st.session_state.start_time = None

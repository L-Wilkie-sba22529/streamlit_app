import streamlit as st
from PIL import Image
import pandas as pd
from io import BytesIO
from streamlit_clickable_images import clickable_images
import ast
import numpy as np


icon_url = "assets/steam_icon.png"

st.set_page_config(
    page_title="Streamlit Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #171A21;
    }
    .custom-title {
        color: white;
        font-size: 2em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#### Loading data
df_weighted = pd.read_csv("dashboard_input/weighted_rating_filled.csv")
df_played = pd.read_csv("dashboard_input/game_list_df.csv", index_col="steam_id")
df_played["game_list"] = df_played["game_list"].apply(ast.literal_eval)
df_played['play_time_recommend'] = df_played['play_time_recommend'].fillna('[]')
df_played["play_time_recommend"] = df_played["play_time_recommend"].apply(ast.literal_eval)
top_game_list = set(df_weighted.id.unique())

games_df = pd.read_csv("dashboard_input/weighted_rating_expanded.csv", index_col="id")
#games_df["id"] = games_df["id"].astype(int)






# def select_user():
#     st.session_state.username = ''
#     st.session_state.user_games = ''


# def change_page(page):
#     st.session_state.page = page

st.session_state.valid = False



icon_url = "assets/steam_icon.png"



def validate_username(username):
    try:
        username = int(username)
        if 0 <= username <= 1180:
            return True, username
        else:
            return False, None
    except ValueError:
        return False, None
    

def evaluate_sidebar():
    st.sidebar.empty()
    if st.session_state.fresh:
        st.session_state.valid_user = False
        st.sidebar.image(icon_url, width=100)
        st.sidebar.write("Welcome to your Steam Overview")
        st.sidebar.write("Enter username or select new user below!")
        side_col1, side_col2 = st.sidebar.columns(2)
        with side_col1:
        #     st.button("New User", on_click=new_user, key="new_user_button")
        # with side_col2:
            st.button("Existing User", on_click=existing_user, key="existing_user_button")
    elif st.session_state.make_new_user:
        st.sidebar.image(icon_url, width=100)
        st.sidebar.write("Please select games you like.")
        st.sidebar.write("(will add this at the end)")
        st.sidebar.write("(needs quick exploration on which games to offer)")
        side_col1, side_col2 = st.sidebar.columns(2)
        with side_col1:
            st.button("Back", on_click=fresh_load, key="new_user_back")
    elif st.session_state.existing_user:
        st.sidebar.image(icon_url, width=100)
        st.sidebar.write("Enter your username to view your suggested content!")
        st.sidebar.write("(Usernames 0 - 1180 are available for this demonstration)")
        username = st.sidebar.text_input("Enter name:", key="username_input")
        side_col1, side_col2 = st.sidebar.columns(2)
        with side_col1:
            st.button("Back", on_click=fresh_load, key="exist_user_back")
        with side_col2:
            st.button("Enter", on_click=username_confirmed, key="exist_user_enter")
    elif st.session_state.incorrect_username:
        st.sidebar.image(icon_url, width=100)
        st.sidebar.write("Invalid username. Please enter a number between 1 and 1000.")
        side_col1, side_col2 = st.sidebar.columns(2)
        with side_col1:
            st.button("Ok", on_click=fresh_load, key="exist_user_back")
    elif st.session_state.username_confirmed:
        st.sidebar.image(icon_url, width=100)
        st.sidebar.write(f"Welcome steam_user#{st.session_state.username} to your steam review.")
        side_col1, side_col2 = st.sidebar.columns(2)
        with side_col1:
            st.button("Select New User", on_click=fresh_load, key="user_confirmed_back")


        ## selected game
        cc1, cc2, cc3 = st.columns(3)
        #click_cols = [cc1, cc2, cc3]

        # this can take the id of selected game and parse larger data when ready
        if 'selected_game' in st.session_state:
           #with cc1:
                #display_game_thumbnail(st.session_state.selected_game.url)
            with cc2:
                st.markdown(st.session_state.selected_game)
                st.markdown("TEST")
            # with cc3:
            #     display_game_thumbnail(st.session_state.selected_game.thumbnail)
        
        ### Weighted rating game ###
        # games in the users library are subtracted from this list 
        st.markdown('<h2 style="color:white;">Top rated games</h2>', unsafe_allow_html=True)
        st.markdown('<span style="color:white;">We think you\'ll like these popular games...</span>', unsafe_allow_html=True)

        
        # this could probably search with index, and save making tuples
        top_games = get_top_weighted()
        top_w1, top_w2, top_w3, top_w4, top_w5 = st.columns(5)
        top_w_cols = [top_w1, top_w2, top_w3, top_w4, top_w5]

        for i in range(len(top_games)):
            with top_w_cols[i]:
                display_game_thumbnail(
                    game_id=top_games[i][1], 
                    game_url=top_games[i][4], 
                    game_title=top_games[i][0].title(), 
                    game_price=top_games[i][3], 
                    game_desc=top_games[i][2]
                )


        ### Games based on your recent activity
        # not shown for new users
        # not shown for users with no games played

        recently_played_recommendations()


        ### Users like you based on reviews ###
()
                

        

def fresh_load():
    st.session_state.fresh = True
    st.session_state.make_new_user = False

class User():
    def __init__(self, username):
        self.username = username
        # self.owned_games = [219150, 212680, 620, 400, 48700]
        self.owned_games = list(df_played.iloc[username]["game_list"])
        if len(list(df_played.iloc[username]["play_time_recommend"]))>0:
            self.played_recommendations = list(df_played.iloc[username]["play_time_recommend"])
        else:
            self.played_recommendations  = ""
        self.user = username
    def get_owned_games(self):
        pass


class SelectedGame():
    def __init__(self, id):
        self.desc = games_df.loc[games_df['id'] == id, 'desc'].values[0]
        self.short_desc = games_df.loc[games_df['id'] == id, 'short_desc'].values[0]
        self.thumbnail = games_df.loc[games_df['id'] == id, 'thumbnail'].values[0]
        self.url = games_df.loc[games_df['id'] == id, 'url'].values[0]


def get_top_weighted(number=5):
    ## this can always be shown
    top_games = []
    for i in range(len(df_weighted)):
        if str(df_weighted["id"][i]) not in st.session_state.user.owned_games:
            top_games.append((df_weighted["title"][i], df_weighted["id"][i], 
                              df_weighted["short_desc"][i], df_weighted["price"][i],
                              df_weighted["url"][i]))
            if len(top_games) >= number:
                break
    return top_games

def recently_played_recommendations():
    if st.session_state.user.played_recommendations != "":     
        st.markdown('<h2 style="color:white;">Based on your recent activity</h2>', unsafe_allow_html=True)
        st.markdown('<span style="color:white;">Why not try these trending games...</span>', unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="color:white;">Hop back in</h2>', unsafe_allow_html=True)
        st.markdown('<span style="color:white;">Pick up where you left off...</span>', unsafe_allow_html=True)

    recent_1, recent_2, recent_3, recent_4, recent_5 = st.columns(5)
    recent_cols = [recent_1, recent_2, recent_3, recent_4, recent_5]
    if st.session_state.user.played_recommendations != "": 
        recent_recommendations = get_recent_recommendations()

        for i in range(len(recent_recommendations)):
            with recent_cols[i]:
                display_game_thumbnail(
                    game_id=recent_recommendations[i][1], 
                    game_url=recent_recommendations[i][4], 
                    game_title=recent_recommendations[i][0].title(), 
                    game_price=recent_recommendations[i][3], 
                    game_desc=recent_recommendations[i][2]
                )
    else:
        recent_recommendations = random_games_played()

        for i in range(len(recent_recommendations)):
            with recent_cols[i]:
                display_game_thumbnail(
                    game_id=recent_recommendations[i][1], 
                    game_url=recent_recommendations[i][4], 
                    game_title=recent_recommendations[i][0].title(), 
                    game_price=recent_recommendations[i][3], 
                    game_desc=recent_recommendations[i][2]
                )
            
import random

def random_games_played():
    games_played = []
    played = st.session_state.user.owned_games
    played_total = len(played)
    if played_total > 5:
        game_range = 5
    else:
        game_range = played_total
    random_games = random.sample(played, game_range)
    

    for i in random_games:
        i = int(i)
        try:
            games_played.append((games_df.loc[i]["title"], (games_df.loc[i].index), 
                            games_df.loc[i]["short_desc"], "",
                            games_df.loc[i]["url"]))

        except:
            pass
    return games_played



def get_recent_recommendations():
    recent_recommendations = []
    if st.session_state.user.played_recommendations != "":
        recent = st.session_state.user.played_recommendations
        for i in recent:
            i = int(i)
            n = 0
            i += n
            # this is quick fix to stop games that don't work
            try:
                recent_recommendations.append((games_df.loc[i]["title"], (games_df.loc[i].index), 
                                  games_df.loc[i]["short_desc"], games_df.loc[i]["price"],
                                  games_df.loc[i]["url"]))
            except:
                n += -1
    return recent_recommendations



def display_game_thumbnail(game_id, game_url, game_title, game_price, game_desc):
    st.markdown(
        f"""
        <div style="cursor:pointer;">
            <a href="/?selected_game={game_id}" target="_self">
                <img src="{game_url}" alt="Game ID: {game_id}" width="90%">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    if game_price != "":
        game_price = "€" + str(game_price)

    st.markdown(f'<span style="color:white;"><strong>{game_title}. {game_price}</strong></span>', unsafe_allow_html=True)
    if len(game_desc) < 90:
        st.markdown(f'<span style="color:white;">{game_desc}</span>', unsafe_allow_html=True)
    else:
        short_desc_string = game_desc[:90].rstrip() + "...."
        # short_desc_string = short_desc_string + "...."
        st.markdown(f'<span style="color:white;">{short_desc_string}</span>', unsafe_allow_html=True)


# def header_image(game_id):
#     url = df_weighted.loc[df_weighted['id'] == game_id, 'url'].values[0]
#     st.markdown(
#         f"""
#         <script>
#         function selectGame(gameId) {{
#             var xhttp = new XMLHttpRequest();
#             xhttp.open("GET", "/?selected_game=" + gameId, true);
#             xhttp.send();
#         }}
#         </script>
#         <div onclick="selectGame({game_id})" style="cursor:pointer;">
#             <img src="{url}" alt="Game ID: {game_id}" width="90%">
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# def select_game(game_id):
#     #st.session_state.selected_game = SelectedGame(game_id)
#     st.markdown("TEST")



def new_user():
    st.session_state.fresh = False
    st.session_state.make_new_user = True

def existing_user():
    st.session_state.fresh = False
    st.session_state.make_new_user = False
    st.session_state.existing_user = True

def username_confirmed():
    valid, username = validate_username(st.session_state.username_input)
    if valid:
        st.session_state.valid_user = True
        st.session_state.username = username
        st.session_state.username_confirmed = True
        st.session_state.incorrect_username = False
        st.session_state.existing_user = False
        st.session_state.user = User(username)
    else:
        st.session_state.valid_user = False
        st.session_state.username_confirmed = False
        st.session_state.incorrect_username = True
        st.session_state.existing_user = False

        

def app_start():
    st.session_state.page = 'home'
    st.markdown('<h1 class="custom-title">Welcome to your Steam Review</h1>', unsafe_allow_html=True)

    # set variables at start
    if 'fresh' not in st.session_state:
        st.session_state.fresh = True
        st.session_state.make_new_user = False
        st.session_state.existing_user = False
        st.session_state.username_confirmed = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    evaluate_sidebar()

app_start()








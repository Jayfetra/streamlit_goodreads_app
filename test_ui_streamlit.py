import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime, timedelta
import warnings
import pytz
import streamlit.components.v1 as components
from tzlocal import get_localzone  # pip install tzlocal
import time
import chess
import chess.pgn
import io
import pprint
import requests
warnings.filterwarnings('ignore')
import chess_com_download
from streamlit_javascript import st_javascript
from pytz import timezone

from chess_com_download import test_function_test
from chess_com_download import opening_database
from chess_com_download import download_data_chess_com
from chess_com_download import pre_analysis_chessgame
from chess_com_download import analyze_chess_games
from chess_com_download import prepare_game_data
from chess_com_download import insert_to_supabase
from supabase import create_client, Client
from datetime import datetime
import pytz


local_timezone=timezone('Asia/Jakarta')
# user_timezone = st_javascript("""await (async () => {
#             const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
#             console.log(userTimezone)
#             return userTimezone
# })().then(returnValue => returnValue)""")

df_chess_game = download_data_chess_com('jay_fh',6,7,2025)
# games_data = prepare_game_data(df_chess_game)
# total_inserted = insert_to_supabase(games_data)
# print(f"\nSuccessfully inserted {total_inserted} out of {len(df_chess_game)} games")
df = pre_analysis_chessgame(df_chess_game, 'jay_fh',local_timezone)
print (df_chess_game.head())
print (df.head())
print (df.columns)






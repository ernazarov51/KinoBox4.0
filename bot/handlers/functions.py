import asyncio
from datetime import datetime

from db.models import Models
from db.service import CRUD

# my_id=5647453083
# Johon's id=713108235
# Diyor=1739751167
genres = "Jangari,Fantastika,Komediya,Drama,Triller,Sarguzasht,Qo‘rqinchli,Tarixiy,Biografik,Oilaviy,Animatsiya,Detektiv"


async def kino_statistics():
    movies:[list['Models.Movie']]=CRUD(Models.Movie).select_all()
    movie_count=len(movies)
    caption="Bugungi Filmlar: \n"
    if movies:
        for i in movies:

            if str(i.created_at.day)==str(datetime.today().day):
                caption+=f"📌 Nomi: {i.title}\n"
                caption+=f"🕓 Vaqt: {i.created_at.strftime('%H:%M')}\n"
        caption+='\n\n'+f"Jami filmlar {movie_count}ta"
    else:
        caption+='\n'+"Bugun hech qanday film qo'shilmagan!"+f"Jami filmlar {movie_count}ta"
    return caption

async def search_users(title:str=None):
    all_users=CRUD(Models.User).select_all()
    title = title[12:]
    if title:
        results=[]
        for i in all_users:
            if str(title).lower() in str(i.first_name).lower():
                results.append(i)
        return results
    elif title=='':
        return all_users
async def search_movies(title:str=None):
    if title and title != "films" and title != "admin-kinolar":
        title=title.split()[1] if len(title.split())>1 else None
        movies=CRUD(Models.Movie).select_all()
        results=[]
        for i in movies:
            if str(title).lower() in str(i.title).lower():
                results.append(i)
        return results
    elif title == "films" or title == "admin-kinolar":
        return CRUD(Models.Movie).select_all()




async def last_added(title:str=None):
    diapason=3
    if title!='last-added':
        title=title.split()[1] if len(title.split())>1 else None
        movies=CRUD(Models.Movie).select_all()
        movies=movies[0:diapason]
        results=[]
        for i in movies:
            if str(title).lower() in str(i.title).lower():
                results.append(i)
        return results
    elif title=='last-added':
        movies=CRUD(Models.Movie).select_all()
        return movies[0:diapason]

async def return_messages():
    messages:list['Models.Review'] = CRUD(Models.Review).select_all()
    msg=''
    for i in messages:
        user:str=CRUD(Models.User).select_by_filter(user_id=i.user_id)
        username=f'{user.user_name}' if user.user_name!='None' else f'{user.first_name}|{user.user_id}'
        msg+='〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n'
        msg+=f'User: {username}'
        msg+='\n'
        msg+=f'Review: {i.review}\n'
        msg += '〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n'
    return msg

async def block_user(id:int):
    CRUD(Models.User).update(id_=id, is_blockes='true')
async def unblock_user(id:int):
    CRUD(Models.User).update(id_=id, is_blockes='false')

async def user_statistics():
    users=CRUD(Models.User).select_all()
    caption = "Bugun Qo'shilgan foydalanuvchilar: \n"
    if users:
        for i in users:
            if str(i.created_at.day)==str(datetime.today().day):
                caption += f"📌 username: {i.user_name}\n"
                caption += f"🕓 Vaqt: {i.created_at.strftime('%H:%M')}\n"
        caption += '\n\n' + f"Jami foydalanuvchilar {len(users)}ta"
    else:
        caption+='\n'+"Bugun hech qanday film qo'shilmagan!"+f"Jami filmlar {len(users)}ta"
    return caption


async def search_movie(code:str=None):
    movie=CRUD(Models.Movie).select_by_filter(film_code=code)
    if movie:
        CRUD(Models.Movie).update(movie.id,visit_count=int(movie.visit_count)+1)
    return movie if movie else None

async def search_genre(title: str = None):
    if title:
        genre_title = title.split()[0] if len(title.split()) > 1 else title.strip()
        try:
            title = title.split()[1] if len(title.split()) > 1 else None
        except:
            title = None

        movies=CRUD(Models.Movie).select_all()
        current_genre_movies = []
        for i in movies:
            if genre_title.title() in i.genre:
                current_genre_movies.append(i)



        results = []
        if title:
            for movie in current_genre_movies:
                if title.lower() in movie.title.lower():
                    results.append(movie)

        else:
            results = current_genre_movies

        return results

    return []


async def week_film():
    movie = CRUD(Models.Movie).select_with_max(Models.Movie.visit_count)
    return movie


async def get_user_data(user_id:str):
    user:['Models.User']=CRUD(Models.User).select_by_filter(user_id=user_id)
    caption=f"""Firstname | {user.first_name}
Username | {user.user_name}
UserID | {user.user_id}
Created at | {user.created_at.strftime('%Y:%D%H:%M')}
    """
    return caption


import random

def generate_unique_code():
    code = ''.join(str(random.randint(0, 9)) for _ in range(5))
    return code







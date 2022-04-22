import datetime
from typing import List
from enum import Enum


class Movie:
    def __init__(self, name, year, director, genre):
        self.genre = genre
        self.director = director
        self.year = year
        self.name = name
        self.watched = False
        self.watched_at: datetime.datetime = None

    def __str__(self) -> str:
        watched_at = ''
        watched = 'нет'
        if self.watched:
            watched = 'да'
            if self.watched_at is not None:
                watched_at = ', Дата просмотра: {}'.format(self.watched_at.strftime('%m/%d/%Y'))
        return 'Название: {}, Год {}, Жанр: {}, Режиссер: {}, Просмотренний : {}{}'.format(
            self.name,
            self.year,
            self.director,
            self.genre,
            watched,
            watched_at
        )


# class MovieType(Enum):
#     WATCHED = 1
#     NEW = 2


class Movies:
    def __init__(self, movies=None):
        if movies is None:
            movies = []
        self.movies: List[Movie] = movies

    def add_film_to_list(self):
        movie_name = input('Введи название фильма который хочешь добавить: ')
        movie_year = input('Введи год фильма который хочешь добавить: ')
        movie_director = input('Введи режисера фильма который хочешь добавить: ')
        movie_genre = input('Введи жанр фильма который хочешь добавить: ')
        self.movies.append(Movie(movie_name, movie_year, movie_director, movie_genre))

    def __str__(self) -> str:
        list = ''
        for i, film in enumerate(self.movies):
            s = '{} - {}\n'.format(i + 1, film)
            list += s
        return list

    def is_watched(self) -> bool:
        # self.movies[ask - 1] # фильм который видел пользователь
        ask = input('did you watch some of them? (y/n) -')
        if ask == 'y':
            ask_which = input('which one? - ')
            if ask_which.isdigit() and (0 <= int(ask_which) - 1 < len(self.movies)):
                self.movies[int(ask_which) - 1].watched = True
                print('Фильму присвоен статус просмотренный!')
                date = input('Просмотрен в (mm/dd/yyyy): ')
                try:
                    self.movies[int(ask_which) - 1].watched_at = datetime.datetime.strptime(date, '%m/%d/%Y')
                except ValueError:
                    print('Invalid date!')

    def filtered(self, watched: bool, created_from: datetime.datetime, created_to: datetime.datetime,
                 genres: List[str]):
        filtered_list = []
        # created_from_r = time.strptime(created_from, '%m/%d/%Y')
        # created_to_r = time.strptime(created_to, '%m/%d/%Y')
        for film in self.movies:
            found_genre = False
            if not film.watched == watched:
                continue
            if not (film.watched_at > created_from) and not (film.watched_at < created_to):
                continue
            for genre in genres:
                if film.genre == genre:
                    found_genre = True
                    break
            if not found_genre:
                continue

            filtered_list.append(film)
        return Movies(filtered_list)


from_ = datetime.datetime(2019, 1, 1)
to_ = datetime.datetime(2022, 12, 12)
Films = Movies()
Films.add_film_to_list()
Films.add_film_to_list()
Films.add_film_to_list()
print(Films)
Films.is_watched()
print(Films)
print(Films.filtered(True, from_, to_, ['horor', 'comedy']))
print(Films)

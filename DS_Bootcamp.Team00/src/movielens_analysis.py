#!/usr/bin/env python3

import os
from collections import Counter
from datetime import datetime, timezone
from collections import defaultdict

import requests
from bs4 import BeautifulSoup


class Ratings:
  """
  Analyzing data from ratings.csv
  movies_titles - dict(movieId: (title, year, genres))
                      movieId: int, title: str, year: int, genres: list(str)
  """
  def __init__(self, path_to_the_file: str, movies_titles: dict) -> None:
    """
    Put here any fields that you think you will need.
    """
    if not path_to_the_file.endswith("ratings.csv"):
      raise Exception("It's a wrong file. You have to use next file 'ratings.csv'") 
    self.path = path_to_the_file
    self.headers = []
    self.ratings = [] # list((userId: int, movie_title: str, rating: float.0, time: datetime))
    self.load_ratings(movies_titles)
    self.movies = Ratings.Movies(self.ratings)
    self.users = Ratings.Users(self.ratings)
  
  def load_ratings(self, movies_titles: dict) -> None:
    """
    Upload all retings from the file.
    """
    if not os.path.exists(self.path):
      raise OSError("Can't open file. May be such file doesn't exist. Try again.")
    movies_titles = dict(movies_titles)
    with open(self.path, 'r', encoding='utf-8') as file:
      self.headers = next(file).strip().split(',')  # читаем и разбиваем заголовки
      for line in file:
        line = line.strip()
        if not line:
          continue  # пропускаем пустые строки
        parts = line.split(',', maxsplit=3)  # разбиваем на 4 части
        userId = int(parts[0])
        movieId = int(parts[1])
        if not movieId in movies_titles:
          continue
        movie_title = movies_titles[movieId][0]
        rating = round(float(parts[2]), 1)
        time = datetime.fromtimestamp(int(parts[3]), tz = timezone.utc)
        self.ratings.append((userId, movie_title, rating, time))

  class Movies:
    """
    TO DO: rating by budget, rating by profit
    """
    def __init__(self, ratings: list) -> None:
      self.ratings = ratings # list((userId: int, movie_title: str, rating: float.0, time: datetime))
      self.ratings_by_year = dict() # dict(year: ratings_count) - year: int, ratings_count: int
      self.ratings_distribution = dict() # dict(rating: count) - rating: float.0, count: int
      self.dist_by_num_of_ratings = Counter()
      self.dist_rating = dict() # dict(movie_title: list(ratings))

    def dist_by_year(self) -> dict:
      """
      The method returns a dict where the keys are years and the values are counts of ratings. 
      Sort it by years ascendingly. You need to extract years from timestamps.
      """
      if not self.ratings_by_year:
        list_years = [item[3].year for item in self.ratings]
        self.ratings_by_year = dict(sorted(Counter(list_years).items(), key=lambda item: item[0]))
      return self.ratings_by_year
    
    def dist_by_rating(self) -> dict:
      """
      The method returns a dict where the keys are ratings and the values are counts.
      Sort it by ratings ascendingly.
      """
      if not self.ratings_distribution:
        list_ratings = [item[2] for item in self.ratings]
        self.ratings_distribution = dict(sorted(Counter(list_ratings).items(), key=lambda item: item[0]))
      return self.ratings_distribution
    
    def top_by_num_of_ratings(self, n: int, obj = "movies") -> dict:
      """
      The method returns top-n movies by the number of ratings. 
      It is a dict where the keys are movie titles and the values are numbers.
      Sort it by numbers descendingly.
      """
      if n <= 0:
        raise Exception("Wrong count - n in Ratings.top_by_num_of_ratings()! n has to be positive > 0.")
      field_index = 1
      if obj == "users":
        field_index = 0
      if not self.dist_by_num_of_ratings:
        list_dist_by_num_of_ratings = [item[field_index] for item in self.ratings]
        self.dist_by_num_of_ratings = Counter(list_dist_by_num_of_ratings)
      top_movies = dict(self.dist_by_num_of_ratings.most_common(n))
      return top_movies
    
    def top_by_ratings(self, n: int, metric = "average", obj = "movies") -> dict:
      """
      The method returns top-n movies by the average or median of the ratings.
      It is a dict where the keys are movie titles and the values are metric values.
      Sort it by metric descendingly.
      The values should be rounded to 2 decimals.
      """
      if n <= 0:
        raise Exception("Wrong count - n in Ratings.top_by_ratings()! n has to be positive > 0.")
      if metric not in ("average", "median"):
        raise Exception("Wrong parameter 'metric' in Ratings.top_by_ratings()! 'metric' has to be 'average' or 'median'.")
      
      field_index = 1
      if obj == "users":
        field_index = 0
      if not self.dist_rating:
        self.dist_rating = defaultdict(list)
        for item in self.ratings:
          self.dist_rating[item[field_index]].append(item[2]) # dict(movie_title or userIds: list(ratings))

      movies_metric_rating = dict()
      for item in self.dist_rating.items():
        movies_metric_rating[item[0]] = Statistics.average(item[1]) if metric == "average" else Statistics.median(item[1])
      top_movies = dict(Counter(movies_metric_rating).most_common(n))
      return top_movies
    
    def top_controversial(self, n: int, obj = "movies") -> dict:
      """
      The method returns top-n movies by the variance of the ratings.
      It is a dict where the keys are movie titles and the values are the variances.
      Sort it by variance descendingly.
      The values should be rounded to 2 decimals.
      """
      if n <= 0:
        raise Exception("Wrong count - n in Ratings.top_controversial()! n has to be positive > 0.")
      
      field_index = 1
      if obj == "users":
        field_index = 0
      if not self.dist_rating:
        self.dist_rating = defaultdict(list)
        for item in self.ratings:
          self.dist_rating[item[field_index]].append(item[2]) # dict(movie_title or userIds: list(ratings))

      movies_variance_rating = dict()
      for item in self.dist_rating.items():
        movies_variance_rating[item[0]] = Statistics.variance(item[1])
      top_movies = dict(Counter(movies_variance_rating).most_common(n))
      return top_movies

  class Users(Movies):
    """
    In this class, three methods should work. 
    Inherit from the class Movies. Several methods are similar to the methods from it.
    """
    def __init__(self, ratings: list) -> None:
      super().__init__(ratings)

    def top_users_by_ratings_count(self, n: int) -> dict:
      """
      The 1st returns the distribution of users by the number of ratings made by them.
      """
      return self.top_by_num_of_ratings(n, "users")
    
    def top_users_by_ratings(self, n: int, metric = "average") -> dict:
      """
      The 2nd returns the distribution of users by average or median ratings made by them.
      """
      return self.top_by_ratings(n, metric, "users")
    
    def top_users_controversial(self, n: int) -> dict:
      """
      The 3rd returns top-n users with the biggest variance of their ratings.
      """
      return self.top_controversial(n, "users")


class Tags:
  """
  Analyzing data from tags.csv
  """
  def __init__(self, path_to_the_file: str) -> None:
    if not path_to_the_file.endswith("tags.csv"):
      raise Exception("It's a wrong file. You have to use next file 'tags.csv'") 
    self.path = path_to_the_file
    self.headers = []
    self.tags = [] # list((userId: int, movieId: int, tag: str, time: datetime))
    self.only_tags = [] # list(tag: str)
    self.load_tags()
  
  def load_tags(self) -> None:
    """
    Upload all tags from the file.
    """
    if not os.path.exists(self.path):
      raise OSError("Can't open file. May be such file doesn't exist. Try again.")
    with open(self.path, 'r', encoding='utf-8') as file:
      self.headers = next(file).strip().split(',')  # читаем и разбиваем заголовки
      for line in file:
        line = line.strip()
        if not line:
          continue  # пропускаем пустые строки
        parts = line.split(',', maxsplit=3)  # разбиваем на 4 части
        userId = int(parts[0])
        movieId = int(parts[1])
        tag = parts[2].strip().lower()
        time = datetime.fromtimestamp(int(parts[3]), tz = timezone.utc)
        self.tags.append((userId, movieId, tag, time))
        self.only_tags.append(tag)
      
  def most_words(self, n: int) -> dict:
    """
    The method returns top-n tags with most words inside. It is a dict 
    where the keys are tags and the values are the number of words inside the tag.
    Drop the duplicates. Sort it by numbers descendingly.
    """
    if n <= 0:
      raise Exception("Wrong count - n in Tags.most_words()! n has to be positive > 0.")
    tags_word_count = {}
    tags = set(self.only_tags)
    for tag in tags:
      word_count = len(tag.split())
      tags_word_count[tag] = word_count
    sorted_tags = sorted(tags_word_count.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_tags[:n])

  def longest(self, n: int) -> list:
    """
    The method returns top-n longest tags in terms of the number of characters.
    It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
    """
    if n <= 0:
      raise Exception("Wrong count - n in Tags.longest()! n has to be positive > 0.")
    tags = set(self.only_tags)
    sorted_tags = sorted(tags, key=lambda item: len(item), reverse=True)
    return sorted_tags[:n]

  def most_words_and_longest(self, n: int) -> list:
    """
    The method returns the intersection between top-n tags with most words inside and 
    top-n longest tags in terms of the number of characters.
    Drop the duplicates. It is a list of the tags.
    """
    top_words = set(self.most_words(n).keys())
    top_longest = set(self.longest(n))
    intersection = list(top_words.intersection(top_longest))
    return intersection
      
  def most_popular(self, n: int) -> dict:
    """
    The method returns the most popular tags. 
    It is a dict where the keys are tags and the values are the counts.
    Drop the duplicates. Sort it by counts descendingly.
    """
    if n <= 0:
      raise Exception("Wrong count - n in Tags.most_popular()! n has to be positive > 0.")
    tags_by_count = Counter(self.only_tags)
    return dict(tags_by_count.most_common(n))
      
  def tags_with(self, word: str) -> list:
    """
    The method returns all unique tags that include the word given as the argument.
    Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
    """
    if word == "":
      raise Exception("Wrong word in Tags.tags_with()! The word has not to be empty.")
    word_lower = word.lower()
    tags = set(self.only_tags)
    filtered_tags = [tag for tag in tags if word_lower in tag.lower()]
    return sorted(filtered_tags)
  
  def most_popular_by_years(self, n_latest_years: int, n: int) -> dict:
    """
    Bonus part
    The method returns all unique tags that were most popular every year.
    It is a dict where the keys are years and the values are dicts where the keys are tags and the values are the counts.
    Drop the duplicates. Sort it by counts descendingly.
    """
    if n_latest_years <= 0 or n <= 0:
      raise Exception("Wrong count - n_latest_years or n in Tags.most_popular()! n_latest_years and n have to be positive > 0.")
    popular_tags_by_years = dict()
    for tag in self.tags: # разбираем теги в словарь по годам
      year = tag[3].year
      text = tag[2]
      if not year in popular_tags_by_years:
        popular_tags_by_years[year] = list()
      popular_tags_by_years[year].append(text)
    
    # сортировака словаря по годам по убыванию и выбор n_latest_years последних лет
    popular_tags_by_years = dict(sorted(popular_tags_by_years.items(), key=lambda item: item[0], reverse=True)[:n_latest_years])
    for year in popular_tags_by_years.keys():
      # сортировка списков тегов по каждому году по популярности по убыванию и выбор n популярных
      popular_tags_by_years[year] = dict(Counter(popular_tags_by_years[year]).most_common(n))
    return popular_tags_by_years
  
  def tags_with_by_years(self, word: str) -> dict:
    """
    Bonus part
    The method returns all unique tags that include the word given as the argument by years.
    It is a dict where the keys are years and the values are dicts where the keys are tags and the values are the counts.
    Drop the duplicates. Sort it by counts descendingly.
    """
    if word == "":
      raise Exception("Wrong word in Tags.tags_with()! The word has not to be empty.")
    word_lower = word.lower()
    tags_with_by_years = dict()
    for tag in self.tags: # разбираем теги в словарь по годам
      if not word_lower in tag[2]:
        continue
      year = tag[3].year
      text = tag[2]
      if not year in tags_with_by_years:
        tags_with_by_years[year] = list()
      tags_with_by_years[year].append(text)
    
    # сортировака словаря по годам по убыванию
    tags_with_by_years = dict(sorted(tags_with_by_years.items(), key=lambda item: item[0], reverse=True))
    for year in tags_with_by_years.keys():
      # сортировка списков тегов по каждому году по популярности по убыванию
      tags_with_by_years[year] = dict(sorted(Counter(tags_with_by_years[year]).items(), key=lambda item: item[1], reverse=True))
    return tags_with_by_years


class Movies:
  """
  Analyzing data from movies.csv
  genres = {"Action", "Adventure", "Animation", "Children's", "Comedy",
              "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir",
              "Horror", "Musical", "Mystery", "Romance", "Sci-Fi",
              "Thriller", "War", "Western", "(no genres listed)"}
  """
  def __init__(self, path_to_the_file: str) -> None:
    """
    Put here any fields that you think you will need.
    """
    if not path_to_the_file.endswith("movies.csv"):
      raise Exception("It's a wrong file. You have to use next file 'movies.csv'")
    self.path = path_to_the_file
    self.headers = list()
    self.movies = dict() # dict(movieId: (title: str, year_release: str, genres: list(str)))
    self.releases_by_years = dict() # dict(year: count) - year: str, count: int
    self.dict_by_genres = dict() # dict(genre: count) - genre: str, count: int
    self.movies_by_genres_count = list() # list((title: str, genres_count: int))
    self.load_movies()

  def load_movies(self) -> None:
    """
    Upload all movies from the file.
    """
    if not os.path.exists(self.path):
      raise OSError("Can't open file. May be such file doesn't exist. Try again.")
    with open(self.path, 'r', encoding='utf-8') as file:
      self.headers = next(file).strip().split(',')  # читаем и разбиваем заголовки
      for line in file:
        line = line.strip()
        if not line:
          continue  # пропускаем пустые строки
        parts = line.split(',', maxsplit=2)  # разбиваем на 3 части, чтобы не разбивать жанры с запятыми в названии
        if len(parts) < 3:
          continue
        movieId = int(parts[0])

        title_str = line.split(",", maxsplit=1)[1].rsplit(",", maxsplit=1)[0] 
        if len(title_str.rsplit(" (", 1)) != 2:
          continue
        title = title_str.rsplit(" (", 1)[0].replace("\"", "")
        year = title_str.rsplit(" (", 1)[1].replace(")", "").replace("\"", "")
        genres_str = line.rsplit(",", 1)[1]
        genres = genres_str.split('|')  # разбиваем жанры по '|'
        if "(no genres listed)" in genres:
          genres.remove("(no genres listed)")
        self.movies[movieId] = (title, year, genres)

  def dist_by_release(self) -> dict:
    """
    The method returns a dict or an OrderedDict where the keys are years and the values are counts. 
    You need to extract years from the titles. Sort it by counts descendingly.
    """
    if not self.releases_by_years:
      for movieId in self.movies.keys():
        year = self.movies[movieId][1]
        self.releases_by_years[year] = self.releases_by_years.get(year, 0) + 1
      self.releases_by_years = dict(sorted(self.releases_by_years.items(), key=lambda item: item[1], reverse=True))
    return self.releases_by_years
  
  def dist_by_genres(self) -> dict:
    """
    The method returns a dict where the keys are genres and the values are counts.
    Sort it by counts descendingly.
    """
    if not self.dict_by_genres:
      for movie in self.movies.values():
        for genre in movie[2]:
          self.dict_by_genres[genre] = self.dict_by_genres.get(genre, 0) + 1
      self.dict_by_genres = dict(sorted(self.dict_by_genres.items(), key=lambda item: item[1], reverse=True))
    return self.dict_by_genres
      
  def most_genres(self, n: int) -> dict:
    """
    The method returns a dict with top-n movies where the keys are movie titles and 
    the values are the number of genres of the movie. Sort it by numbers descendingly.
    """
    if n <= 0:
      raise Exception("Wrong count - n in Movies.most_genres()! n has to be positive > 0.")
    if not self.movies_by_genres_count:
      list_title_genres_count = [(item[0], len(item[2])) for item in self.movies.values()]
      self.movies_by_genres_count = sorted(list_title_genres_count, key=lambda item: item[1], reverse=True)
    return dict(self.movies_by_genres_count[:n])
      

class Links:
  """
  Analyzing data from links.csv
  """
  def __init__(self, path_to_the_file: str, list_of_movies: dict) -> None:
    if not path_to_the_file.endswith("links.csv"):
      raise Exception("It's a wrong file. You have to use next file 'links.csv'")
    self.path = path_to_the_file
    self.headers = list()

    self.links = dict() # dict(movieId: (imdbId: str, tmdbId: str))
    self.list_of_movies = list_of_movies # dict(movieId: (title: str, year: int, genres: list(str)))
    self.movies_info = dict() # dict(movieId: (Director: str, Budget: int, Gross worldwide: int, Runtime: int)) runtime - minutes
    self.directors_by_count = Counter()
    self.movies_by_budget = list() # list((title: str, budget: int))
    self.movies_by_profit = list() # list((title: str, profit: int))
    self.movies_by_runtime = list() # list((title: str, runtime: int)) runtime - minutes
    self.movies_by_cost_per_minute = list() # list((title: str, cost_per_minute: decimal.00)) cost_per_minute - budget/runtime

    self.load_links()
    list_fields = ["Director", "Budget", "Gross worldwide", "Runtime"]
    self.movies_info = self.get_imdb(self.list_of_movies)

  def load_links(self) -> None:
    if not os.path.exists(self.path):
      raise OSError("Can't open file. May be such file doesn't exist. Try again.")
    with open(self.path, 'r', encoding='utf-8') as file:
      self.headers = next(file).strip().split(',')  # читаем и разбиваем заголовки
      for line in file:
        line = line.strip()
        if not line:
          continue  # пропускаем пустые строки
        parts = line.split(',')  # разбиваем на 3 части
        movieId = int(parts[0])
        imdbId = parts[1]
        tmdbId = parts[2]
        self.links[movieId] = (imdbId, tmdbId)
  
  def get_imdb(self, list_of_movies: dict) -> dict:
    """
    The method returns a dict {movieId: (field1, field2, field3, ...)} for the list of movies given as the argument (movieId).
    For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
    The values should be parsed from the IMDB webpages of the movies.
    Sort it by movieId descendingly.
    """
    movies_info = defaultdict(list)
    for movieId in list_of_movies.keys():
      if not movieId in self.links:
        continue
      link_imdb = self.links[movieId][0]
      try:
        movies_info[movieId] = WebParseСlient.get_data(link_imdb)
      except Exception as e:
        # print(f"Ошибка при попытке распарсить данные для movieId={movieId}, imdb={link_imdb}")
        pass
    movies_info = dict(sorted(movies_info.items(), key=lambda item: item[0], reverse=True))
    return movies_info
      
  def top_directors(self, n: int) -> dict:
    """
    The method returns a dict with top-n directors where the keys are directors and 
    the values are numbers of movies created by them. Sort it by numbers descendingly.
    """
    if n <= 0:
      raise Exception("Wrong count of directors - n in Links.top_directors()! n has to be positive > 0.")
    if not self.directors_by_count:
      list_of_directors = [item[0] for item in self.movies_info.values()]
      self.directors_by_count = Counter(list_of_directors)
    return dict(self.directors_by_count.most_common(n))

  def most_expensive(self, n: int) -> dict:
    """
    The method returns a dict with top-n movies where the keys are movie titles and
    the values are their budgets. Sort it by budgets descendingly.
    """
    if n <= 0:
      raise Exception("Wrong count - n in Links.most_expensive()! n has to be positive > 0.")
    if not self.movies_by_budget:
      list_title_budgets = list()
      for movieId in self.links.keys():
        if not movieId in self.list_of_movies:
          continue
        title = self.list_of_movies[movieId][0]
        if not movieId in self.movies_info:
          continue
        budget = self.movies_info[movieId][1]
        list_title_budgets.append((title, budget))
      self.movies_by_budget = sorted(list_title_budgets, key=lambda item: item[1], reverse=True)
    return dict(self.movies_by_budget[:n])
  
  def most_profitable(self, n: int) -> dict:
    """
    The method returns a dict with top-n movies where the keys are movie titles and
    the values are the difference between cumulative worldwide gross and budget.
    Sort it by the difference descendingly.
    """
    if n <= 0:
      raise Exception("Wrong count - n in Links.most_profitable()! n has to be positive > 0.")
    if not self.movies_by_profit:
      list_title_profit = list()
      for movieId in self.links.keys():
        if not movieId in self.list_of_movies:
          continue
        title = self.list_of_movies[movieId][0]
        if not movieId in self.movies_info:
          continue
        profit = self.movies_info[movieId][2] - self.movies_info[movieId][1]
        list_title_profit.append((title, profit))
      self.movies_by_profit = sorted(list_title_profit, key=lambda item: item[1], reverse=True)
    return dict(self.movies_by_profit[:n])
   
  def longest(self, n: int) -> dict:
    """
    The method returns a dict with top-n movies where the keys are movie titles and
    the values are their runtime. If there are more than one version – choose any.
    Sort it by runtime descendingly.
    """
    if n <= 0:
      raise Exception("Wrong count - n in Links.longest()! n has to be positive > 0.")
    if not self.movies_by_runtime:
      list_title_runtime = list()
      for movieId in self.links.keys():
        if not movieId in self.list_of_movies:
          continue
        title = self.list_of_movies[movieId][0]
        if not movieId in self.movies_info:
          continue
        runtime = self.movies_info[movieId][3]
        list_title_runtime.append((title, runtime))
      self.movies_by_runtime = sorted(list_title_runtime, key=lambda item: item[1], reverse=True)
    return dict(self.movies_by_runtime[:n])
      
  def top_cost_per_minute(self, n: int) -> dict:
    """
    The method returns a dict with top-n movies where the keys are movie titles and
    the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it. 
    The values should be rounded to 2 decimals. Sort it by the division descendingly.
    """
    if n <= 0:
      raise Exception("Wrong count - n in Links.top_cost_per_minute()! n has to be positive > 0.")
    if not self.movies_by_cost_per_minute:
      list_title_cost = list()
      for movieId in self.links.keys():
        if not movieId in self.list_of_movies:
          continue
        title = self.list_of_movies[movieId][0]
        if not movieId in self.movies_info:
          continue
        budget_by_minute = round(self.movies_info[movieId][1] / self.movies_info[movieId][3], 2)
        list_title_cost.append((title, budget_by_minute))
      self.movies_by_cost_per_minute = sorted(list_title_cost, key=lambda item: item[1], reverse=True)
    return dict(self.movies_by_cost_per_minute[:n])


class Statistics:
  """
	Statistics utils extra class
  """
  @staticmethod
  def average(values: list) -> float: # возвращает среднее значение
    if len(values) == 0:
      raise ValueError("This list is empty")
    return round(sum(values) / len(values), 2)
  
  @staticmethod
  def median(values: list) -> float: # возвращает медианное значение
    if len(values) == 0:
      raise ValueError("The list is empty")
    if len(values) == 1:
      return round(float(values[0]), 2)
    values = sorted(values)
    mid = int(len(values) / 2)
    if len(values) % 2:
      return round(float(values[mid]), 2)
    return round((values[mid - 1] + values[mid]) / 2.0, 2)

  @staticmethod
  def variance(values: list) -> float:  # возвращает разброс оценок (дисперсия) Σ((avg - Ai)^2)/n
    if len(values) == 0:
      raise ValueError("The list is empty")
    if len(values) == 1:
      return round(0.0, 2)
    avg = Statistics.average(values)
    deltas = [(value - avg) ** 2 for value in values]
    return round(float(sum(deltas)) / len(values), 2)


class WebParseСlient:
  __url_imdb = "http://www.imdb.com/title/tt"
  __url_tmdb = "https://www.themoviedb.org/movie/"

  @staticmethod
  def get_data(id: str, syte = "imdb") -> tuple: # ("Director", Budget, Gross Worldwide, Runtime)
    url = (WebParseСlient.__url_imdb if syte == "imdb" else WebParseСlient.__url_tmdb) + id
    html_content = WebParseСlient.get_response(url)
    try:
      result = WebParseСlient.parse_page(html_content)
    except Exception as e:
      if str(e) == "Director is empty":
        # print(f"Ошибка при попытке распарсить данные для imdb={id}: Director is empty")
        pass
      raise e
    
    # print(f'''Фильм imdb={id}, director={result[0]}, len={len(result[0])}  budget={result[1]},
    #           gross worldwide={result[2]}, runtime={result[3]}''')
    return result

  @staticmethod
  def get_response(url: str):
    headers = {
      "Accept-Language": "en-US,en;q=0.9",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    return response.content

  @staticmethod
  def parse_page(html) -> str:
    soup = BeautifulSoup(html, "html.parser")
    director_name = ""
    director_li = soup.find('li', role='presentation',
                            class_='ipc-metadata-list__item ipc-metadata-list__item--align-end')
    if director_li:
      label = director_li.find('span', string='Director')
      if label:
        # Ищем ссылку внутри этого li
        link = director_li.find('a', class_='ipc-metadata-list-item__list-content-item--link')
        if link:
          director_name = link.get_text(strip=True)
          # print("Режиссер:", director_name)
        else:
          # print("Ссылка с именем режиссера не найдена")
          pass
      else:
        # print("Метка 'Director' не найдена")
        pass
    else:
      # print("Блок с режиссером не найден")
      pass
    if director_name is None or director_name == '':
      raise ValueError("Director is empty")
    
    def get_value_by_testid(testid):
      # Находим li с нужным data-testid
      li = soup.find('li', attrs={'data-testid': testid})
      if li:
        # Ищем внутри span с классом, который содержит сумму
        span = li.find('span', class_='ipc-metadata-list-item__list-content-item')
        if span:
          return span.get_text(strip=True)
      return None

    # Получаем Budget
    budget_str = get_value_by_testid('title-boxoffice-budget')
    if not budget_str:
      raise ValueError("Budget field not found or empty")
    budget = int(budget_str.split()[0].replace(',', '').replace('$', ''))
    # Получаем Gross Worldwide
    gross_worldwide_str = get_value_by_testid('title-boxoffice-cumulativeworldwidegross')
    if not budget_str:
      raise ValueError("Budget field not found or empty")
    gross_worldwide = int(gross_worldwide_str.replace(',', '').replace('$', ''))

    # Находим элемент с data-testid="title-techspec_runtime"
    runtime = 0
    runtime_element = soup.find('li', {'data-testid': 'title-techspec_runtime'})
    if runtime_element:
      # Ищем внутри него текст с временем, например "1h 21m" или "(81 min)"
      runtime_str = runtime_element.get_text()
      runtime = int(runtime_str.split("(")[1].split()[0])
    else:
        # print("Информация о runtime не найдена.")
        pass
    return (director_name, budget, gross_worldwide, runtime)


class Tests:
	class TestRatings:
		path = "ml-latest-small/for-tests/test_"
		movies = Movies(path + "movies.csv")
		ratings = Ratings(path + "ratings.csv", movies.movies)
		num = 5
		print("TestRatings started:")

	# 1. METHODS RETURN THE CORRECT DATA TYPES
		def test_dtype_ratings_load_ratings(self):
			print("\ntest_dtype_ratings_load_ratings - ratings : ", self.ratings.ratings)
			assert type(self.ratings) is Ratings, "error: type(ratings) is not a Ratings"
			assert len(self.ratings.ratings) == 9, "error: len(ratings.ratings) != 9"
			assert type(self.ratings.movies) is Ratings.Movies, "error: type(ratings.movies) is not a Ratings.Movies"
			assert type(self.ratings.users) is Ratings.Users, "error: type(ratings.users) is not a Ratings.Users"

		def test_dtype_ratings_movies_dist_by_year(self):
			result = Ratings.Movies.dist_by_year(self.ratings.movies)
			print("test_dtype_ratings_movies_dist_by_year - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_ratings_movies_dist_by_rating(self):
			result = Ratings.Movies.dist_by_rating(self.ratings.movies)
			print("test_dtype_ratings_movies_dist_by_rating - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_ratings_movies_top_by_num_of_ratings(self):
			result = Ratings.Movies.top_by_num_of_ratings(self.ratings.movies, self.num)
			print("test_dtype_ratings_movies_top_by_num_of_ratings - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_ratings_movies_top_by_ratings_average(self):
			result = Ratings.Movies.top_by_ratings(self.ratings.movies, self.num)
			print("test_dtype_ratings_movies_top_by_ratings_average - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_ratings_movies_top_by_ratings_median(self):
			result = Ratings.Movies.top_by_ratings(self.ratings.movies, self.num, "median")
			print("test_dtype_ratings_movies_top_by_ratings_average - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_ratings_movies_top_controversial(self):
			result = Ratings.Movies.top_controversial(self.ratings.movies, self.num)
			print("test_dtype_ratings_movies_top_controversial - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_ratings_users_top_users_by_ratings_count(self):
			result = Ratings.Users.top_users_by_ratings_count(self.ratings.users, self.num)
			print("test_dtype_ratings_users_top_users_by_ratings_count - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_ratings_users_top_users_by_ratings_average(self):
			result = Ratings.Users.top_users_by_ratings(self.ratings.users, self.num)
			print("test_dtype_ratings_users_top_users_by_ratings_average - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_ratings_users_top_users_by_ratings_median(self):
			result = Ratings.Users.top_users_by_ratings(self.ratings.users, self.num, "median")
			print("test_dtype_ratings_users_top_users_by_ratings_median - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_ratings_users_top_users_controversial(self):
			result = Ratings.Users.top_users_controversial(self.ratings.users, self.num)
			print("test_dtype_ratings_users_top_users_controversial - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

	# 2. LIST ELEMENTS HAVE THE CORRECT DATA TYPES
		def test_eltype_ratings_load_ratings(self):
			assert type(self.ratings.ratings[0][0]) is int, "error: type(userId) is not an int"
			assert type(self.ratings.ratings[0][1]) is str, "error: type(movie_title) is not a str"
			assert type(self.ratings.ratings[0][2]) is float, "error: type(rating) is not a float"
			assert type(self.ratings.ratings[0][3]) is datetime, "error: type(time) is not a datetime"

		def test_eltype_ratings_movies_dist_by_year(self):
			result = Ratings.Movies.dist_by_year(self.ratings.movies)
			assert (set(map(type, result.keys())) == {int}), "error: type('years') are not ints"
			assert (set(map(type, result.values())) == {int}), "error: type('counts') are not ints"
			
		def test_eltype_ratings_movies_dist_by_rating(self):
			result = Ratings.Movies.dist_by_rating(self.ratings.movies)
			assert (set(map(type, result.keys())) == {float}), "error: type('ratings') are not floats"
			assert (set(map(type, result.values())) == {int}), "error: type('counts') are not ints"

		def test_eltype_ratings_movies_top_by_num_of_ratings(self):
			result = Ratings.Movies.top_by_num_of_ratings(self.ratings.movies, self.num)
			assert (set(map(type, result.keys())) == {str}), "error: type('titles') are not strs"
			assert (set(map(type, result.values())) == {int}), "error: type('numbers_of_ratings') are not ints"

		def test_eltype_ratings_movies_top_by_ratings_average(self):
			result = Ratings.Movies.top_by_ratings(self.ratings.movies, self.num)
			assert (set(map(type, result.keys())) == {str}), "error: type('titles') are not strs"
			assert (set(map(type, result.values())) == {float}), "error: type('avg_ratings') are not floats"

		def test_eltype_ratings_movies_top_by_ratings_median(self):
			result = Ratings.Movies.top_by_ratings(self.ratings.movies, self.num, "median")
			assert (set(map(type, result.keys())) == {str}), "error: type('titles') are not strs"
			assert (set(map(type, result.values())) == {float}), "error: type('avg_ratings') are not floats"

		def test_eltype_ratings_movies_top_controversial(self):
			result = Ratings.Movies.top_controversial(self.ratings.movies, self.num)
			assert (set(map(type, result.keys())) == {str}), "error: type('titles') are not strs"
			assert (set(map(type, result.values())) == {float}), "error: type('variances') are not floats"

		def test_eltype_ratings_users_top_users_by_ratings_count(self):
			result = Ratings.Users.top_users_by_ratings_count(self.ratings.users, self.num)
			assert (set(map(type, result.keys())) == {int}), "error: type('userIds') are not ints"
			assert (set(map(type, result.values())) == {int}), "error: type('numbers_of_ratings') are not ints"

		def test_eltype_ratings_users_top_users_by_ratings_average(self):
			result = Ratings.Users.top_users_by_ratings(self.ratings.users, self.num)
			assert (set(map(type, result.keys())) == {int}), "error: type('userIds') are not ints"
			assert (set(map(type, result.values())) == {float}), "error: type('avg_ratings') are not floats"

		def test_eltype_ratings_users_top_users_by_ratings_median(self):
			result = Ratings.Users.top_users_by_ratings(self.ratings.users, self.num, "median")
			assert (set(map(type, result.keys())) == {int}), "error: type('userIds') are not ints"
			assert (set(map(type, result.values())) == {float}), "error: type('avg_ratings') are not floats"

		def test_eltype_ratings_users_top_users_controversial(self):
			result = Ratings.Users.top_users_controversial(self.ratings.users, self.num)
			assert (set(map(type, result.keys())) == {int}), "error: type('userIds') are not ints"
			assert (set(map(type, result.values())) == {float}), "error: type('variances') are not floats"

	# 3. RETURNED DATA IS SORTED CORRECTLY
		def test_sorted_ratings_movies_dist_by_year(self):
			result = Ratings.Movies.dist_by_year(self.ratings.movies)
			flag_sorted_correctly = True
			years = list(result.keys())
			for i in range(1, len(years)):
				if years[i - 1] > years[i]: # sorted dictionary ascending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_ratings_movies_dist_by_rating(self):
			result = Ratings.Movies.dist_by_rating(self.ratings.movies)
			flag_sorted_correctly = True
			ratings_keys = list(result.keys())
			for i in range(1, len(ratings_keys)):
				if ratings_keys[i - 1] > ratings_keys[i]: # sorted dictionary ascending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_ratings_movies_top_by_num_of_ratings(self):
			result = Ratings.Movies.top_by_num_of_ratings(self.ratings.movies, self.num)
			flag_sorted_correctly = True
			counts = list(result.values())
			for i in range(1, len(counts)):
				if counts[i - 1] < counts[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_ratings_movies_top_by_ratings_average(self):
			result = Ratings.Movies.top_by_ratings(self.ratings.movies, self.num)
			flag_sorted_correctly = True
			avg_ratings = list(result.values())
			for i in range(1, len(avg_ratings)):
				if avg_ratings[i - 1] < avg_ratings[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_ratings_movies_top_by_ratings_median(self):
			result = Ratings.Movies.top_by_ratings(self.ratings.movies, self.num, "median")
			flag_sorted_correctly = True
			median_ratings = list(result.values())
			for i in range(1, len(median_ratings)):
				if median_ratings[i - 1] < median_ratings[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_ratings_movies_top_controversial(self):
			result = Ratings.Movies.top_controversial(self.ratings.movies, self.num)
			flag_sorted_correctly = True
			variances = list(result.values())
			for i in range(1, len(variances)):
				if variances[i - 1] < variances[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_ratings_users_top_users_by_ratings_count(self):
			result = Ratings.Users.top_users_by_ratings_count(self.ratings.users, self.num)
			flag_sorted_correctly = True
			counts = list(result.values())
			for i in range(1, len(counts)):
				if counts[i - 1] < counts[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_ratings_users_top_users_by_ratings_average(self):
			result = Ratings.Users.top_users_by_ratings(self.ratings.users, self.num)
			flag_sorted_correctly = True
			avg_ratings = list(result.values())
			for i in range(1, len(avg_ratings)):
				if avg_ratings[i - 1] < avg_ratings[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_ratings_users_top_users_by_ratings_median(self):
			result = Ratings.Users.top_users_by_ratings(self.ratings.users, self.num, "median")
			flag_sorted_correctly = True
			median_ratings = list(result.values())
			for i in range(1, len(median_ratings)):
				if median_ratings[i - 1] < median_ratings[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_ratings_users_top_users_controversial(self):
			result = Ratings.Users.top_users_controversial(self.ratings.users, self.num)
			flag_sorted_correctly = True
			variances = list(result.values())
			for i in range(1, len(variances)):
				if variances[i - 1] < variances[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

	class TestTags:
		path = "ml-latest-small/for-tests/test_"
		tags = Tags(path + "tags.csv")
		num = 5
		print("TestTags started:")

	# 1. METHODS RETURN THE CORRECT DATA TYPES
		def test_dtype_tags_load_tags(self):
			print("\ntest_dtype_tags_load_tags - tags : ", self.tags.only_tags)
			assert type(self.tags) is Tags, "error: type(tags) is not a Tags"
			assert len(self.tags.tags) == 10, "error: len(tags.tags) != 10"

		def test_dtype_tags_most_words(self):
			result = Tags.most_words(self.tags, self.num)
			print("test_dtype_tags_most_words - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_tags_longest(self):
			result = Tags.longest(self.tags, self.num)
			print("test_dtype_tags_longest - result : ", result)
			assert type(result) is list, "error: type(result) is not a list"

		def test_dtype_tags_most_words_and_longest(self):
			result = Tags.most_words_and_longest(self.tags, self.num)
			print("test_dtype_tags_most_words_and_longest - result : ", result)
			assert type(result) is list, "error: type(result) is not a list"

		def test_dtype_tags_most_popular(self):
			result = Tags.most_popular(self.tags, self.num)
			print("test_dtype_tags_most_popular - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"
			
		def test_dtype_tags_tags_with(self):
			result = Tags.tags_with(self.tags, "mafi")
			print("test_dtype_tags_tags_with - result : ", result)
			assert type(result) is list, "error: type(result) is not a list"

		def test_dtype_tags_most_popular_by_years(self):
			result = Tags.most_popular_by_years(self.tags, self.num, self.num)
			print("test_dtype_tags_most_popular_by_years - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"
			
		def test_dtype_tags_tags_with_by_years(self):
			result = Tags.tags_with_by_years(self.tags, "mafi")
			print("test_dtype_tags_tags_with_by_years - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

	# 2. LIST ELEMENTS HAVE THE CORRECT DATA TYPES
		def test_eltype_tags_load_tags(self):
			assert type(self.tags.only_tags[0]) is str, "error: type(only_tags[0]) is not a str"
			assert type(self.tags.tags[0]) is tuple, "error: type(tags[0]) is not a tuple"

		def test_eltype_tags_most_words(self):
			result = Tags.most_words(self.tags, self.num)
			assert type(list(result.items())[0][0]) is str, "error: type('tag') is not a str"
			assert type(list(result.items())[0][1]) is int, "error: type('count') is not an int"
			
		def test_eltype_tags_longest(self):
			result = Tags.longest(self.tags, self.num)
			assert (set(map(type, result)) == {str}), "error: type('tag') is not a str"

		def test_eltype_tags_most_words_and_longest(self):
			result = Tags.most_words_and_longest(self.tags, self.num)
			assert (set(map(type, result)) == {str}), "error: type('tag') is not a str"
			
		def test_eltype_tags_most_popular(self):
			result = Tags.most_popular(self.tags, self.num)
			assert type(list(result.items())[0][0]) is str, "error: type('tag') is not a str"
			assert type(list(result.items())[0][1]) is int, "error: type('count') is not an int"

		def test_eltype_tags_tags_with(self):
			result = Tags.tags_with(self.tags, "mafi")
			assert (set(map(type, result)) == {str})

		def test_eltype_tags_most_popular_by_years(self):
			result = Tags.most_popular_by_years(self.tags, self.num, self.num)
			assert type(list(result.items())[0][0]) is int, "error: type('year') is not an int"
			assert type(list(result.items())[0][1]) is dict, "error: type('tag_by_count') is not a dict"

		def test_eltype_tags_tags_withy_by_years(self):
			result = Tags.tags_with_by_years(self.tags, "mafi")
			assert type(list(result.items())[0][0]) is int, "error: type('year') is not an int"
			assert type(list(result.items())[0][1]) is dict, "error: type('tag_by_count') is not a dict"

	# 3. RETURNED DATA IS SORTED CORRECTLY
		def test_sorted_tags_most_words(self):
			result = Tags.most_words(self.tags, self.num)
			flag_sorted_correctly = True
			words_count = list(result.values())
			for i in range(1, len(words_count)):
				if words_count[i - 1] < words_count[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_tags_longest(self):
			result = Tags.longest(self.tags, self.num)
			flag_sorted_correctly = True
			for i in range(1, len(result)):
				if len(result[i - 1]) < len(result[i]): # sorted list descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_tags_most_popular(self):
			result = Tags.most_popular(self.tags, self.num)
			flag_sorted_correctly = True
			tag_counts = list(result.values())
			for i in range(1, len(tag_counts)):
				if tag_counts[i - 1] < tag_counts[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_tags_tags_with(self):
			result = Tags.tags_with(self.tags, 'mafi')
			flag_sorted_correctly = True
			for i in range(1, len(result)):
				if result[i - 1] < result[i]: # sorted list descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_tags_most_popular_by_years(self):
			result = Tags.most_popular_by_years(self.tags, self.num, self.num)
			flag_sorted_correctly = True
			years = list(result.keys())
			for i in range(1, len(years)):
				if years[i - 1] < years[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_tags_tags_with_by_years(self):
			result = Tags.tags_with_by_years(self.tags, 'mafi')
			flag_sorted_correctly = True
			years = list(result.keys())
			for i in range(1, len(years)):
				if years[i - 1] < years[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly
	
	class TestMovies:
		path = "ml-latest-small/for-tests/test_"
		movies = Movies(path + "movies.csv")
		# (Director, Budget, Gross worldwide, Runtime)
		movies_info = {1: ("John Lasseter", 30_000_000, 394_436_586, 81),
						2: ("Joe Johnston", 65_000_000, 262_821_940, 104),
						3: ("Howard Deutch", 25_000_000, 71_518_503, 101),
						4: ("Forest Whitaker", 16_000_000, 81_452_156, 124),
						5: ("Charles Shyer", 30_000_000, 76_594_107, 106)}
		num = 3
		print("TestMovies started:")

	# 1. METHODS RETURN THE CORRECT DATA TYPES
		def test_dtype_movies_load_movies(self):
			print("\ntest_dtype_movies_load_movies - movies : ", self.movies.movies)
			assert type(self.movies) is Movies, "error: type(movies) is not a Movies"
			assert len(self.movies.movies) == 6, "error: len(movies.movies) != 6"

		def test_dtype_movies_dist_by_release(self):
			result = Movies.dist_by_release(self.movies)
			print("test_dtype_movies_dist_by_release - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_movies_dist_by_genres(self):
			result = Movies.dist_by_genres(self.movies)
			print("test_dtype_movies_dist_by_genres - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_movies_most_genres(self):
			result = Movies.most_genres(self.movies, self.num)
			print("test_dtype_movies_most_genres - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

	# 2. LIST ELEMENTS HAVE THE CORRECT DATA TYPES
		def test_eltype_movies_load_movies(self):
			assert type(self.movies.movies[1]) is tuple, "error: type(movies[1]) is not a tuple"
			assert type(self.movies.movies[1][0]) is str, "error: type(movies[1][0]) is not a str"

		def test_eltype_movies_dist_by_release(self):
			result = Movies.dist_by_release(self.movies)
			assert (set(map(type, result.keys())) == {str}), "error: type('years') are not strs"
			assert (set(map(type, result.values())) == {int}), "error: type('counts') are not ints"
			
		def test_eltype_movies_dist_by_genres(self):
			result = Movies.dist_by_genres(self.movies)
			assert (set(map(type, result.keys())) == {str}), "error: type('genres') are not strs"
			assert (set(map(type, result.values())) == {int}), "error: type('counts') are not ints"

		def test_eltype_movies_most_genres(self):
			result = Movies.most_genres(self.movies, self.num)
			assert (set(map(type, result.keys())) == {str}), "error: type('titles') are not strs"
			assert (set(map(type, result.values())) == {int}), "error: type('numbers_of_genres') are not ints"

	# 3. RETURNED DATA IS SORTED CORRECTLY
		def test_sorted_movies_dist_by_release(self):
			result = Movies.dist_by_release(self.movies)
			flag_sorted_correctly = True
			counts = list(result.values())
			for i in range(1, len(counts)):
				if counts[i - 1] < counts[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_movies_dist_by_genres(self):
			result = Movies.dist_by_genres(self.movies)
			flag_sorted_correctly = True
			counts = list(result.values())
			for i in range(1, len(counts)):
				if counts[i - 1] < counts[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_movies_most_genres(self):
			result = Movies.most_genres(self.movies, self.num)
			flag_sorted_correctly = True
			counts = list(result.values())
			for i in range(1, len(counts)):
				if counts[i - 1] < counts[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

	class TestLinks:
		path = "ml-latest-small/for-tests/test_"
		movies = Movies(path + "movies.csv")
		links = Links(path + "links.csv", movies.movies)
		# (Director, Budget, Gross worldwide, Runtime)
		movies_info = {1: ("John Lasseter", 30_000_000, 394_436_586, 81),
						2: ("Joe Johnston", 65_000_000, 262_821_940, 104),
						3: ("Howard Deutch", 25_000_000, 71_518_503, 101),
						4: ("Forest Whitaker", 16_000_000, 81_452_156, 124),
						5: ("Charles Shyer", 30_000_000, 76_594_107, 106)}
		links.movies_info = movies_info
		num = 3
		print("TestLinks started:")
		print("movies : ", movies.movies)

	# 1. METHODS RETURN THE CORRECT DATA TYPES
		def test_dtype_links_load_links(self):
			print("\ntest_dtype_links_load_links - links : ", self.links.links)
			assert type(self.links) is Links, "error: type(links) is not a Links"
			assert len(self.links.links) == 5, "error: len(links.links) != 5"

		def test_dtype_links_top_directors(self):
			result = Links.top_directors(self.links, self.num)
			print("test_dtype_links_top_directors - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_links_most_expensive(self):
			result = Links.most_expensive(self.links, self.num)
			print("test_dtype_links_most_expensive - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_links_most_profitable(self):
			result = Links.most_profitable(self.links, self.num)
			print("test_dtype_links_most_profitable - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_links_longest(self):
			result = Links.longest(self.links, self.num)
			print("test_dtype_links_longest - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

		def test_dtype_links_top_cost_per_minute(self):
			result = Links.top_cost_per_minute(self.links, self.num)
			print("test_dtype_links_top_cost_per_minute - result : ", result)
			assert type(result) is dict, "error: type(result) is not a dict"

	# 2. LIST ELEMENTS HAVE THE CORRECT DATA TYPES
		def test_eltype_links_load_links(self):
			assert type(self.links.links[1]) is tuple, "error: type(links[1]) is not a tuple"
			assert type(self.links.links[1][0]) is str, "error: type(links[1][0]) is not a str"
			assert type(self.links.links[1][1]) is str, "error: type(links[1][1]) is not a str"

		def test_eltype_links_top_directors(self):
			result = Links.top_directors(self.links, self.num)
			assert (set(map(type, result.keys())) == {str}), "error: type('directors') are not strs"
			assert (set(map(type, result.values())) == {int}), "error: type('counts') are not ints"
			
		def test_eltype_links_most_expensive(self):
			result = Links.most_expensive(self.links, self.num)
			assert (set(map(type, result.keys())) == {str}), "error: type('movie_title') are not strs"
			assert (set(map(type, result.values())) == {int}), "error: type('budget') are not ints"

		def test_eltype_links_most_profitable(self):
			result = Links.most_profitable(self.links, self.num)
			assert (set(map(type, result.keys())) == {str}), "error: type('movie_title') are not strs"
			assert (set(map(type, result.values())) == {int}), "error: type('profit') are not ints"

		def test_eltype_links_longest(self):
			result = Links.longest(self.links, self.num)
			assert (set(map(type, result.keys())) == {str}), "error: type('movie_title') are not strs"
			assert (set(map(type, result.values())) == {int}), "error: type('runtime') are not ints"

		def test_eltype_links_top_cost_per_minute(self):
			result = Links.top_cost_per_minute(self.links, self.num)
			assert (set(map(type, result.keys())) == {str}), "error: type('movie_title') are not strs"
			assert (set(map(type, result.values())) == {float}), "error: type('cost_per_minute') are not floats"

	# 3. RETURNED DATA IS SORTED CORRECTLY
		def test_sorted_links_top_directors(self):
			result = Links.top_directors(self.links, self.num)
			flag_sorted_correctly = True
			counts = list(result.values())
			for i in range(1, len(counts)):
				if counts[i - 1] < counts[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_links_most_expensive(self):
			result = Links.most_expensive(self.links, self.num)
			flag_sorted_correctly = True
			budgets = list(result.values())
			for i in range(1, len(budgets)):
				if budgets[i - 1] < budgets[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_links_most_profitable(self):
			result = Links.most_profitable(self.links, self.num)
			flag_sorted_correctly = True
			profits = list(result.values())
			for i in range(1, len(profits)):
				if profits[i - 1] < profits[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_links_longest(self):
			result = Links.longest(self.links, self.num)
			flag_sorted_correctly = True
			runtimes = list(result.values())
			for i in range(1, len(runtimes)):
				if runtimes[i - 1] < runtimes[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly

		def test_sorted_links_top_cost_per_minute(self):
			result = Links.top_cost_per_minute(self.links, self.num)
			flag_sorted_correctly = True
			costs = list(result.values())
			for i in range(1, len(costs)):
				if costs[i - 1] < costs[i]: # sorted dictionary descending
					flag_sorted_correctly = False
					break
			assert flag_sorted_correctly
	
	class TestWebParseClient:
		def test_print_three_movies(self):
			list_three_movies = {1: ("Toy Story", 1995, ["Adventure", "Animation", "Children", "Comedy", "Fantasy"]),
								2: ("Jumanji", 1995, ["Adventure", "Children", "Fantasy"]),
								3: ("Grumpier Old Men", 1995, ["Comedy", "Romance"])}
			links = Links("ml-latest-small/links.csv", list_three_movies)
			three_movies_info = links.get_imdb(list_three_movies)
			print("\n", three_movies_info)
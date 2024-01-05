class EmptyValueError(ValueError):
    pass

class NonPositiveIntValueError(ValueError):
    pass

class EmptyStringError(EmptyValueError):
    pass

class Film:
    """
    Class Film. Contains attributes:

    :param id: film's id
    :type id: int

    :param title: film's title
    :type title: str

    :param year: release year
    :type year: int

    :param genre: film's genres
    :type genre: list

    :param director: film's director
    :type director: str

    :param actors: top actors
    :type actors: list

    :param description: film's short description
    :type id: str

    :param user_rating: film's rating
    :type user_rating: float

    :param rating_sum: sum of all of ratings of the film
    :type rating_sum: int

    :param number_of_ratings: number of ratings
    :type number_of_ratings: int
    """
    def __init__(self, id, title, year, genre, director, actors, description='', rating_sum = 0, number_of_ratings = 0):
        if id < 0 or type(id) != int:
            raise NonPositiveIntValueError()
        if title == '':
            raise EmptyStringError()
        if year < 0 or type(year) != int:
            raise NonPositiveIntValueError()
        if not genre:
            raise EmptyValueError()
        if director == '':
            raise EmptyStringError()
        if not actors:
            raise EmptyValueError()
        
        self._id = id
        self._title = title
        self._year = year
        self._genre = genre
        self._director = director
        self._actors = actors
        self._description = description
        self._rating_sum = rating_sum
        self._number_of_ratings = number_of_ratings
        if self._rating_sum != 0 and self._number_of_ratings != 0:
            self._user_rating = self._rating_sum / self._number_of_ratings
        else:
            self._user_rating = 0

    def id(self):
        return self._id
    def title(self):
        return self._title
    def year(self):
        return self._year
    def genre(self):
        return self._genre
    def director(self):
        return self._director
    def actors(self):
        return self._actors
    def description(self):
        return self._description
    def rating_sum(self):
        return self._rating_sum
    def number_of_ratings(self):
        return self._number_of_ratings
    def user_rating(self):
        return self._user_rating
    
    def update_rating(self, new_rating, old_rating):
        """
        Takes 3 parameters. Self, int(updated rating), int(old rating, if the film was not rated previously,
        method is called with old_rating = 0).
        Updates rating sum and number of ratings. Based on that recalculates and updates overall rating.
        """
        difference = new_rating - old_rating
        self._rating_sum += difference
        if difference == new_rating:
            self._number_of_ratings += 1
        self._user_rating = self._rating_sum / self._number_of_ratings

    def __str__(self):
        """
        Takes 1 parameter. Self.
        Returns a string with all information about the film.
        """
        title = f'Title: {self._title}\n'
        year = f'Release date: {self._year}\n'
        genre = f'Genres:'
        for g in self._genre:
            genre += f' {g}'
            if g  != self._genre[-1]:
                genre += f','
        director = f'\nDirector: {self._director}\n'
        actors = f'Actors:'
        for a in self._actors:
            actors += f' {a}'
            if a != self._actors[-1]:
                actors += f','
        description = f'\nDesccription: {self._description}\n'
        rating = f'Rating: {self._user_rating}'
        return title+year+genre+director+actors+description+rating

    

class User:
    """
    Class User. Contains Attributes:

    :param username: username
    :type username: str

    :param password: password
    :type password: str

    :param my_ratings: user's ratings, defaults to None
    :type my_ratings: dict, key - title of the film, value - int rating
    """
    def __init__(self, id, username, password, my_ratings=None):
        if id < 0 or type(id) != int:
            raise NonPositiveIntValueError()
        if username == '':
            raise EmptyStringError()
        if password == '':
            raise EmptyStringError()
        self._username = username
        self._password = password
        self._id = id
        if my_ratings:
            self._my_ratings = my_ratings
        else:
            self._my_ratings = {}

    def id(self):
        return self._id
    def username(self):
        return self._username
    def password(self):
        return self._password
    def my_ratings(self):
        return self._my_ratings
    
    def add_rating(self, film, rating):
        """
        Takes 3 parameters. Self, string(title of the film to be rated), int(rating of the film).
        Checks if this film was already rated. Updates user's ratings. Calls a method for updating a film's rating.
        """
        old_rating = 0
        if film.title() in self._my_ratings:
            old_rating = self._my_ratings[film.title()]
        self._my_ratings[film.title()] = rating
        film.update_rating(rating, old_rating)
        
    
class Portal():
    """
    Class Portal. Contains attributes:

    :param films: films
    :type films: list

    :param users: users
    :type users: list
    """
    def __init__(self,current_user, films, users):
        if not current_user:
            raise EmptyValueError()
        if not films:
            raise EmptyValueError()
        if not users:
            raise EmptyValueError()
        self._current_user = current_user
        self._films = films
        self._users = users

    def current_user(self):
        return self._current_user
    def films(self):
        return self._films
    def users(self):
        return self._users
    
    def get_film_by_title(self, title):
        """
        Takes 2 parameters. Self, string(title of the film).
        returns list of objects Film with matching titles.
        """
        films = self.films()
        output = []
        for film in films:
            current_title = film.title()
            if title.lower() in current_title.lower():
                output.append(film)
        if output:
            return output
        return None
    
    
    def get_film_info(self, title):
        """
        Takes 2 parameters. Self, string(title of the film).
        If there is no such film in the database the method returns a message communicating that.
        Else method str is called on object Film with that title.
        """
        films = self.get_film_by_title(title)
        if not films:
            return 'There is no film with this title in the database.'
        output = []
        for film in films:
            output.append(film.__str__())
        return output
    
        
    def get_user_ratings(self, username):
        """
        Takes 2 parameters. Self, string (username).
        Method searches for a user with this username, in case of unsuccessfull search the method returns a message
        saying that such user does not exist.
        In case of fiding the user the method then creates a list of strings of ratings.
        If the user does not have any ratings the method returns a message communicating that.
        If the user has ratings the method returns a list of strings.
        """
        output = []
        wanted_user = None
        for user in self._users:
            if username == user.username():
                wanted_user = user
                keys = list(user.my_ratings().keys())
                values = list(user.my_ratings().values())
                for i in range(0, len(keys)):
                    output.append(f'{keys[i]}: {values[i]}')
        if not wanted_user:
            return('The user with this username does not exist.')
        elif not output:
            return('This user did not rate any films.')
        else:
            return output
        
        
    def rate(self, title, rating):
        """
        Takes 3 parameters. Self, string (title of the film to be rated), rating of the film.
        In case of non numeric or out of range rating the method returns a message saying that the rating is invalid.
        If the given title does not match a title in the film database the method returns a message saying
        that there is no such film in the database.
        If everything is valid the method calls a method for user and returns a message saying that the film was rated.
        """
        if not rating.isnumeric():
            return "Invalid rating."
        rating = int(rating)
        if rating > 10 or rating < 1:
            return "Invalid rating."
        matching_films = self.get_film_by_title(title)
        if not matching_films:
            return"There is no film with this title in the database."
        if len(matching_films) == 1:
            self._current_user.add_rating(matching_films[0], rating)
            return"Film rated succesfully."
        else:
            return"There is more than 1 film that matches the given title. Please try again with a more precise title. "
    
    
    def is_genres(self, film, rec_genres):
        """
        Takes 3 parameters. Self, object of type Film, list of strings.
        This method checks whether or not genres of a film is in a list of genres given as a seccond parameter.
        If one of the genres is in the list the method returns True.
        If none of the genres are in the list the method returns False.
        """
        return any(genre in rec_genres for genre in film.genre())
    
    def rec(self):
        """
        Takes 1 parameter. Self.
        The method recommends 5 (if not possible - less) films to the user
        based on genres of films the user rated
        """
        MAX_RECOMMENDATIONS = 5
        output = []
        used_films = []
        films = sorted(self.films(), key=lambda film: film.user_rating(), reverse = True)  
        len_films = len(films)
        my_range = min(len_films, MAX_RECOMMENDATIONS) 

        """
        In case of absense of ratings method recommends top 5 films
        based on other users' ratings
        """
        if self.current_user().my_ratings() == {}:
            for i in range(0, my_range):
                output.append(films[i].title())
            return output
        
        ratings = list(self.current_user().my_ratings().items())
        ratings = sorted(ratings,key =lambda rating: rating[1], reverse = True)

        """
        If the film was rated 7 or higher the method will recommend films with this genre.
        If the film was rated 3 or lower the method will not recommend films with this genre.
        """
        BAD_RATING_BOUND = 3
        GOOD_RATING_BOUND = 7
        genres_to_rec = []
        genres_not_to_rec =[]
        for rating in ratings:
            current_film = self.get_film_by_title(rating[0])[0]
            used_films.append(current_film)
            if rating[1] >= GOOD_RATING_BOUND:
                for genre in current_film.genre():
                    genres_to_rec.append(genre)
            elif rating[1] <= BAD_RATING_BOUND:
                for genre in current_film.genre():
                    genres_not_to_rec.append(genre)

        """
        To check whether or not to recommend the film or not the method checks 2 conditions:
        1). the genre is in list of genres for recommendation
        2). the genre is not in the list of genres not for recommendation
        if the genre is in both films the film will not be recommended.
        First the method recommends films that satisfy both conditions, if there are not enough films, then
        films that satisfy only the second condition.
        """
        to_rec = []
        possible_rec = []
        for film in films:
            if film not in used_films and not self.is_genres(film, genres_not_to_rec):
                if self.is_genres(film, genres_to_rec):
                    to_rec.append(film)
                else:
                    possible_rec.append(film)
                used_films.append(film)

        to_rec = sorted(to_rec, key=lambda film: film.user_rating())
        possible_rec = sorted(to_rec, key=lambda film: film.user_rating())

        to_rec += possible_rec
        num = min(5, len(to_rec))
        output = to_rec[0:num]

        return output
        

        




    


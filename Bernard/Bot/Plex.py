from plexapi.myplex import MyPlexAccount


def readAccountInformation():
    with open('PlexKey', 'r')as fd:
        return fd.read().split()


def write(list, file):
    with open(file, 'w') as fd:
        fd.write('\n'.join(list))


def read(file):
    with open(file, 'r') as fd:
        return fd.read()


class mPlex:
    def __init__(self):
        user, passw = readAccountInformation()
        self.account = MyPlexAccount(user, passw)
        self.plex = self.account.resource('Bernard').connect()
        self.writeListMoviesTitle()

    def update(self):
        self.plex.library.update()
        self.writeListMoviesTitle()

    def listMoviesTitle(self):
        movies = self.plex.library.section('Movies')
        titles = []
        for movie in movies.search():
            titles.append(movie.title)
        return titles

    def writeListMoviesTitle(self):
        titles = self.listMoviesTitle()
        write(titles, 'Movies.txt')

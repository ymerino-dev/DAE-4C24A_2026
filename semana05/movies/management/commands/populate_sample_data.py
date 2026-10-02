from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from movies.models import Genre, Movie, Person, Rating


class Command(BaseCommand):
    """Populate database with sample data for visualization."""

    help = 'Create sample movies, genres, people, and ratings'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create genres
        genres_data = [
            'Acción', 'Drama', 'Comedia', 'Ciencia Ficción',
            'Terror', 'Romance', 'Thriller', 'Animación',
            'Documental', 'Fantasía', 'Crimen', 'Aventura',
            'Misterio', 'Música', 'Deportes'
        ]
        genres = {}
        for name in genres_data:
            genre, _ = Genre.objects.get_or_create(name=name)
            genres[name] = genre

        # Create people (actors/directors)
        people_data = [
            ('Christopher Nolan', 'DIRECTOR'),
            ('Leonardo DiCaprio', 'ACTOR'),
            ('Christian Bale', 'ACTOR'),
            ('Heath Ledger', 'ACTOR'),
            ('Tom Hardy', 'ACTOR'),
            ('Denis Villeneuve', 'DIRECTOR'),
            ('Timothée Chalamet', 'ACTOR'),
            ('Zendaya', 'ACTOR'),
            ('Greta Gerwig', 'DIRECTOR'),
            ('Margot Robbie', 'ACTOR'),
            ('Ryan Gosling', 'ACTOR'),
            ('Bong Joon-ho', 'DIRECTOR'),
            ('Song Kang-ho', 'ACTOR'),
            ('Jordan Peele', 'DIRECTOR'),
            ('Daniel Kaluuya', 'ACTOR'),
            ('Guillermo del Toro', 'DIRECTOR'),
            ('Sally Hawkins', 'ACTOR'),
            ('Doug Jones', 'ACTOR'),
            ('Hayao Miyazaki', 'DIRECTOR'),
            ('Rinko Kikuchi', 'ACTOR'),
            ('Matthew McConaughey', 'ACTOR'),
            ('Anne Hathaway', 'ACTOR'),
            ('Damien Chazelle', 'DIRECTOR'),
            ('Miles Teller', 'ACTOR'),
            ('J.K. Simmons', 'ACTOR'),
            ('Stanley Kubrick', 'DIRECTOR'),
            ('Jack Nicholson', 'ACTOR'),
            ('Shelley Duvall', 'ACTOR'),
            ('Asif Kapadia', 'DIRECTOR'),
            ('Ayrton Senna', 'ACTOR'),
        ]
        people = {}
        for name, role in people_data:
            person, _ = Person.objects.get_or_create(name=name, role=role)
            people[name] = person

        # Create movies with ratings
        movies_data = [
            {
                'title': 'Origen',
                'release_year': 2010,
                'synopsis': 'Un ladrón que roba secretos corporativos mediante el uso de la tecnología de compartir sueños, se le da la tarea inversa de plantar una idea en la mente de un CEO.',
                'genres': ['Acción', 'Ciencia Ficción', 'Thriller'],
                'cast': ['Christopher Nolan', 'Leonardo DiCaprio', 'Tom Hardy'],
                'ratings': [(5, 'Obra maestra del cine moderno'), (5, 'Increíble concepto'), (4, 'Complejo pero gratificante'), (5, 'Nolan en su mejor momento'), (4, 'Visuales impresionantes')],
            },
            {
                'title': 'El Caballero Oscuro',
                'release_year': 2008,
                'synopsis': 'Batman forma una alianza con el teniente Gordon y el fiscal Harvey Dent para acabar con el crimen organizado en Gotham, pero se enfrenta al caos del Joker.',
                'genres': ['Acción', 'Crimen', 'Drama', 'Thriller'],
                'cast': ['Christopher Nolan', 'Christian Bale', 'Heath Ledger'],
                'ratings': [(5, 'La mejor película de superhéroes'), (5, 'Heath Ledger es legendario'), (5, 'Perfecta en todo sentido'), (4, 'Oscura y madura'), (5, 'Un clásico instantáneo')],
            },
            {
                'title': 'Dune',
                'release_year': 2021,
                'synopsis': 'Paul Atreides, un joven brillante y talentoso, debe viajar al planeta más peligroso del universo para asegurar el futuro de su familia y su pueblo.',
                'genres': ['Ciencia Ficción', 'Aventura', 'Drama'],
                'cast': ['Denis Villeneuve', 'Timothée Chalamet', 'Zendaya'],
                'ratings': [(5, 'Epica visual'), (4, 'Fiel al libro'), (5, 'Hans Zimmer otra vez'), (4, 'Espera la parte 2'), (5, 'Cinema puro')],
            },
            {
                'title': 'Barbie',
                'release_year': 2023,
                'synopsis': 'Barbie sufre una crisis que la lleva a cuestionar su mundo y su existencia, embarcándose en un viaje de autodescubrimiento.',
                'genres': ['Comedia', 'Aventura', 'Fantasía'],
                'cast': ['Greta Gerwig', 'Margot Robbie', 'Ryan Gosling'],
                'ratings': [(5, 'Más profunda de lo que parece'), (4, 'Divertida y emotiva'), (5, 'Ken es todo'), (4, 'Gran dirección'), (5, 'Rosa por doquier')],
            },
            {
                'title': 'Parásitos',
                'release_year': 2019,
                'synopsis': 'Una familia pobre se infiltra en la vida de una familia rica, pero un incidente inesperado cambia todo.',
                'genres': ['Drama', 'Thriller', 'Crimen'],
                'cast': ['Bong Joon-ho', 'Song Kang-ho'],
                'ratings': [(5, 'Maestra del suspenso'), (5, 'Mejor película 2019'), (4, 'Giro inesperado'), (5, 'Comentario social brillante'), (5, 'Perfecta')],
            },
            {
                'title': '¡Huye!',
                'release_year': 2017,
                'synopsis': 'Un joven afroamericano visita a la familia de su novia blanca, descubriendo un secreto aterrador.',
                'genres': ['Terror', 'Thriller', 'Misterio'],
                'cast': ['Jordan Peele', 'Daniel Kaluuya'],
                'ratings': [(5, 'Terror inteligente'), (4, 'Muy original'), (5, 'Peele es genio'), (4, 'Incómoda y necesaria'), (5, 'Mejor terror moderno')],
            },
            {
                'title': 'La Forma del Agua',
                'release_year': 2017,
                'synopsis': 'En 1962, una mujer muda que trabaja en un laboratorio gubernamental descubre una criatura misteriosa y forma un vínculo con ella.',
                'genres': ['Fantasía', 'Romance', 'Drama'],
                'cast': ['Guillermo del Toro', 'Sally Hawkins', 'Doug Jones'],
                'ratings': [(5, 'Del Toro en estado puro'), (4, 'Visualmente hermosa'), (5, 'Historia de amor única'), (4, 'Oscar merecido'), (5, 'Magia cinematográfica')],
            },
            {
                'title': 'El Viaje de Chihiro',
                'release_year': 2001,
                'synopsis': 'Una niña de 10 años entra en un mundo de espíritus y debe trabajar en un balneario para salvar a sus padres transformados en cerdos.',
                'genres': ['Animación', 'Fantasía', 'Aventura'],
                'cast': ['Hayao Miyazaki', 'Rinko Kikuchi'],
                'ratings': [(5, 'Obra maestra de Ghibli'), (5, 'Mejor animación ever'), (4, 'Mundo increíble'), (5, 'Emotiva y mágica'), (5, 'Perfecta en todo')],
            },
            {
                'title': 'Interestelar',
                'release_year': 2014,
                'synopsis': 'Un equipo de exploradores viaja a través de un agujero de gusano para encontrar un nuevo hogar para la humanidad.',
                'genres': ['Ciencia Ficción', 'Aventura', 'Drama'],
                'cast': ['Christopher Nolan', 'Matthew McConaughey', 'Anne Hathaway'],
                'ratings': [(5, 'Ciencia y emoción'), (4, 'Hans Zimmer épico'), (5, 'El final me rompió'), (4, 'Visuales alucinantes'), (5, 'Nolan + espacio = oro')],
            },
            {
                'title': 'Whiplash',
                'release_year': 2014,
                'synopsis': 'Un joven baterista de jazz persigue la grandeza bajo la tutela de un instructor brutal e implacable.',
                'genres': ['Drama', 'Música'],
                'cast': ['Damien Chazelle', 'Miles Teller', 'J.K. Simmons'],
                'ratings': [(5, 'Intensa y adictiva'), (5, 'J.K. Simmons increíble'), (4, 'El final... wow'), (5, 'Mejor película sobre música'), (4, 'Ansiedad pura')],
            },
            {
                'title': 'El Resplandor',
                'release_year': 1980,
                'synopsis': 'Un escritor acepta ser cuidador de un hotel aislado durante el invierno, pero la presencia sobrenatural afecta su cordura.',
                'genres': ['Terror', 'Drama', 'Misterio'],
                'cast': ['Stanley Kubrick', 'Jack Nicholson', 'Shelley Duvall'],
                'ratings': [(5, 'Terror psicológico perfecto'), (5, 'Kubrick genio'), (4, 'Atmosfera inigualable'), (5, 'Jack Nicholson icónico'), (4, 'Clásico absoluto')],
            },
            {
                'title': 'Senna',
                'release_year': 2010,
                'synopsis': 'Documental sobre la vida del piloto brasileño Ayrton Senna, su carrera en la Fórmula 1 y su trágico final.',
                'genres': ['Documental', 'Deportes', 'Drama'],
                'cast': ['Asif Kapadia', 'Ayrton Senna'],
                'ratings': [(5, 'Emocionante y bello'), (4, 'No hace falta saber de F1'), (5, 'Mejor documental deportivo'), (4, 'Montaje brillante'), (5, 'Lágrimas al final')],
            },
        ]

        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                release_year=movie_data['release_year'],
                defaults={
                    'synopsis': movie_data['synopsis'],
                }
            )
            if created:
                movie.genres.set([genres[g] for g in movie_data['genres']])
                movie.cast.set([people[p] for p in movie_data['cast']])

                for score, comment in movie_data['ratings']:
                    Rating.objects.create(
                        movie=movie,
                        score=score,
                        comment=comment
                    )
                self.stdout.write(f'  Created: {movie.title} ({len(movie_data["ratings"])} ratings)')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))


        # Summary
        self.stdout.write(f'\nGenres: {Genre.objects.count()}')
        self.stdout.write(f'People: {Person.objects.count()}')
        self.stdout.write(f'Movies: {Movie.objects.count()}')
        self.stdout.write(f'Ratings: {Rating.objects.count()}')
movies = [
    {"id": 1, "name": "Inception", "genre": "Sci-Fi"},
    {"id": 2, "name": "The Matrix", "genre": "Sci-Fi"},
    {"id": 3, "name": "Titanic", "genre": "Romance"},
    {"id": 4, "name": "The Notebook", "genre": "Romance"},
    {"id": 5, "name": "Interstellar", "genre": "Sci-Fi"},
    {"id": 6, "name": "Pride and Prejudice", "genre": "Romance"},
]

def recommend_by_genre(genre):
    return [movie for movie in movies if movie["genre"].lower() == genre.lower()]

def main():
    genre = input("What type of movie do you want to see? (e.g. Sci-Fi, Romance): ")
    recommendations = recommend_by_genre(genre)
    if recommendations:
        print("Recommended movies:")
        for movie in recommendations:
            print(f'- {movie["name"]} ({movie["genre"]})')
    else:
        print("Sorry, no recommendations found for that genre.")

if __name__ == "__main__":
    main()
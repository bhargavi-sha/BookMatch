import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations(user_id):
    """Generates book recommendations for a given user."""

    # Load the datasets
    books_df = pd.read_csv('data/books.csv')
    ratings_df = pd.read_csv('data/ratings.csv')

    # Create a user-item matrix where rows are users, columns are books, and values are ratings.
    # 'fillna(0)' replaces missing ratings with 0.
    user_item_matrix = ratings_df.pivot_table(index='user_id', columns='book_id', values='rating').fillna(0)

    # --- Find Similar Users ---
    try:
        # Calculate the cosine similarity between all users.
        user_similarities = cosine_similarity(user_item_matrix)
        # Create a DataFrame for easier lookup.
        user_sim_df = pd.DataFrame(user_similarities, index=user_item_matrix.index, columns=user_item_matrix.index)

        # Get the top 5 most similar users to our target user (excluding the user themselves).
        similar_users = user_sim_df[user_id].sort_values(ascending=False).iloc[1:6]
    except KeyError:
        # Handle case where the user_id is not in the dataset
        return []

    # --- Generate Recommendations ---
    recommended_books = {}
    user_ratings = user_item_matrix.loc[user_id]

    # Iterate through similar users and the books they've rated.
    for similar_user_id, similarity_score in similar_users.items():
        similar_user_ratings = user_item_matrix.loc[similar_user_id]

        for book_id, rating in similar_user_ratings.items():
            # If the similar user liked the book (rating > 3) and our target user hasn't read it yet...
            if rating > 3 and user_ratings[book_id] == 0:
                # Add the book to our recommendations, weighting it by similarity score.
                if book_id not in recommended_books:
                    recommended_books[book_id] = 0
                recommended_books[book_id] += similarity_score

    # Sort the recommended books by their calculated score.
    sorted_recommendations = sorted(recommended_books.items(), key=lambda item: item[1], reverse=True)

    # Get the book titles for the top recommended book IDs.
    top_books = []
    for book_id, score in sorted_recommendations:
        book_title = books_df.loc[books_df['book_id'] == book_id, 'title'].iloc[0]
        top_books.append(book_title)

    return top_books[:5] # Return top 5 recommendations
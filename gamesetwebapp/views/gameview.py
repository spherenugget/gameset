from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
import requests
from gamesetwebapp.models import Game, Comment
from gamesetwebapp.forms import CommentForm

API_KEY = "08fc1e235cf24be5ba0d1074ea82e2c9"

class GameDetailView(View):
    template_name = "gamesetwebapp/games.html"

    def get_game_data(self, game_id):
        """Fetch game data from the database or API."""
        try:
            # Try to get the game from the database
            game = Game.objects.get(id=game_id)
            return game  # Return the Game object
        except Game.DoesNotExist:
            # If the game does not exist in the database, get it from the API
            api_url = f"https://api.rawg.io/api/games/{game_id}?key={API_KEY}"
            response = requests.get(api_url)
            if response.status_code == 200:
                # Create a Game object from the API response
                game_data = response.json()
                return {
                    'id': game_data.get('id'),
                    'name': game_data.get('name'),
                    'description': game_data.get('description'),
                    'rate': game_data.get('rating'),
                    'image': game_data.get('background_image'),
                    'like_count': 0,  # Default like count
                    'review_count': 0,  # Default review count
                    'comments': []  # No comments from API
                }
            else:
                return None  # Game not found

    def get(self, request, game_id):
        game = self.get_game_data(game_id)
        if game is None:
            return HttpResponse("Game not found", status=404)

        # If game is a dictionary (from API), convert it to a Game object
        if isinstance(game, dict):
            # Create a new Game object if it was fetched from the API
            game_obj = Game(
                id=game['id'],
                name=game['name'],
                description=game['description'],
                rate=game['rate'],
                image=game['image'],
                like_count=game['like_count'],
                review_count=game['review_count']
            )
        else:
            game_obj = game  # It's a Game object from the database

        comments = game_obj.comments.all()  # Fetch comments related to the game
        form = CommentForm()  # Create a new comment form

        return render(request, self.template_name, {
            "game": game_obj,
            "comments": comments,
            "form": form,
        })

    def post(self, request, game_id):
        # Get the game ID from the request
        user_name = request.POST.get('user_name')
        content = request.POST.get('content')

        # Save the comment regardless of game existence
        comment = Comment.objects.create(
            game_id=game_id,  # Use the game_id from the URL
            user_name=user_name,
            content=content
        )

        # Optionally, you can increment the review count if the game exists
        try:
            game = Game.objects.get(id=game_id)
            game.review_count += 1  # Increment the review count
            game.save()  # Save the game to update the review count
        except Game.DoesNotExist:
            pass  # Ignore if the game does not exist

        # Return a JSON response indicating success
        return JsonResponse({'success': True, 'comment': comment.content})

class TrendView(View):
    template_name = "gamesetwebapp/trend.html"

    def get(self, request):
        api_url = f"https://api.rawg.io/api/games?key={API_KEY}&page_size=10&ordering=-rating"
        response = requests.get(api_url)

        if response.status_code == 200:
            trending_games = response.json().get('results', [])
        else:
            trending_games = []

        game_data = []
        for game in trending_games:
            game_data.append({
                "id": game.get("id"),
                "name": game.get("name"),
                "image": game.get("background_image"),
                "rate": game.get("rating"),
                "ratings_count": game.get("ratings_count"),
                "playtime": game.get("playtime"),
            })

        return render(request, self.template_name, {
            'trending_games': game_data,
        })
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
import requests
from gamesetwebapp.models import Game, Comment
from gamesetwebapp.forms import CommentForm

API_KEY = "08fc1e235cf24be5ba0d1074ea82e2c9"

class GameDetailView(TemplateView):
    template_name = "gamesetwebapp/games.html"

    def get(self, request, game_id):
        try:
            # Try to get the game from the database
            game = Game.objects.get(id=game_id)
            game_data = {
                "id": game.id,
                "name": game.name,
                "description": game.description,
                "rate": game.rate,
                "image": game.image.url if game.image else None,
            }
        except Game.DoesNotExist:
            # If the game does not exist in the database, get it from the API
            api_url = f"https://api.rawg.io/api/games/{game_id}?key={API_KEY}"
            response = requests.get(api_url)
            if response.status_code == 200:
                game_data = response.json()
            else:
                return HttpResponse("Game not found", status=404)

        # Fetch comments for the game
        comments = Comment.objects.filter(game_id=game_id)

        # Comment form for adding a new comment
        comment_form = CommentForm()

        context = {
            "game": game_data,
            "comments": comments,
            "comment_form": comment_form,
        }

        return render(request, self.template_name, context)

    def post(self, request, game_id):
        if "add_comment" in request.POST:
            # Handle adding a new comment
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.game_id = game_id
                comment.save()
                return redirect('game-detail', game_id=game_id)

        elif "edit_comment" in request.POST:
            # Handle editing an existing comment
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, id=comment_id)
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('game-detail', game_id=game_id)

        elif "delete_comment" in request.POST:
            # Handle deleting a comment
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()
            return redirect('game-detail', game_id=game_id)

        # Re-render the page with an error if any of the above fail
        comments = Comment.objects.filter(game_id=game_id)
        return render(request, self.template_name, {
            "game": Game.objects.get(id=game_id),
            "comments": comments,
            "comment_form": CommentForm(),
        })

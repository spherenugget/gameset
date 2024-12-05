from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from gamesetwebapp.models import Game

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

        return render(request, self.template_name, {"game": game_data})

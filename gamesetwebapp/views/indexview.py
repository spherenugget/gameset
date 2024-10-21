from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import requests
from gamesetwebapp.models import Game

API_KEY = "08fc1e235cf24be5ba0d1074ea82e2c9"

class IndexView(TemplateView): 
    template_name = 'gamesetwebapp/index.html'

    def get(self, request):
        # Fetch game data from the database
        games = Game.objects.order_by("name")
        
        # Create context from database games
        context = {
            "games": [
                {
                    "name": game.name,
                    "description": game.description,
                    "rate": game.rate,
                    "image": game.image
                }
                for game in games
            ]
        }
        
        # API request to RAWG.io API
        api_url = f"https://api.rawg.io/api/games?key={API_KEY}&dates=2019-09-01,2019-09-30&platforms=18,1,7"
        response = requests.get(api_url)
        
        # Check if the API request was successful (status code 200)
        if response.status_code == 200:
            api_data = response.json()  # Parse the API response to JSON
            context["api_games"] = api_data.get("results", [])  # Add API data to context
        else:
            context["api_games"] = []  # In case of an API error, provide an empty list
        
        # Render the template with both the database games and API data
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))


    
    
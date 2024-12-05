from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
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
            "comments": [
                {
                    "name": game.name,
                    "description": game.description,
                    "rate": game.rate,
                    "image": game.image
                }
                for game in games
            ]
        }
        
        # Pagination parameters
        page = int(request.GET.get("page", 1))  # Default to page 1
        page_size = 19  # Number of games per page
        offset = (page - 1) * page_size

        # API request to RAWG.io API
        api_url = (
            f"https://api.rawg.io/api/games?key={API_KEY}"
            f"&dates=2019-09-01,2019-09-30"
            f"&platforms=18,1,7"
            f"&page={page}"  # Include the page parameter
        )
        response = requests.get(api_url)
        
        # Check if the API request was successful (status code 200)
        if response.status_code == 200:
            api_data = response.json()  # Parse the API response to JSON
            api_results = api_data.get("results", [])
            next_page = page + 1 if api_results else None  # Determine next page availability
            previous_page = page - 1 if page > 1 else None  # Determine previous page availability

            context.update({
                "api_games": api_results,  # Add paginated API data to context
                "next_page": next_page,  # Add next page number to context
                "previous_page": previous_page  # Add previous page number to context
            })
        else:
            context.update({
                "api_games": [],  # In case of an API error, provide an empty list
                "next_page": None,  # No next page
                "previous_page": None  # No previous page
            })
        
        # Render the template with both the database games and API data
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))
    
#get game details
from django.shortcuts import get_object_or_404, render

class GameDetailView(TemplateView):
    template_name = "gamesetwebapp/games.html"

    def get(self, request, game_id):
        try:
            # First, try to fetch the game from your database
            game = Game.objects.get(id=game_id)
            game_data = {
                "id": game.id,
                "name": game.name,
                "description": game.description,
                "rate": game.rate,
                "image": game.image.url if game.image else None,
            }
        except Game.DoesNotExist:
            # If not found in the database, fetch from the RAWG.io API
            api_url = f"https://api.rawg.io/api/games/{game_id}?key={API_KEY}"
            response = requests.get(api_url)
            if response.status_code == 200:
                game_data = response.json()
            else:
                return HttpResponse("Game not found", status=404)

        return render(request, self.template_name, {"game": game_data})


#Trending game views
class TrendView(TemplateView):
    template_name = "gamesetwebapp/trend.html"

    def get(self, request):
        # API request to RAWG.io for games
        api_url = f"https://api.rawg.io/api/games?key={API_KEY}&page_size=40"
        response = requests.get(api_url)

        trending_games = []
        if response.status_code == 200:
            api_data = response.json()
            api_results = api_data.get("results", [])

            # Filter games based on trending criteria
            trending_games = [
                game for game in api_results
                if game.get("rating", 0) > 3.5
                and game.get("ratings_count", 0) > 500
                and game.get("playtime", 0) > 10
            ]

        context = {
            "trending_games": trending_games
        }
        return render(request, self.template_name, context)
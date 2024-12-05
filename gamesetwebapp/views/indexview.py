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
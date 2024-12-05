from pkgutil import get_data
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template import loader
import requests
from gamesetwebapp.forms import CommentForm
from gamesetwebapp.models import Comment, Game

API_KEY = "08fc1e235cf24be5ba0d1074ea82e2c9"

class IndexView(TemplateView): 
    template_name = 'gamesetwebapp/index.html'

    def get(self, request):
        games = Game.objects.order_by("name")
        context = {
            "comments": [
                {
                    "name": game.name,
                    "description": game.description,
                    "rate": game.rate if game.rate > 0 else "Not Rated",
                    "image": game.image
                }
                for game in games
            ]
        }
        page = int(request.GET.get("page", 1))
        page_size = 19
        offset = (page - 1) * page_size

        api_url = (
            f"https://api.rawg.io/api/games?key={API_KEY}"
            f"&dates=2019-09-01,2019-09-30"
            f"&platforms=18,1,7"
            f"&page={page}"
        )
        response = requests.get(api_url)

        if response.status_code == 200:
            api_data = response.json()
            api_results = api_data.get("results", [])
            for game in api_results:
                game['rating'] = game.get('rating', 0)
                if game['rating'] == 0:
                    game['rating'] = "Not Rated"
            next_page = page + 1 if api_results else None
            previous_page = page - 1 if page > 1 else None

            context.update({
                "api_games": api_results,
                "next_page": next_page,
                "previous_page": previous_page
            })
        else:
            context.update({
                "api_games": [],
                "next_page": None,
                "previous_page": None
            })
        
        template = loader.get_template(self.template_name)
        return HttpResponse(template.render(context, request))

def trend(request): 
    return render(request, 'trend.html')

class GameDetailView(TemplateView):
    template_name = "gamesetwebapp/game.html"
    
    def get(self, request, game_id):
        api_url = f"https://api.rawg.io/api/games/{game_id}?key={API_KEY}"
        response = requests.get(api_url)
        if response.status_code == 200:
            game_data = response.json()
        else:
            return HttpResponse("Game not found", status=404)

        comment_form = CommentForm()
        comments = Comment.objects.filter(game_id=game_id)

        return render(request, self.template_name, {
            'game': game_data,
            'comment_form': comment_form,
            'comments': comments,
        })

    def post(self, request, game_id):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.game_id = game_id
            comment.username = f"anonymous#{comment.id or ''}"  # Assign username
            comment.save()
            return redirect('game-detail', game_id=game_id)
        
        comments = Comment.objects.filter(game_id=game_id)
        return render(request, self.template_name, {
            'game': get_data,
            'comment_form': comment_form,
            'comments': comments,
        })

def delete_comment(request, comment_id):
    """Delete a specific comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    game_id = comment.game_id
    comment.delete()
    return redirect('game-detail', game_id=game_id)

def edit_comment(request, comment_id):
    """Edit a specific comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('game-detail', game_id=comment.game_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'gamesetwebapp/edit_comment.html', {'form': form})

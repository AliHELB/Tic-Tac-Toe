import json
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Game
from django.db.models import Count, Q
from django.db.models.functions import TruncDay
from django.contrib.auth.models import User


def home(request):
    context = {
        'games': Game.objects.all()
    }
    return render(request, 'morpion/home.html', context)


class GameListView(ListView):
    model = Game
    template_name = 'morpion/home.html'
    context_object_name = 'games'
    ordering = ['date_posted']

    def get_queryset(self):  # seulement afficher les parties non complètes
        return Game.objects.filter(full=False)


class GameDetailView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = 'morpion/game_detail.html'


class GameCreateForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'gridsize', 'alignement', 'public']
        labels = {
            'title': 'Titre',
            'gridsize': 'Taille de la grille',
            'alignement': 'Alignement',
            'public': 'Publique',
        }

    def clean(self):
        cleaned_data = super().clean()
        alignement = cleaned_data.get('alignement')
        gridsize = cleaned_data.get('gridsize')

        if alignement > gridsize:
            raise forms.ValidationError("L'alignement ne peut pas être plus grand que la taille de la grille.")
        if 3 > gridsize or 3 > alignement:
            raise forms.ValidationError("L'alignement et la taille de la grille doivent être au moins égal à 3")

        return cleaned_data


class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    template_name = 'morpion/game_form.html'
    form_class = GameCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.current_player = self.request.user  # on définit le créateur de la partie en temps que 1er joueur
        form.instance.board = [[None for _ in range(form.instance.gridsize)] for _ in range(form.instance.gridsize)]
        return super().form_valid(form)


class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    template_name = 'morpion/game_form.html'
    form_class = GameCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object.board = [[None for _ in range(self.object.gridsize)] for _ in range(self.object.gridsize)]
        return super().form_valid(form)

    def test_func(self):
        game = self.get_object()
        if self.request.user == game.author:
            return True
        return False


class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Game
    template_name = 'morpion/game_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        game = self.get_object()
        if self.request.user == game.author:
            return True
        return False


class GamePlayView(LoginRequiredMixin, DetailView):
    model = Game
    template_name = 'morpion/game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grid_rows'] = range(self.object.gridsize)
        context['grid_columns'] = range(self.object.gridsize)
        context['gameover'] = self.object.gameover
        return context


class JoinPrivateGameView(LoginRequiredMixin, View):
    template_name = 'morpion/join_private_game.html'

    def get(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=self.kwargs['game_id'], public=False)
        return render(request, self.template_name, {'game': game})

    def post(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=self.kwargs['game_id'], public=False)
        entered_code = request.POST.get('access_code', '')

        if entered_code == game.access_code:
            messages.success(request, f"Vous avez rejoint la partie {game.title}")
            if request.user != game.author:
                game.opponent = request.user
                game.full = True
                game.save()
            return redirect('game-play', pk=game.pk)
        else:
            messages.error(request, "Code d'accès incorrect. Veuillez réessayer.")
            return render(request, self.template_name, {'game': game})


def statistics(request):
    user = request.user
    # Récupérer les données réelles des parties où l'utilisateur est auteur ou opposant
    games_data = Game.objects.filter(Q(author=user) | Q(opponent=user)).annotate(day=TruncDay('date_posted')).values('day').annotate(total_games=Count('id')).order_by('day')

    # Extraire les jours et le nombre de parties jouées pour les utiliser dans le graphique
    days = [entry['day'].strftime('%Y-%m-%d') for entry in games_data]
    games_played = [entry['total_games'] for entry in games_data]

    # Logique pour le classement
    gridsize = request.POST.get('gridsize')
    alignement = request.POST.get('alignement')

    # Calculer le classement des utilisateurs en fonction des jeux gagnés
    users = User.objects.all()
    ranking_data = {}

    for user in users:
        games_won = Game.objects.filter(winner=user, exist_winner=True, gridsize=gridsize, alignement=alignement).count()
        ranking_data[user] = games_won

    rank = {
        'days': days,
        'games_played': games_played,
        'ranking_data': ranking_data,
        'gridsize': gridsize,  # Ajouter la taille du tableau au contexte
        'alignement': alignement,  # Ajouter l'alignement au contexte
    }

    return render(request, 'morpion/statistics.html', rank)


def get_data(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if hasattr(game, 'winner') and game.winner is not None:     #eviter une erreur s'il n'y a pas de gagnant
        winner_username = game.winner.username
    else:
        winner_username = None
    if hasattr(game, 'loser') and game.loser is not None:       #eviter une erreur s'il n'y a pas de perdant
        loser_username = game.loser.username
    else:
        loser_username = None

    data ={
        'board': game.get_board(),
        'gridSize': game.gridsize,
        'authorSymbol': game.author.profile.symbol.url,
        'opponentSymbol': game.opponent.profile.symbol.url,
        'author': game.author.username,
        'opponent': game.opponent.username,
        'gameOver': game.gameover,
        'winner': winner_username,
        'loser': loser_username,
        'current_player': game.current_player,
        'alignement': game.alignement,
        'isff': game.is_ff,
    }
    return JsonResponse({'game': data})


def join_public_game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.user != game.author:
        game.opponent = request.user
        game.full = True
        game.save()
    return redirect('game-play', pk=game_id)


@csrf_exempt
@require_POST
def make_move(request, pk):
    game = get_object_or_404(Game, id=pk)
    data = json.loads(request.body.decode('utf-8'))
    row = data.get('row')
    col = data.get('col')
    if game.exist_winner:
        return JsonResponse({'error': "la partie est terminée"})
    elif request.user.username != game.current_player:
        return JsonResponse({'error': "ce n'est pas votre tour"})
    else:
        if game.current_player == game.author.username:
            game.board[row][col] = '0'
            game.current_player = game.opponent.username
        else:
            game.board[row][col] = '1'
            game.current_player = game.author.username
        game.save()
    return JsonResponse({'success': True})

@csrf_exempt
@require_POST
def surrender(request, pk):
    game = get_object_or_404(Game, id=pk)
    if request.user == game.author:
        game.winner = game.opponent
        print(game.opponent.username)
    else:
        game.winner = game.author
        print(game.author.username)
    game.loser = request.user
    game.gameover = True
    game.exist_winner = True
    game.is_ff = True
    game.save()
    response_data = {'success': True, 'message': 'Forfait déclaré avec succès.', 'loser': request.user.username}
    return JsonResponse(response_data)

@csrf_exempt
@require_POST
def set_winner(request, pk):
    game = get_object_or_404(Game, id=pk)
    data = json.loads(request.body.decode('utf-8'))
    winner = data.get('winner')
    if winner == game.author.username:
        game.winner = game.author
        game.loser = game.opponent
        game.exist_winner = True;
    else:
        game.winner = game.opponent
        game.loser = game.author
        game.exist_winner = True;
    game.save()
    return JsonResponse({'success': True})
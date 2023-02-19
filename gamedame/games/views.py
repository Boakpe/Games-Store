from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseBadRequest


from .models import CartItem, Game, Purchase, PurchaseItem, Rating


def gameList(request):
    search = request.GET.get('search')
    searched_games = []
    latest_games = []
    best_selling_games = []
    games_on_sale = []

    if (search):
        searched_games = Game.objects.filter(Q(title__icontains=search))
    else:
        latest_games = Game.objects.all().order_by('-release_date')[:4]
        best_selling_games = Game.objects.all().order_by('-copies_sold')[:4]
        games_on_sale = Game.objects.filter(
            promotion__isnull=False).order_by('-promotion')[:4]

    return render(request, 'games/list.html', {'searched_games': searched_games, 'latest_games': latest_games, 'games_on_sale': games_on_sale, 'best_selling_games': best_selling_games})


def gameView(request, id):
    game = get_object_or_404(Game, pk=id)
    has_purchased = PurchaseItem.objects.filter(
        purchase__user=request.user, game=game, refunded=False).exists()
    is_in_cart = CartItem.objects.filter(user=request.user, game=game).exists()

    # Busca todas as avaliações para o jogo e calcula a média das notas
    rating_sum = Rating.objects.filter(game=game).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    return render(request, 'games/game.html', {'game': game, 'has_purchased': has_purchased, 'is_in_cart': is_in_cart, 'rating_sum': rating_sum})



def cartView(request):
    user_cart = CartItem.objects.filter(user=request.user)
    cart_items = CartItem.objects.filter(user=request.user)
    total = 0
    for item in cart_items:
        total += item.game.price_with_discount()
    context = {'cart_items': user_cart,
               'total': total}
    return render(request, 'games/cart.html', context)


def removecartItemView(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    cart_item.delete()
    return redirect('cart-view')


def addcartItemView(request, game_id):
    game = get_object_or_404(Game, id=game_id)

       # Verifica se o jogo já está no carrinho
    try:
        cart_item = CartItem.objects.get(user=request.user, game=game)
        return HttpResponseBadRequest('<script>alert("Este jogo já está no carrinho."); window.history.back();</script>')
    except CartItem.DoesNotExist:
        CartItem.objects.create(user=request.user, game=game)
        return redirect('/cart')


def purchaseView(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if cart_items:
        # Cria um objeto Purchase
        purchase = Purchase.objects.create(user=user)

        # Cria objetos PurchaseItem para cada item do carrinho
        for cart_item in cart_items:
            game = cart_item.game
            price = game.price_with_discount()
            PurchaseItem.objects.create(
                game=game, purchase=purchase, price=price)

        # Remove os itens do carrinho
        cart_items.delete()

        return redirect('/')
    else:
        # Se o carrinho está vazio, redireciona de volta para o carrinho
        return redirect('cart')


def refundGameView(request, game_id):
    # obtém o jogo a ser reembolsado
    game = get_object_or_404(Game, id=game_id)

    # processa o reembolso do jogo
    purchase_items = PurchaseItem.objects.filter(
        game=game, purchase__user=request.user)
    for purchase_item in purchase_items:
        purchase_item.refunded = True
        purchase_item.save()

    return redirect('perfil-view')

@login_required
def add_rating(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    user = request.user
    rating = int(request.POST.get('rating', 0))
    
    if rating > 0:
        rating, created = Rating.objects.update_or_create(user=user, game=game, defaults={'rating': rating})
    
    return redirect('game-view', id = game.id)
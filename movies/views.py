from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition, Vote, Like
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term, hidden=False)
    else:
        movies = Movie.objects.filter(hidden=False)

    # Add like status for each movie
    for movie in movies:
        movie.user_liked = movie.user_has_liked(request.user) if request.user.is_authenticated else False

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

def hidden_movies(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term, hidden=True)
    else:
        movies = Movie.objects.filter(hidden=True)

    template_data = {}
    template_data['title'] = 'Hidden Movies'
    template_data['movies'] = movies
    return render(request, 'movies/hidden.html', {'template_data': template_data})

@login_required
def hide_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.hidden = True
    movie.save()
    return redirect('movies.index')

@login_required
def unhide_movie(request, id):
    movie = get_object_or_404(Movie, id=id)
    movie.hidden = False
    movie.save()
    return redirect('movies.hidden')

@login_required
def petition(request):
    if request.method == 'POST' and request.POST.get('movie_title', '').strip():
        petition = Petition()
        petition.movie_title = request.POST['movie_title'].strip()
        petition.director = request.POST.get('director', '').strip()
        petition.year = request.POST.get('year') or None
        petition.reason = request.POST.get('reason', '').strip()
        petition.user = request.user
        petition.save()
        return redirect('movies.petition')

    petitions = Petition.objects.all().order_by('-created_at')

    # Add voting status for each petition
    for petition in petitions:
        petition.user_voted = petition.user_has_voted(request.user) if request.user.is_authenticated else False

    template_data = {}
    template_data['title'] = 'Movie Petition'
    template_data['petitions'] = petitions
    return render(request, 'movies/petition.html', {'template_data': template_data})

@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)

    vote, created = Vote.objects.get_or_create(
        petition=petition,
        user=request.user
    )

    if not created:
        vote.delete()
        voted = False
    else:
        voted = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'voted': voted,
            'vote_count': petition.vote_count()
        })

    return redirect('movies.petition')


@login_required
def like_movie(request, id):
    movie = get_object_or_404(Movie, id=id)

    like, created = Like.objects.get_or_create(
        movie=movie,
        user=request.user
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': movie.like_count()
        })

    return redirect('movies.index')
from asgiref.sync import sync_to_async

from bot_backend.models import User, Post


@sync_to_async
def get_user(user_id) -> User:
    user = User.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def create_user(user_id, name, second_name, number, email, nickname, city):
    try:
        user = User(
            user_id=user_id,
            nickname=nickname,
            number=number,
            name=name,
            second_name=second_name,
            email=email,
            city=city,
        )
        user.save()
        return user
    except Exception:
        return get_user(user_id)


@sync_to_async
def create_post(album, description, date):
    post = Post(album=album, description=description, date=date)
    post.save()
    return post


@sync_to_async
def get_post(date) -> Post:
    post = Post.objects.filter(date=date).all()
    return post

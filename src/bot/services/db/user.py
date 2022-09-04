from asgiref.sync import sync_to_async

from bot_backend.models import User, Member, Chanel


@sync_to_async
def get_user(user_id) -> User:
    user = User.objects.filter(user_id=user_id).first()
    if not user:
        user = Member.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def create_member(user_id, invite_user):
    user = User.objects.filter(user_id=invite_user).first()
    user.count_members += 1
    member = Member(user_id=user_id, active=True, invite_user=user)
    member.save()
    user.save()


@sync_to_async
def create_channel(user_id, channel_id, name):
    user = User.objects.filter(user_id=user_id).first()
    channel = Chanel(user=user, chat_id=channel_id, name_channel=name)
    channel.save()


@sync_to_async
def get_user_channel(channel_id):
    return Chanel.objects.filter(chat_id=channel_id).first().user.user_id


@sync_to_async
def get_channels(user_id):
    user = User.objects.filter(user_id=user_id).first()
    return Chanel.objects.filter(user=user)


@sync_to_async
def delete_channel(channel_id):
    Chanel.objects.filter(chat_id=channel_id).first().delete()


@sync_to_async
def create_user(user_id, name, number, nickname):
    print(user_id)
    try:
        user = User(
            user_id=user_id,
            nickname=nickname,
            number=number,
            name=name,
            count_members=0,
            active=True,
        )
        user.save()
        return user
    except Exception:
        return get_user(user_id)

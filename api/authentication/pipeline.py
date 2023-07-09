def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    if not user:
        return

    url = None

    if backend.name == 'google-oauth2':
        url = response.get("picture")

    if url:
        user.avatar = url
        user.save()

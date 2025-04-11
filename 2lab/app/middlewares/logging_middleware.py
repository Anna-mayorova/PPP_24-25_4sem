class LoggingMiddleware:  # нужно дорабатывать
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        print(f"Request received: {scope['path']}")
        await self.app(scope, receive, send)
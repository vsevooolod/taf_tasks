"""Global point for collected routers."""

from app.internal.pkg.models import Routes
from app.internal.routes import tasks, tags

__all__ = ["__routes__"]

__routes__ = Routes(
    routers=(
        tasks.router,
        tags.router,
    ),
)

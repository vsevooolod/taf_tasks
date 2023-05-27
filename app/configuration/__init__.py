"""Server configuration.

Collect or build all requirements for startup. Provide global point to
``Server`` instance.
"""

from app.pkg.models.core import Container, Containers
from app.internal.repositories import Repositories
from app.internal.services import Services
from app.pkg.connectors import Connectors

__all__ = ["__containers__"]

__containers__ = Containers(
    pkg_name=__name__,
    containers=[
        Container(container=Repositories),
        Container(container=Services),
        Container(container=Connectors),
    ],
)

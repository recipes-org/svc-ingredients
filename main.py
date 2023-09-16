import logging

from ingredients.app import create_app


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

app = create_app()

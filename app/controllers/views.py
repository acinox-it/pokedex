"""View controllers for HTML pages"""
import logging
from fastapi import HTTPException
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from app.database import PokemonRepository
from app.config import TEMPLATE_DIR

logger = logging.getLogger(__name__)

# Initialize templates
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# Constant for stat bar calculations
MAX_STAT_VALUE = 250


class ViewController:
    """Controller for page views"""

    @staticmethod
    async def home(request: Request):
        """Home page displaying list of Pokémons"""
        try:
            pokemons = await PokemonRepository.get_all()
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "pokemons": pokemons,
                    "total": len(pokemons)
                }
            )
        except Exception as err:
            logger.error(f"Error loading home page: {err}")
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    async def pokemon_detail(request: Request, name: str):
        """Details page for a single Pokémon"""
        try:
            pokemon = await PokemonRepository.get_by_name(name)
            if not pokemon:
                raise HTTPException(status_code=404, detail="Pokémon not found")
            
            return templates.TemplateResponse(
                "detail.html",
                {
                    "request": request,
                    "pokemon": pokemon,
                    "maxStatValue": MAX_STAT_VALUE
                }
            )
        except HTTPException:
            raise
        except Exception as err:
            logger.error(f"Error loading pokemon detail '{name}': {err}")
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    async def add_page(request: Request):
        """Page for adding a new Pokémon"""
        return templates.TemplateResponse("add.html", {"request": request})

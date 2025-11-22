"""API controllers for Pokémon operations"""
import logging
from fastapi import HTTPException
from typing import Dict, Any
from app.database import PokemonRepository
from app.schemas import PokemonCreate

logger = logging.getLogger(__name__)


class PokemonController:
    """Controller for Pokémon API endpoints"""

    @staticmethod
    async def get_all_pokemons() -> Dict[str, Any]:
        """Get all Pokémons"""
        try:
            pokemons = await PokemonRepository.get_all()
            return {
                "count": len(pokemons),
                "data": pokemons
            }
        except Exception as err:
            logger.error(f"Error fetching all pokemons: {err}")
            raise HTTPException(status_code=500, detail="Failed to fetch pokemons")

    @staticmethod
    async def search_pokemons(q: str) -> Dict[str, Any]:
        """Search Pokémons by name or type"""
        if not q or not q.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        try:
            results = await PokemonRepository.search(q.strip())
            return {
                "query": q.strip(),
                "count": len(results),
                "data": results
            }
        except Exception as err:
            logger.error(f"Search error for '{q}': {err}")
            raise HTTPException(status_code=500, detail="Search failed")

    @staticmethod
    async def create_pokemon(pokemon: PokemonCreate) -> Dict[str, Any]:
        """Create a new Pokémon"""
        try:
            pokemon_data = pokemon.model_dump()
            success = await PokemonRepository.create(pokemon_data)
            
            if not success:
                raise HTTPException(status_code=400, detail="Error creating Pokémon")
            
            return {
                "status": "success",
                "message": f"Pokémon '{pokemon.name}' created successfully",
                "pokemon": pokemon_data
            }
        except HTTPException:
            raise
        except Exception as err:
            logger.error(f"Error creating pokemon: {err}")
            raise HTTPException(status_code=500, detail=f"Failed to create pokemon: {str(err)}")

    @staticmethod
    async def get_pokemon_stats() -> Dict[str, Any]:
        """Get global Pokémon statistics"""
        try:
            stats = await PokemonRepository.get_stats()
            return stats if stats else {
                "count": 0,
                "avg_hp": 0,
                "avg_attack": 0,
                "avg_defense": 0,
                "avg_sp_attack": 0,
                "avg_sp_defense": 0,
                "avg_speed": 0
            }
        except Exception as err:
            logger.error(f"Error fetching stats: {err}")
            raise HTTPException(status_code=500, detail="Failed to fetch statistics")


class HealthController:
    """Controller for health check endpoints"""

    @staticmethod
    async def health_check() -> Dict[str, str]:
        """Health check endpoint"""
        return {"status": "ok", "service": "pokedex", "version": "1.0.0"}

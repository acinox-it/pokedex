"""
MySQL database connection management
"""
import mysql.connector
from mysql.connector import Error
from typing import List, Optional, Dict, Any
from fastapi import Depends
from fastapi.concurrency import run_in_threadpool
from app.config import DB_CONFIG


class DatabaseConnection:
    """Manages database connection"""
    
    @staticmethod
    def get_connection():
        """Gets a new database connection"""
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            return connection
        except Error as err:
            if err.errno == 2003:
                raise Exception("Cannot connect to MySQL server") from err
            elif err.errno == 1045:
                raise Exception("Access denied - check your credentials in .env") from err
            raise Exception(f"Database error: {err}") from err

    @staticmethod
    def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Executes a SELECT query and returns results"""
        connection = None
        cursor = None
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as err:
            raise Exception(f"Query execution error: {err}") from err
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def execute_update(query: str, params: tuple = ()) -> bool:
        """Executes an INSERT/UPDATE/DELETE query"""
        connection = None
        cursor = None
        try:
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            return True
        except Error as err:
            if connection:
                connection.rollback()
            raise Exception(f"Update execution error: {err}") from err
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


class PokemonRepository:
    """Manages Pokemon operations"""
    
    @staticmethod
    async def get_all() -> List[Dict[str, Any]]:
        """Retrieves all Pokemon"""
        query = """
            SELECT id, name, types, hp, attack, defense, 
                   sp_attack, sp_defense, speed, created_at, updated_at
            FROM pokemon
            ORDER BY id
        """
        return await run_in_threadpool(DatabaseConnection.execute_query, query)

    @staticmethod
    async def get_by_id(pokemon_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a Pokemon by ID"""
        query = """
            SELECT id, name, types, hp, attack, defense, 
                   sp_attack, sp_defense, speed, created_at, updated_at
            FROM pokemon
            WHERE id = %s
        """
        results = await run_in_threadpool(DatabaseConnection.execute_query, query, (pokemon_id,))
        return results[0] if results else None

    @staticmethod
    async def get_by_name(name: str) -> Optional[Dict[str, Any]]:
        """Retrieves a Pokemon by name"""
        query = """
            SELECT id, name, types, hp, attack, defense, 
                   sp_attack, sp_defense, speed, created_at, updated_at
            FROM pokemon
            WHERE LOWER(name) = LOWER(%s)
        """
        results = await run_in_threadpool(DatabaseConnection.execute_query, query, (name,))
        return results[0] if results else None

    @staticmethod
    async def search(query_term: str) -> List[Dict[str, Any]]:
        """Searches Pokemon by name or type"""
        query = """
            SELECT id, name, types, hp, attack, defense, 
                   sp_attack, sp_defense, speed, created_at, updated_at
            FROM pokemon
            WHERE LOWER(name) LIKE LOWER(%s) 
               OR LOWER(types) LIKE LOWER(%s)
            ORDER BY name
        """
        search_term = f"%{query_term}%"
        return await run_in_threadpool(DatabaseConnection.execute_query, query, (search_term, search_term))

    @staticmethod
    async def create(data: Dict[str, Any]) -> bool:
        """Creates a new Pokemon"""
        query = """
            INSERT INTO pokemon 
            (id, name, types, hp, attack, defense, sp_attack, sp_defense, speed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data.get("id"),
            data.get("name"),
            data.get("types"),
            data.get("hp"),
            data.get("attack"),
            data.get("defense"),
            data.get("sp_attack"),
            data.get("sp_defense"),
            data.get("speed"),
        )
        return await run_in_threadpool(DatabaseConnection.execute_update, query, params)

    @staticmethod
    async def get_stats() -> Dict[str, Any]:
        """Retrieves global Pokemon statistics (via SQL)"""
        query = """
            SELECT 
                COUNT(*) as count,
                ROUND(AVG(hp), 2) as avg_hp,
                ROUND(AVG(attack), 2) as avg_attack,
                ROUND(AVG(defense), 2) as avg_defense,
                ROUND(AVG(sp_attack), 2) as avg_sp_attack,
                ROUND(AVG(sp_defense), 2) as avg_sp_defense,
                ROUND(AVG(speed), 2) as avg_speed,
                MAX(hp) as max_hp,
                MAX(attack) as max_attack,
                MIN(hp) as min_hp,
                MIN(attack) as min_attack
            FROM pokemon
        """
        result = await run_in_threadpool(DatabaseConnection.execute_query, query)
        return result[0] if result else {}

    @staticmethod
    async def count() -> int:
        """Counts the number of Pokemon"""
        query = "SELECT COUNT(*) as count FROM pokemon"
        result = await run_in_threadpool(DatabaseConnection.execute_query, query)
        return result[0]["count"] if result else 0

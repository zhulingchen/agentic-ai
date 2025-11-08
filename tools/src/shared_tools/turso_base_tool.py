from abc import abstractmethod
from crewai.tools import BaseTool
import libsql
import os


class TursoBaseTool(BaseTool):
    """Base class for all Turso database tools with shared connection logic."""
    
    def _get_connection(self):
        """
        Establish connection to Turso database using environment variables.
        
        Returns:
            libsql.Connection: Database connection object
            
        Raises:
            ValueError: If required environment variables are not set
        """
        database_url = os.getenv("TURSO_DATABASE_URL")
        auth_token = os.getenv("TURSO_AUTH_TOKEN")
        
        if (not database_url) or (not auth_token):
            raise ValueError(
                "TURSO_DATABASE_URL and TURSO_AUTH_TOKEN must be set in environment variables"
            )
        
        conn = libsql.connect(
            database=database_url,
            auth_token=auth_token,
        )
        return conn
    
    @abstractmethod
    def _run(self, **kwargs) -> str:
        """
        Abstract method to be implemented by subclasses.
        Each tool should implement its specific database operations.
        """
        pass

"""
Serviço para integração com Spotify (geração de links de busca).
"""
from urllib.parse import quote
from typing import Dict


class SpotifyService:
    """Serviço para geração de links de busca do Spotify."""
    
    SEARCH_BASE_URL = "https://open.spotify.com/search"
    
    @staticmethod
    def generate_search_url(title: str, artist: str) -> str:
        """
        Gera URL de busca do Spotify para uma música.
        
        Args:
            title: Título da música
            artist: Nome do artista
        
        Returns:
            URL completa de busca no Spotify
        """
        # Limpa e formata a query de busca
        query = f"{title} {artist}"
        query_clean = SpotifyService._clean_query(query)
        query_encoded = quote(query_clean)
        
        return f"{SpotifyService.SEARCH_BASE_URL}/{query_encoded}"
    
    @staticmethod
    def _clean_query(query: str) -> str:
        """
        Limpa a query removendo caracteres especiais que podem atrapalhar a busca.
        
        Args:
            query: String original
        
        Returns:
            String limpa
        """
        # Remove caracteres problemáticos comuns
        replacements = {
            ' Featuring ': ' ',
            ' feat. ': ' ',
            ' feat ': ' ',
            ' ft. ': ' ',
            ' ft ': ' ',
            ' & ': ' ',
            ' x ': ' ',
            '  ': ' '  # Espaços duplos
        }
        
        cleaned = query
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        # Remove caracteres especiais mas mantém letras, números e espaços
        cleaned = ''.join(char for char in cleaned if char.isalnum() or char.isspace())
        
        return cleaned.strip()
    
    @staticmethod
    def get_embed_url(spotify_track_id: str) -> str:
        """
        Gera URL de embed do Spotify (para uso futuro se implementar API).
        
        Args:
            spotify_track_id: ID da track no Spotify
        
        Returns:
            URL de embed
        """
        return f"https://open.spotify.com/embed/track/{spotify_track_id}"
"""
Serviço para consulta de dados da Billboard Hot 100 via dataset Kaggle.
"""
import pandas as pd
import streamlit as st
from typing import List, Dict, Optional
from datetime import datetime
import os


class BillboardService:
    """Serviço para consulta do chart Billboard Hot 100 via dataset."""
    
    _dataset_path = None
    _df_hot_stuff = None
    _df_audio_features = None
    
    @staticmethod
    def initialize_dataset(dataset_path: str = None):
        """
        Inicializa o dataset carregando os arquivos CSV.
        
        Args:
            dataset_path: Caminho para a pasta do dataset (opcional)
        """
        if dataset_path:
            BillboardService._dataset_path = dataset_path
        
        if BillboardService._df_hot_stuff is None:
            try:
                # Se não foi fornecido caminho, tenta baixar
                if not BillboardService._dataset_path:
                    import kagglehub
                    BillboardService._dataset_path = kagglehub.dataset_download(
                        "thedevastator/billboard-hot-100-audio-features"
                    )
                
                # Carrega os CSVs
                hot_stuff_path = os.path.join(BillboardService._dataset_path, "Hot Stuff.csv")
                audio_features_path = os.path.join(BillboardService._dataset_path, "Hot 100 Audio Features.csv")
                
                BillboardService._df_hot_stuff = pd.read_csv(hot_stuff_path)
                BillboardService._df_audio_features = pd.read_csv(audio_features_path)
                
                # Converte WeekID para datetime
                BillboardService._df_hot_stuff['WeekID'] = pd.to_datetime(
                    BillboardService._df_hot_stuff['WeekID']
                )
                
            except Exception as e:
                st.error(f"Erro ao carregar dataset: {str(e)}")
                return False
        
        return True
    
    @staticmethod
    @st.cache_data(ttl=86400)
    def get_chart(date_str: str) -> Optional[List[Dict[str, any]]]:
        """
        Busca o chart da Billboard para uma data específica.
        
        Args:
            date_str: Data no formato YYYY-MM-DD
        
        Returns:
            Lista de dicionários com os dados das músicas ou None em caso de erro
        """
        # Garante que o dataset está carregado
        if not BillboardService.initialize_dataset():
            return None
        
        try:
            # Converte a string de data para datetime
            target_date = pd.to_datetime(date_str)
            
            # Filtra pelo mês e ano
            df_filtered = BillboardService._df_hot_stuff[
                (BillboardService._df_hot_stuff['WeekID'].dt.year == target_date.year) &
                (BillboardService._df_hot_stuff['WeekID'].dt.month == target_date.month)
            ]
            
            if df_filtered.empty:
                return None
            
            # Pega a semana mais próxima da data solicitada
            df_week = df_filtered.sort_values('WeekID').iloc[0:100]
            
            # Ordena por posição
            df_week = df_week.sort_values('Week Position')
            
            # Converte para lista de dicionários
            songs = []
            for _, row in df_week.iterrows():
                songs.append({
                    'rank': int(row['Week Position']),
                    'title': str(row['Song']),
                    'artist': str(row['Performer']),
                    'weeks_on_chart': int(row['Weeks on Chart']) if pd.notna(row['Weeks on Chart']) else 0,
                    'last_week': int(row['Previous Week Position']) if pd.notna(row['Previous Week Position']) else None,
                    'peak_pos': int(row['Peak Position']) if pd.notna(row['Peak Position']) else None,
                    'isNew': row['Previous Week Position'] == 0 if pd.notna(row['Previous Week Position']) else False
                })
            
            return songs if len(songs) > 0 else None
            
        except Exception as e:
            st.error(f"Erro ao processar dados: {str(e)}")
            return None
    
    @staticmethod
    def get_available_date_range() -> tuple:
        """
        Retorna o range de datas disponíveis no dataset.
        
        Returns:
            Tuple (ano_inicial, ano_final)
        """
        if not BillboardService.initialize_dataset():
            return (1958, datetime.now().year)
        
        try:
            min_date = BillboardService._df_hot_stuff['WeekID'].min()
            max_date = BillboardService._df_hot_stuff['WeekID'].max()
            return (min_date.year, max_date.year)
        except:
            return (1958, datetime.now().year)
    
    @staticmethod
    def get_available_weeks() -> List[str]:
        """
        Retorna todas as semanas disponíveis no dataset.
        
        Returns:
            Lista de datas no formato YYYY-MM-DD
        """
        if not BillboardService.initialize_dataset():
            return []
        
        try:
            weeks = BillboardService._df_hot_stuff['WeekID'].unique()
            return sorted([str(w.date()) for w in weeks])
        except:
            return []
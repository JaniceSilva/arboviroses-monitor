import os
import sys
import json
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import pandas as pd
import numpy as np

# Adicionar o diretório pai para importar módulos do projeto principal
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

try:
    from src.models import ArbovirusMLModels
    from src.collectors import RealDataCollector
    from src.preprocessor import RealDataPreprocessor
    from src.alerts import AlertSystem
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    # Fallback para desenvolvimento
    ArbovirusMLModels = None
    RealDataCollector = None
    RealDataPreprocessor = None
    AlertSystem = None

arboviroses_bp = Blueprint('arboviroses', __name__)

# Instâncias globais dos sistemas
ml_system = None
collector = None
preprocessor = None
alert_system = None

def initialize_systems():
    """Inicializa os sistemas se ainda não foram inicializados"""
    global ml_system, collector, preprocessor, alert_system
    
    try:
        if ArbovirusMLModels and ml_system is None:
            ml_system = ArbovirusMLModels()
            # Tentar carregar modelos existentes
            ml_system.load_models()
        
        if RealDataCollector and collector is None:
            collector = RealDataCollector()
        
        if RealDataPreprocessor and preprocessor is None:
            preprocessor = RealDataPreprocessor()
        
        if AlertSystem and alert_system is None:
            alert_system = AlertSystem()
            
    except Exception as e:
        print(f"Erro ao inicializar sistemas: {e}")

@arboviroses_bp.route('/dashboard-data')
def get_dashboard_data():
    """Retorna dados principais para o dashboard"""
    try:
        initialize_systems()
        
        # Dados simulados para demonstração
        current_date = datetime.now()
        
        # Casos atuais (última semana)
        current_cases = {
            'dengue': 28,
            'zika': 12,
            'chikungunya': 8,
            'febre_amarela': 2
        }
        
        # Predições para próximas 4 semanas
        predictions = {
            'dengue': [30, 35, 42, 38],
            'zika': [14, 16, 18, 15],
            'chikungunya': [10, 12, 15, 13],
            'febre_amarela': [3, 4, 5, 4]
        }
        
        # Dados climáticos atuais
        climate_data = {
            'temperatura': 26.5,
            'umidade': 78,
            'precipitacao': 15.2,
            'vento': 12.3
        }
        
        # Nível de alerta
        if alert_system:
            risk_assessment = alert_system.assess_risk_level(current_cases)
            alert_level = risk_assessment.get('overall_risk', 'baixo')
            recommendations = risk_assessment.get('recommendations', [])
        else:
            alert_level = 'medio'
            recommendations = [
                "⚡ ALERTA MÉDIO: Manter vigilância ativa",
                "🔍 Intensificar monitoramento epidemiológico"
            ]
        
        dashboard_data = {
            'timestamp': current_date.isoformat(),
            'current_cases': current_cases,
            'predictions': predictions,
            'climate': climate_data,
            'alert_level': alert_level,
            'recommendations': recommendations,
            'total_cases_week': sum(current_cases.values()),
            'trend': 'increasing'  # ou 'decreasing', 'stable'
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/historical-data')
def get_historical_data():
    """Retorna dados históricos para gráficos"""
    try:
        # Gerar dados históricos simulados para os últimos 12 meses
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        dates = pd.date_range(start=start_date, end=end_date, freq='W')
        
        historical_data = []
        
        for i, date in enumerate(dates):
            week_of_year = date.isocalendar()[1]
            
            # Padrão sazonal para dengue (pico no verão)
            dengue_seasonal = 20 + 15 * np.sin(2 * np.pi * (week_of_year - 10) / 52)
            dengue_cases = max(0, dengue_seasonal + np.random.normal(0, 5))
            
            # Zika com padrão diferente
            zika_cases = max(0, 8 + 5 * np.sin(2 * np.pi * (week_of_year - 5) / 52) + np.random.normal(0, 2))
            
            # Chikungunya
            chik_cases = max(0, 6 + 4 * np.sin(2 * np.pi * (week_of_year - 15) / 52) + np.random.normal(0, 2))
            
            # Febre amarela (mais rara)
            fa_cases = max(0, 1 + 2 * np.sin(2 * np.pi * (week_of_year - 8) / 52) + np.random.normal(0, 1))
            
            historical_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'dengue': int(dengue_cases),
                'zika': int(zika_cases),
                'chikungunya': int(chik_cases),
                'febre_amarela': int(fa_cases)
            })
        
        return jsonify(historical_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/climate-correlation')
def get_climate_correlation():
    """Retorna dados de correlação climática"""
    try:
        # Dados simulados de correlação
        correlation_data = {
            'temperature_correlation': {
                'dengue': 0.72,
                'zika': 0.68,
                'chikungunya': 0.65,
                'febre_amarela': 0.45
            },
            'humidity_correlation': {
                'dengue': 0.58,
                'zika': 0.62,
                'chikungunya': 0.55,
                'febre_amarela': 0.38
            },
            'precipitation_correlation': {
                'dengue': 0.45,
                'zika': 0.42,
                'chikungunya': 0.48,
                'febre_amarela': 0.25
            }
        }
        
        return jsonify(correlation_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/risk-map')
def get_risk_map():
    """Retorna dados para o mapa de risco"""
    try:
        # Dados simulados para diferentes bairros/regiões de Teófilo Otoni
        risk_map_data = [
            {
                'region': 'Centro',
                'lat': -17.8644,
                'lng': -41.5056,
                'risk_level': 'alto',
                'cases': 45,
                'population': 15000
            },
            {
                'region': 'Altino Barbosa',
                'lat': -17.8700,
                'lng': -41.5100,
                'risk_level': 'medio',
                'cases': 28,
                'population': 12000
            },
            {
                'region': 'São Jacinto',
                'lat': -17.8600,
                'lng': -41.5000,
                'risk_level': 'baixo',
                'cases': 12,
                'population': 8000
            },
            {
                'region': 'Grão Pará',
                'lat': -17.8750,
                'lng': -41.5150,
                'risk_level': 'medio',
                'cases': 32,
                'population': 10000
            },
            {
                'region': 'Vila Solidária',
                'lat': -17.8580,
                'lng': -41.4980,
                'risk_level': 'alto',
                'cases': 38,
                'population': 9000
            }
        ]
        
        return jsonify(risk_map_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/predictions/<int:weeks>')
def get_predictions(weeks):
    """Retorna predições para N semanas"""
    try:
        initialize_systems()
        
        if weeks > 12:
            weeks = 12  # Limitar a 12 semanas
        
        # Se o sistema ML estiver disponível, usar predições reais
        if ml_system and hasattr(ml_system, 'trained_models') and ml_system.trained_models:
            # Aqui seria implementada a predição real
            # Por simplicidade, usar dados simulados
            pass
        
        # Gerar predições simuladas
        predictions = []
        base_cases = {'dengue': 25, 'zika': 12, 'chikungunya': 8, 'febre_amarela': 2}
        
        for week in range(1, weeks + 1):
            week_pred = {}
            for disease, base in base_cases.items():
                # Adicionar variação sazonal e aleatória
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * week / 52)
                random_factor = 1 + np.random.normal(0, 0.2)
                week_pred[disease] = max(0, int(base * seasonal_factor * random_factor))
            
            predictions.append({
                'week': week,
                'date': (datetime.now() + timedelta(weeks=week)).strftime('%Y-%m-%d'),
                **week_pred
            })
        
        return jsonify(predictions)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/alerts')
def get_alerts():
    """Retorna alertas ativos e histórico"""
    try:
        initialize_systems()
        
        if alert_system:
            # Obter alertas reais do sistema
            recent_alerts = alert_system.get_alert_history(30)
            status = alert_system.get_current_status()
        else:
            # Dados simulados
            recent_alerts = [
                {
                    'id': 'alert_20250807_090000',
                    'timestamp': datetime.now().isoformat(),
                    'risk_level': 'medio',
                    'alert_level': 1,
                    'diseases': {
                        'dengue': {'predicted_cases': 35, 'risk_level': 'medio'}
                    },
                    'status': 'ativo'
                }
            ]
            status = {
                'system_active': True,
                'recent_alerts_count': 1,
                'highest_recent_risk': 'medio'
            }
        
        return jsonify({
            'recent_alerts': recent_alerts,
            'system_status': status
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/statistics')
def get_statistics():
    """Retorna estatísticas gerais do sistema"""
    try:
        # Estatísticas simuladas
        stats = {
            'total_cases_year': 1247,
            'total_cases_month': 156,
            'most_affected_disease': 'dengue',
            'prediction_accuracy': 0.78,
            'data_sources': 3,
            'last_update': datetime.now().isoformat(),
            'coverage_area': 'Teófilo Otoni - MG',
            'population_monitored': 140000,
            'active_alerts': 2,
            'model_performance': {
                'dengue': 0.82,
                'zika': 0.75,
                'chikungunya': 0.73,
                'febre_amarela': 0.68
            }
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/health')
def health_check():
    """Endpoint de verificação de saúde da API"""
    try:
        initialize_systems()
        
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'ml_system': ml_system is not None,
                'data_collector': collector is not None,
                'preprocessor': preprocessor is not None,
                'alert_system': alert_system is not None
            },
            'version': '1.0.0'
        }
        
        return jsonify(health_status)
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


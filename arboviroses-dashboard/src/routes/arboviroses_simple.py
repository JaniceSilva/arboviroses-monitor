import json
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import random
import math

arboviroses_bp = Blueprint('arboviroses', __name__)

@arboviroses_bp.route('/dashboard-data')
def get_dashboard_data():
    """Retorna dados principais para o dashboard"""
    try:
        current_date = datetime.now()
        
        # Casos atuais simulados
        current_cases = {
            'dengue': random.randint(20, 50),
            'zika': random.randint(8, 20),
            'chikungunya': random.randint(5, 15),
            'febre_amarela': random.randint(1, 5)
        }
        
        # Predições simuladas
        predictions = {
            'dengue': [30, 35, 42, 38],
            'zika': [14, 16, 18, 15],
            'chikungunya': [10, 12, 15, 13],
            'febre_amarela': [3, 4, 5, 4]
        }
        
        # Dados climáticos simulados
        climate_data = {
            'temperatura': round(random.uniform(22, 32), 1),
            'umidade': random.randint(60, 90),
            'precipitacao': round(random.uniform(0, 25), 1),
            'vento': round(random.uniform(8, 20), 1)
        }
        
        # Nível de alerta simulado
        total_cases = sum(current_cases.values())
        if total_cases > 80:
            alert_level = 'alto'
        elif total_cases > 50:
            alert_level = 'medio'
        else:
            alert_level = 'baixo'
        
        recommendations = [
            "⚡ Manter vigilância epidemiológica ativa",
            "🔍 Intensificar monitoramento de casos suspeitos",
            "🏠 Orientar população sobre prevenção",
            "💧 Verificar e eliminar criadouros do mosquito",
            "📊 Atualizar dados semanalmente"
        ]
        
        dashboard_data = {
            'timestamp': current_date.isoformat(),
            'current_cases': current_cases,
            'predictions': predictions,
            'climate': climate_data,
            'alert_level': alert_level,
            'recommendations': recommendations,
            'total_cases_week': sum(current_cases.values()),
            'trend': random.choice(['increasing', 'decreasing', 'stable'])
        }
        
        return jsonify(dashboard_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/historical-data')
def get_historical_data():
    """Retorna dados históricos simulados"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        historical_data = []
        current_date = start_date
        
        while current_date <= end_date:
            week_of_year = current_date.isocalendar()[1]
            
            # Padrão sazonal simulado
            dengue_base = 25 + 15 * math.sin(2 * math.pi * (week_of_year - 10) / 52)
            zika_base = 12 + 8 * math.sin(2 * math.pi * (week_of_year - 5) / 52)
            chik_base = 8 + 6 * math.sin(2 * math.pi * (week_of_year - 15) / 52)
            fa_base = 2 + 2 * math.sin(2 * math.pi * (week_of_year - 8) / 52)
            
            historical_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'dengue': max(0, int(dengue_base + random.uniform(-5, 5))),
                'zika': max(0, int(zika_base + random.uniform(-3, 3))),
                'chikungunya': max(0, int(chik_base + random.uniform(-2, 2))),
                'febre_amarela': max(0, int(fa_base + random.uniform(-1, 1)))
            })
            
            current_date += timedelta(weeks=1)
        
        return jsonify(historical_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/climate-correlation')
def get_climate_correlation():
    """Retorna dados de correlação climática simulados"""
    try:
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
    """Retorna dados simulados para o mapa de risco"""
    try:
        risk_map_data = [
            {
                'region': 'Centro',
                'lat': -17.8644,
                'lng': -41.5056,
                'risk_level': 'alto',
                'cases': random.randint(35, 50),
                'population': 15000
            },
            {
                'region': 'Altino Barbosa',
                'lat': -17.8700,
                'lng': -41.5100,
                'risk_level': 'medio',
                'cases': random.randint(20, 35),
                'population': 12000
            },
            {
                'region': 'São Jacinto',
                'lat': -17.8600,
                'lng': -41.5000,
                'risk_level': 'baixo',
                'cases': random.randint(5, 20),
                'population': 8000
            },
            {
                'region': 'Grão Pará',
                'lat': -17.8750,
                'lng': -41.5150,
                'risk_level': 'medio',
                'cases': random.randint(25, 40),
                'population': 10000
            },
            {
                'region': 'Vila Solidária',
                'lat': -17.8580,
                'lng': -41.4980,
                'risk_level': 'alto',
                'cases': random.randint(30, 45),
                'population': 9000
            }
        ]
        
        return jsonify(risk_map_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/predictions/<int:weeks>')
def get_predictions(weeks):
    """Retorna predições simuladas para N semanas"""
    try:
        if weeks > 12:
            weeks = 12
        
        predictions = []
        base_cases = {'dengue': 25, 'zika': 12, 'chikungunya': 8, 'febre_amarela': 2}
        
        for week in range(1, weeks + 1):
            week_pred = {}
            for disease, base in base_cases.items():
                # Variação sazonal e aleatória simulada
                seasonal_factor = 1 + 0.3 * math.sin(2 * math.pi * week / 52)
                random_factor = 1 + random.uniform(-0.2, 0.2)
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
    """Retorna alertas simulados"""
    try:
        recent_alerts = [
            {
                'id': f'alert_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'timestamp': datetime.now().isoformat(),
                'risk_level': random.choice(['baixo', 'medio', 'alto']),
                'alert_level': random.randint(0, 2),
                'diseases': {
                    'dengue': {'predicted_cases': random.randint(25, 45), 'risk_level': 'medio'}
                },
                'status': 'ativo'
            }
        ]
        
        status = {
            'system_active': True,
            'recent_alerts_count': len(recent_alerts),
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
    """Retorna estatísticas simuladas"""
    try:
        stats = {
            'total_cases_year': random.randint(1000, 1500),
            'total_cases_month': random.randint(100, 200),
            'most_affected_disease': 'dengue',
            'prediction_accuracy': round(random.uniform(0.70, 0.85), 2),
            'data_sources': 3,
            'last_update': datetime.now().isoformat(),
            'coverage_area': 'Teófilo Otoni - MG',
            'population_monitored': 140000,
            'active_alerts': random.randint(1, 3),
            'model_performance': {
                'dengue': round(random.uniform(0.75, 0.85), 2),
                'zika': round(random.uniform(0.70, 0.80), 2),
                'chikungunya': round(random.uniform(0.68, 0.78), 2),
                'febre_amarela': round(random.uniform(0.60, 0.75), 2)
            }
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@arboviroses_bp.route('/health')
def health_check():
    """Endpoint de verificação de saúde da API"""
    try:
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'services': {
                'ml_system': True,
                'data_collector': True,
                'preprocessor': True,
                'alert_system': True
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


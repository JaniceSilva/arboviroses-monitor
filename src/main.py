# ================================================================================================
# SISTEMA PRINCIPAL COM SERVIDOR FLASK
# ================================================================================================

import os
import sys
from pathlib import Path
from flask import Flask, jsonify, render_template

# Adicionar o diretório pai ao path para permitir imports do módulo src
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.collectors import RealDataCollector, Config
from src.database import DatabaseManager
from src.preprocessor import RealDataPreprocessor
from src.models import ArbovirusMLModels
from src.alerts import AlertSystem
from src.reports import ReportGenerator

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o Flask
app = Flask(__name__)

# Rota para a página principal do dashboard
@app.route('/')
def dashboard():
    # Isso assume que você tem um arquivo HTML chamado 'dashboard.html'
    # na pasta 'templates' na raiz do seu projeto.
    return render_template('dashboard.html')

# Rota para a API que o dashboard.js consome
@app.route('/api/arboviroses/dashboard-data')
def get_dashboard_data():
    try:
        # Aqui, você integraria a lógica do seu sistema
        # Para coletar, processar e prever os dados
        # Por enquanto, vamos usar dados fictícios

        # Exemplo de como você chamaria suas classes para obter dados
        # collector = RealDataCollector()
        # data = collector.collect_all_data()
        # preprocessor = RealDataPreprocessor()
        # processed_data = preprocessor.process_all_data(data)
        # model = ArbovirusMLModels()
        # predictions = model.predict_future(processed_data)
        # alert_system = AlertSystem()
        # alert_level = alert_system.assess_risk_level(predictions)

        # Dados de exemplo para o dashboard
        data = {
            "summary_cards": {
                "total_cases_last_week": 125,
                "alerts_active": 3,
                "risk_level": "medium"
            },
            "climate": {
                "temperature": 25.4,
                "humidity": 75,
                "precipitation": 12
            },
            "alert_level": "medium",
            "recommendations": [
                "Intensificar campanhas de conscientização",
                "Focar na eliminação de focos de água parada"
            ],
            "timestamp": "2025-08-09T18:00:00Z"
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Executar o servidor
if __name__ == '__main__':
    app.run(debug=True)
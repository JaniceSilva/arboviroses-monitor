// Dashboard JavaScript para Sistema de Monitoramento de Arboviroses

class ArbovirosesDashboard {
    constructor() {
        this.charts = {};
        this.map = null;
        this.updateInterval = null;
        this.apiBase = '/api/arboviroses';
        
        this.init();
    }

    async init() {
        this.showLoading(true);
        
        try {
            await this.loadDashboardData();
            await this.loadHistoricalData();
            await this.initializeCharts();
            await this.initializeMap();
            
            this.setupEventListeners();
            this.startAutoUpdate();
            
        } catch (error) {
            console.error('Erro ao inicializar dashboard:', error);
            this.showError('Erro ao carregar dados do dashboard');
        } finally {
            this.showLoading(false);
        }
    }

    async loadDashboardData() {
        try {
            const response = await fetch(`${this.apiBase}/dashboard-data`);
            if (!response.ok) throw new Error('Erro ao carregar dados');
            
            const data = await response.json();
            this.updateSummaryCards(data);
            this.updateClimateData(data.climate);
            this.updateAlertBanner(data.alert_level, data.recommendations);
            this.updateLastUpdate(data.timestamp);
            
            return data;
        } catch (error) {
            console.error('Erro ao carregar dados do dashboard:', error);
            throw error;
        }
    }

    async loadHistoricalData() {
        try {
            const response = await fetch(`${this.apiBase}/historical-data`);
            if (!response.ok) throw new Error('Erro ao carregar dados históricos');
            
            const data = await response.json();
            this.historicalData = data;
            return data;
        } catch (error) {
            console.error('Erro ao carregar dados históricos:', error);
            throw error;
        }
    }

    updateSummaryCards(data) {
        const diseases = ['dengue', 'zika', 'chikungunya', 'febre_amarela'];
        
        diseases.forEach(disease => {
            const cases = data.current_cases[disease] || 0;
            const element = document.getElementById(`${disease.replace('_', '-')}-cases`);
            if (element) {
                this.animateNumber(element, cases);
            }
        });
    }

    updateClimateData(climate) {
        const updates = {
            'temperature': `${climate.temperatura}°C`,
            'humidity': `${climate.umidade}%`,
            'precipitation': `${climate.precipitacao} mm`,
            'wind': `${climate.vento} km/h`
        };

        Object.entries(updates).forEach(([id, value]) => {
            const element = document.getElementById(id);
            if (element) {
                element.textContent = value;
            }
        });
    }

    updateAlertBanner(alertLevel, recommendations) {
        const banner = document.getElementById('alert-banner');
        const message = document.getElementById('alert-message');
        const indicator = document.getElementById('alert-level-indicator');
        
        // Atualizar banner
        banner.className = `alert-banner ${alertLevel} show`;
        
        const alertMessages = {
            'baixo': '✅ Situação sob controle - Manter vigilância de rotina',
            'medio': '⚠️ Alerta médio - Intensificar monitoramento',
            'alto': '🚨 Alerta alto - Ações preventivas necessárias',
            'critico': '🚨 Alerta crítico - Medidas de emergência'
        };
        
        message.textContent = alertMessages[alertLevel] || 'Status desconhecido';
        
        // Atualizar indicador de nível
        if (indicator) {
            const badge = indicator.querySelector('.alert-badge');
            if (badge) {
                badge.className = `alert-badge ${alertLevel}`;
                badge.textContent = alertLevel.toUpperCase();
            }
        }
        
        // Atualizar recomendações
        this.updateRecommendations(recommendations);
    }

    updateRecommendations(recommendations) {
        const list = document.getElementById('recommendations-list');
        if (list && recommendations) {
            list.innerHTML = recommendations
                .map(rec => `<li>${rec}</li>`)
                .join('');
        }
    }

    updateLastUpdate(timestamp) {
        const element = document.getElementById('last-update');
        if (element && timestamp) {
            const date = new Date(timestamp);
            element.textContent = date.toLocaleTimeString('pt-BR', {
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    }

    async initializeCharts() {
        await this.createCasesChart();
        await this.createDistributionChart();
        await this.createPredictionsChart();
    }

    async createCasesChart() {
        const ctx = document.getElementById('cases-chart');
        if (!ctx || !this.historicalData) return;

        const data = this.historicalData.slice(-30); // Últimos 30 registros
        
        this.charts.cases = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => new Date(d.date).toLocaleDateString('pt-BR', {
                    month: 'short',
                    day: 'numeric'
                })),
                datasets: [
                    {
                        label: 'Dengue',
                        data: data.map(d => d.dengue),
                        borderColor: '#e53e3e',
                        backgroundColor: 'rgba(229, 62, 62, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Zika',
                        data: data.map(d => d.zika),
                        borderColor: '#3182ce',
                        backgroundColor: 'rgba(49, 130, 206, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Chikungunya',
                        data: data.map(d => d.chikungunya),
                        borderColor: '#38a169',
                        backgroundColor: 'rgba(56, 161, 105, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Febre Amarela',
                        data: data.map(d => d.febre_amarela),
                        borderColor: '#d69e2e',
                        backgroundColor: 'rgba(214, 158, 46, 0.1)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Data'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Número de Casos'
                        },
                        beginAtZero: true
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }

    async createDistributionChart() {
        const ctx = document.getElementById('distribution-chart');
        if (!ctx || !this.historicalData) return;

        // Calcular totais do último mês
        const lastMonth = this.historicalData.slice(-4);
        const totals = {
            dengue: lastMonth.reduce((sum, d) => sum + d.dengue, 0),
            zika: lastMonth.reduce((sum, d) => sum + d.zika, 0),
            chikungunya: lastMonth.reduce((sum, d) => sum + d.chikungunya, 0),
            febre_amarela: lastMonth.reduce((sum, d) => sum + d.febre_amarela, 0)
        };

        this.charts.distribution = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Dengue', 'Zika', 'Chikungunya', 'Febre Amarela'],
                datasets: [{
                    data: [totals.dengue, totals.zika, totals.chikungunya, totals.febre_amarela],
                    backgroundColor: [
                        '#e53e3e',
                        '#3182ce',
                        '#38a169',
                        '#d69e2e'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} casos (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    async createPredictionsChart() {
        const ctx = document.getElementById('predictions-chart');
        if (!ctx) return;

        try {
            const response = await fetch(`${this.apiBase}/predictions/4`);
            const predictions = await response.json();

            const labels = predictions.map(p => new Date(p.date).toLocaleDateString('pt-BR', {
                month: 'short',
                day: 'numeric'
            }));

            this.charts.predictions = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Dengue',
                            data: predictions.map(p => p.dengue),
                            backgroundColor: 'rgba(229, 62, 62, 0.8)',
                            borderColor: '#e53e3e',
                            borderWidth: 1
                        },
                        {
                            label: 'Zika',
                            data: predictions.map(p => p.zika),
                            backgroundColor: 'rgba(49, 130, 206, 0.8)',
                            borderColor: '#3182ce',
                            borderWidth: 1
                        },
                        {
                            label: 'Chikungunya',
                            data: predictions.map(p => p.chikungunya),
                            backgroundColor: 'rgba(56, 161, 105, 0.8)',
                            borderColor: '#38a169',
                            borderWidth: 1
                        },
                        {
                            label: 'Febre Amarela',
                            data: predictions.map(p => p.febre_amarela),
                            backgroundColor: 'rgba(214, 158, 46, 0.8)',
                            borderColor: '#d69e2e',
                            borderWidth: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Semanas Futuras'
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Casos Previstos'
                            },
                            beginAtZero: true
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Erro ao carregar predições:', error);
        }
    }

    async initializeMap() {
        try {
            const mapElement = document.getElementById('risk-map');
            if (!mapElement) return;

            // Inicializar mapa centrado em Teófilo Otoni
            this.map = L.map('risk-map').setView([-17.8644, -41.5056], 12);

            // Adicionar camada de tiles
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(this.map);

            // Carregar dados de risco
            const response = await fetch(`${this.apiBase}/risk-map`);
            const riskData = await response.json();

            // Adicionar marcadores de risco
            riskData.forEach(region => {
                const color = this.getRiskColor(region.risk_level);
                const radius = Math.max(10, region.cases * 2);

                const marker = L.circleMarker([region.lat, region.lng], {
                    radius: radius,
                    fillColor: color,
                    color: color,
                    weight: 2,
                    opacity: 0.8,
                    fillOpacity: 0.6
                }).addTo(this.map);

                marker.bindPopup(`
                    <div style="text-align: center;">
                        <h4>${region.region}</h4>
                        <p><strong>Casos:</strong> ${region.cases}</p>
                        <p><strong>População:</strong> ${region.population.toLocaleString()}</p>
                        <p><strong>Risco:</strong> <span style="color: ${color}; font-weight: bold;">${region.risk_level.toUpperCase()}</span></p>
                    </div>
                `);
            });

        } catch (error) {
            console.error('Erro ao inicializar mapa:', error);
        }
    }

    getRiskColor(riskLevel) {
        const colors = {
            'baixo': '#38a169',
            'medio': '#d69e2e',
            'alto': '#e53e3e',
            'critico': '#9b2c2c'
        };
        return colors[riskLevel] || '#718096';
    }

    setupEventListeners() {
        // Seletor de período
        const periodSelector = document.getElementById('period-selector');
        if (periodSelector) {
            periodSelector.addEventListener('change', (e) => {
                this.updateChartsForPeriod(e.target.value);
            });
        }

        // Atualização manual
        document.addEventListener('keydown', (e) => {
            if (e.key === 'F5' || (e.ctrlKey && e.key === 'r')) {
                e.preventDefault();
                this.refreshData();
            }
        });
    }

    async updateChartsForPeriod(days) {
        try {
            this.showLoading(true);
            
            // Filtrar dados históricos
            const filteredData = this.historicalData.slice(-parseInt(days));
            
            // Atualizar gráfico de casos
            if (this.charts.cases) {
                this.charts.cases.data.labels = filteredData.map(d => 
                    new Date(d.date).toLocaleDateString('pt-BR', {
                        month: 'short',
                        day: 'numeric'
                    })
                );
                
                this.charts.cases.data.datasets.forEach((dataset, index) => {
                    const diseases = ['dengue', 'zika', 'chikungunya', 'febre_amarela'];
                    dataset.data = filteredData.map(d => d[diseases[index]]);
                });
                
                this.charts.cases.update();
            }
            
        } catch (error) {
            console.error('Erro ao atualizar gráficos:', error);
        } finally {
            this.showLoading(false);
        }
    }

    async refreshData() {
        try {
            this.showLoading(true);
            await this.loadDashboardData();
            await this.loadHistoricalData();
            
            // Atualizar gráficos
            Object.values(this.charts).forEach(chart => {
                if (chart && chart.update) {
                    chart.update();
                }
            });
            
        } catch (error) {
            console.error('Erro ao atualizar dados:', error);
            this.showError('Erro ao atualizar dados');
        } finally {
            this.showLoading(false);
        }
    }

    startAutoUpdate() {
        // Atualizar a cada 5 minutos
        this.updateInterval = setInterval(() => {
            this.refreshData();
        }, 5 * 60 * 1000);
    }

    stopAutoUpdate() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
    }

    animateNumber(element, targetValue) {
        const startValue = parseInt(element.textContent) || 0;
        const duration = 1000;
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = Math.floor(startValue + (targetValue - startValue) * progress);
            element.textContent = currentValue;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }

    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.classList.toggle('show', show);
        }
    }

    showError(message) {
        console.error(message);
        // Aqui poderia implementar um toast ou modal de erro
        alert(message);
    }
}

// Funções globais para eventos
function closeAlert() {
    const banner = document.getElementById('alert-banner');
    if (banner) {
        banner.classList.remove('show');
    }
}

function showAbout() {
    alert('Sistema de Monitoramento de Arboviroses v1.0\nDesenvolvido para Teófilo Otoni - MG\n\nEste sistema utiliza inteligência artificial para prever surtos de arboviroses baseado em dados epidemiológicos e climáticos.');
}

function showHelp() {
    alert('Ajuda do Sistema:\n\n• Os gráficos são atualizados automaticamente a cada 5 minutos\n• Use F5 para atualizar manualmente\n• Clique nos marcadores do mapa para ver detalhes por região\n• As predições são baseadas em modelos de IA treinados com dados históricos');
}

function showContact() {
    alert('Contato:\n\nSecretaria Municipal de Saúde\nTeófilo Otoni - MG\n\nTelefone: (33) 3529-2000\nEmail: saude@teofilootoni.mg.gov.br');
}

// Inicializar dashboard quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new ArbovirosesDashboard();
});

// Cleanup ao sair da página
window.addEventListener('beforeunload', () => {
    if (window.dashboard) {
        window.dashboard.stopAutoUpdate();
    }
});


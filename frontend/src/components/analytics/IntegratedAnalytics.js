import React, { useState, useEffect } from 'react';
import './IntegratedAnalytics.css';

const IntegratedAnalytics = () => {
    const [analyticsData, setAnalyticsData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [lastUpdated, setLastUpdated] = useState(null);
    const [autoRefresh, setAutoRefresh] = useState(true);

    const fetchAnalytics = async () => {
        try {
            setLoading(true);
            const response = await fetch('http://localhost:5004/api/analytics/comprehensive');
            const data = await response.json();
            
            if (data.success) {
                setAnalyticsData(data.analytics);
                setLastUpdated(new Date());
                setError(null);
            } else {
                setError(data.error || 'Failed to fetch analytics');
            }
        } catch (err) {
            setError('Network error: ' + err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAnalytics();

        let interval;
        if (autoRefresh) {
            interval = setInterval(fetchAnalytics, 30000); // Refresh every 30 seconds
        }

        return () => {
            if (interval) clearInterval(interval);
        };
    }, [autoRefresh]);

    const getRiskLevelColor = (level) => {
        switch (level?.toLowerCase()) {
            case 'critical': return '#dc3545';
            case 'high': return '#fd7e14';
            case 'medium': return '#ffc107';
            case 'low': return '#28a745';
            case 'minimal': return '#17a2b8';
            default: return '#6c757d';
        }
    };

    const formatTimestamp = (timestamp) => {
        return new Date(timestamp).toLocaleString();
    };

    if (loading && !analyticsData) {
        return (
            <div className="analytics-container">
                <div className="loading-spinner">
                    <div className="spinner"></div>
                    <p>Loading comprehensive analytics...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="analytics-container">
                <div className="error-state">
                    <h3>⚠️ Analytics Error</h3>
                    <p>{error}</p>
                    <button onClick={fetchAnalytics} className="retry-button">
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="analytics-container">
            <div className="analytics-header">
                <h2>🔬 Integrated Supply Chain Analytics</h2>
                <div className="header-controls">
                    <div className="last-updated">
                        Last Updated: {lastUpdated ? formatTimestamp(lastUpdated) : 'Never'}
                    </div>
                    <label className="auto-refresh-toggle">
                        <input
                            type="checkbox"
                            checked={autoRefresh}
                            onChange={(e) => setAutoRefresh(e.target.checked)}
                        />
                        Auto Refresh
                    </label>
                    <button onClick={fetchAnalytics} className="refresh-button" disabled={loading}>
                        {loading ? '🔄' : '↻'} Refresh
                    </button>
                </div>
            </div>

            {analyticsData && (
                <div className="analytics-grid">
                    {/* Risk Assessment Card */}
                    <div className="analytics-card risk-assessment">
                        <h3>⚠️ Risk Assessment</h3>
                        <div className="risk-overview">
                            <div className="risk-score">
                                <span className="score-number">
                                    {analyticsData.risk_assessment?.overall_risk_score || 0}
                                </span>
                                <span className="score-label">/100</span>
                            </div>
                            <div 
                                className="risk-level"
                                style={{ 
                                    color: getRiskLevelColor(analyticsData.risk_assessment?.risk_level)
                                }}
                            >
                                {analyticsData.risk_assessment?.risk_level || 'UNKNOWN'}
                            </div>
                        </div>
                        {analyticsData.risk_assessment?.risk_factors?.length > 0 && (
                            <div className="risk-factors">
                                <h4>Risk Factors:</h4>
                                <ul>
                                    {analyticsData.risk_assessment.risk_factors.map((factor, index) => (
                                        <li key={index}>{factor}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>

                    {/* Anomaly Detection Card */}
                    <div className="analytics-card anomaly-detection">
                        <h3>🔍 Anomaly Detection</h3>
                        {analyticsData.anomaly_detection?.error ? (
                            <div className="no-data">
                                <p>{analyticsData.anomaly_detection.error}</p>
                            </div>
                        ) : (
                            <div className="anomaly-stats">
                                <div className="stat-item">
                                    <span className="stat-label">Records Analyzed:</span>
                                    <span className="stat-value">
                                        {analyticsData.anomaly_detection?.total_checked || 0}
                                    </span>
                                </div>
                                <div className="stat-item">
                                    <span className="stat-label">Anomalies Found:</span>
                                    <span className="stat-value anomaly-count">
                                        {analyticsData.anomaly_detection?.unique_anomalies_count || 0}
                                    </span>
                                </div>
                                <div className="stat-item">
                                    <span className="stat-label">Processing Time:</span>
                                    <span className="stat-value">
                                        {analyticsData.anomaly_detection?.processing_time?.toFixed(3) || 0}s
                                    </span>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Predictive Analytics Card */}
                    <div className="analytics-card predictive-analytics">
                        <h3>🔮 Predictive Analytics</h3>
                        {analyticsData.predictive_analytics?.error ? (
                            <div className="no-data">
                                <p>{analyticsData.predictive_analytics.error}</p>
                            </div>
                        ) : analyticsData.predictive_analytics?.predictions ? (
                            <div className="prediction-stats">
                                <div className="stat-item">
                                    <span className="stat-label">Targets Predicted:</span>
                                    <span className="stat-value">
                                        {Object.keys(analyticsData.predictive_analytics.predictions).length}
                                    </span>
                                </div>
                                <div className="stat-item">
                                    <span className="stat-label">Data Points Used:</span>
                                    <span className="stat-value">
                                        {analyticsData.predictive_analytics.data_points || 0}
                                    </span>
                                </div>
                                <div className="stat-item">
                                    <span className="stat-label">Features Engineered:</span>
                                    <span className="stat-value">
                                        {analyticsData.predictive_analytics.features_engineered || 0}
                                    </span>
                                </div>
                                <div className="predictions-list">
                                    <h4>Predictions:</h4>
                                    {Object.entries(analyticsData.predictive_analytics.predictions).map(([target, data]) => (
                                        <div key={target} className="prediction-item">
                                            <span className="prediction-target">{target}:</span>
                                            <span className="prediction-count">
                                                {data.values?.length || 0} predictions
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ) : (
                            <div className="no-data">
                                <p>No predictions available</p>
                            </div>
                        )}
                    </div>

                    {/* Alerts Card */}
                    <div className="analytics-card alerts">
                        <h3>🚨 Active Alerts</h3>
                        <div className="alerts-count">
                            <span className="alert-number">
                                {analyticsData.alerts?.length || 0}
                            </span>
                            <span className="alert-label">Active Alerts</span>
                        </div>
                        {analyticsData.alerts?.length > 0 ? (
                            <div className="alerts-list">
                                {analyticsData.alerts.slice(0, 3).map((alert, index) => (
                                    <div key={index} className="alert-item">
                                        <div className="alert-type">{alert.type}</div>
                                        <div className="alert-message">{alert.message}</div>
                                        <div className="alert-time">
                                            {formatTimestamp(alert.timestamp)}
                                        </div>
                                    </div>
                                ))}
                                {analyticsData.alerts.length > 3 && (
                                    <div className="more-alerts">
                                        +{analyticsData.alerts.length - 3} more alerts
                                    </div>
                                )}
                            </div>
                        ) : (
                            <div className="no-alerts">
                                <p>✅ No active alerts</p>
                            </div>
                        )}
                    </div>

                    {/* Recommendations Card */}
                    <div className="analytics-card recommendations">
                        <h3>💡 Recommendations</h3>
                        {analyticsData.recommendations?.length > 0 ? (
                            <div className="recommendations-list">
                                {analyticsData.recommendations.map((rec, index) => (
                                    <div key={index} className="recommendation-item">
                                        <span className="rec-number">{index + 1}.</span>
                                        <span className="rec-text">{rec}</span>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="no-recommendations">
                                <p>No specific recommendations at this time</p>
                            </div>
                        )}
                    </div>

                    {/* System Metrics Card */}
                    <div className="analytics-card system-metrics">
                        <h3>📈 System Metrics</h3>
                        <div className="metrics-grid">
                            <div className="metric-item">
                                <span className="metric-label">Total Predictions:</span>
                                <span className="metric-value">
                                    {analyticsData.system_metrics?.total_predictions || 0}
                                </span>
                            </div>
                            <div className="metric-item">
                                <span className="metric-label">Anomalies Detected:</span>
                                <span className="metric-value">
                                    {analyticsData.system_metrics?.anomalies_detected || 0}
                                </span>
                            </div>
                            <div className="metric-item">
                                <span className="metric-label">Alerts Sent:</span>
                                <span className="metric-value">
                                    {analyticsData.system_metrics?.alerts_sent || 0}
                                </span>
                            </div>
                            <div className="metric-item">
                                <span className="metric-label">System Health:</span>
                                <span className="metric-value health-status">
                                    {analyticsData.system_metrics?.system_health || 'Unknown'}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default IntegratedAnalytics;

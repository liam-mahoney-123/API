// Q3 Launch - API Performance Configuration
// These thresholds govern alerting and release gates

module.exports = {
  // P95 latency target for all core API endpoints
  LATENCY_TARGET_P95_MS: 250,

  // Maximum acceptable error rate during beta
  ERROR_RATE_THRESHOLD: 0.01,

  // Health check interval in seconds
  HEALTH_CHECK_INTERVAL: 30,

  // Circuit breaker trip threshold
  CIRCUIT_BREAKER_FAILURES: 5
};

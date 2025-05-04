# Leverage the LLM's natural language understanding to construct a knowledge graph.
## relation
WRITES	Analyst → Report (작성함)
ISSUED_BY	Report → Broker (발행 주체)
TARGETS	Report → Company (대상 기업)
HAS_FORECAST	Company → Forecast (예측 보유)
FORECASTS	Report → Forecast (예측 포함)
OF_METRIC	Forecast → Metric (어떤 지표의 예측인지)

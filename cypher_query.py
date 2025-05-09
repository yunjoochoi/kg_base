import google.generativeai as genai
from neo4j import GraphDatabase

# =Gemini API 설정
genai.configure(api_key="키")
gemini = genai.GenerativeModel("models/gemini-1.5-pro")

# 사용자 질문
user_question = "크래프톤의 2025년 1분기 영업이익 얼마임?"


# Cypher 생성 프롬프트 (지식그래프 구조 반영)
cypher_prompt = f"""
너는 금융 지식그래프에서 Cypher 쿼리를 생성하는 AI야.

[그래프 구조]
- (:Company {{name}})
- (:Report {{title, publication_date, target_price, rating}})
- (:Forecast {{value, unit, period, yoy_growth, qoq_growth, type}}) period 예시: 1Q24, 3Q24, 1Q25
- (:Metric {{name}})
- (:Analyst {{name}})
- (:Broker {{name}})

[관계 구조]
- (:Analyst)-[:WRITES]->(:Report)
- (:Report)-[:ISSUED_BY]->(:Broker)
- (:Report)-[:TARGETS]->(:Company)
- (:Report)-[:FORECASTS]->(:Forecast) 
- (:Company)-[:HAS_FORECAST]->(:Forecast)
- (:Forecast)-[:OF_METRIC]->(:Metric)

[사용자 질문]
{user_question}

아래와 같은 형식으로 Cypher 쿼리만 출력해:

MATCH ...
WHERE ...
RETURN ...
"""

# Gemini에게 Cypher 쿼리 생성 요청
response = gemini.generate_content(cypher_prompt)
raw_response = response.text.strip()

# 코드 블록 제거
if raw_response.startswith("```"):
    cypher_query = "\n".join(
        line for line in raw_response.splitlines()
        if not line.strip().startswith("```")
    ).strip()
else:
    cypher_query = raw_response

print("정제한 Cypher 쿼리:\n", cypher_query)

# Neo4j 연결 설정
uri = "neo4j+s://91dca365.databases.neo4j.io"
user = "neo4j"
password = "LDm1TfiVmKU1fzX0PUZkBUOF8PM6siBYogmWbsjzUmc"
driver = GraphDatabase.driver(uri, auth=(user, password))

# Cypher 쿼리 실행 및 결과 출력
def run_cypher(query):
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

result = run_cypher(cypher_query)
print("질의 결과:\n", result)


print(user_question)

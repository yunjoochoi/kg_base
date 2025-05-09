import fitz  
import google.generativeai as genai
import json

# Gemini API 설정
genai.configure(api_key="키")
gemini = genai.GenerativeModel("models/gemini-1.5-pro")

# 프롬프트 템플릿 정의
prompt_template = """
다음 텍스트에서 아래 금융 항목들을 스키마에 맞는 JSON 형식으로 추출하세요.
추출된 지표는 '리포트 내 예측값'으로 간주하고, 각 지표는 별도로 명세합니다.

[추출 항목]
- 기업명
- 증권사
- 애널리스트
- 리포트 제목
- 리포트 발행일
- 투자의견
- 목표주가
- 지표들:
  - 지표명 (예: 매출액, 부채비율, PER, EBITDA, ROE 등)
  - 값
  - 단위
  - 기준 기간 (예: 2025F, 1Q24 등)
  - 증감률 (yoy, qoq 중 있는 경우)
  - 이 값이 예측치인지 실제 값인지 (예: "forecast" or "actual")

[텍스트]
{page_text}

[출력 JSON 예시]
{{
  "company": "SK hynix",
  "broker": "NH투자증권",
  "analyst": "홍길동",
  "report_title": "2025 반도체 전망",
  "publication_date": "2024-04-01",
  "target_price": 160000,
  "rating": "Buy",
  "metrics": [
    {{
      "name": "EBITDA",
      "value": 13.5,
      "unit": "조원",
      "period": "2025F",
      "yoy_growth": "14.2%",
      "qoq_growth": null,
      "type": "forecast"
    }},
    {{
      "name": "영업이익",
      "value": 3.2,
      "unit": "조원",
      "period": "2024Q4",
      "yoy_growth": null,
      "qoq_growth": "-5%",
      "type": "actual"
    }}
  ]
}}
"""


# PDF 열기
pdf_path = "/home/yunju/text_project/simple_naver_reports/크래프톤_25.04.30_SK증권.pdf"
doc = fitz.open(pdf_path)

# 페이지 단위로 추출 및 Gemini 추론
all_results = []
from time import sleep
for page_number in range(len(doc)):
    page = doc.load_page(page_number)
    page_text = page.get_text().strip()
    
    if len(page_text) < 100:  # 내용 없는 페이지 스킵
        continue
    
    full_prompt = prompt_template.format(page_text=page_text)
    response = gemini.generate_content(full_prompt)
    sleep(20)
    try:
        if "```json" in response.text:
            json_text = response.text.split("```json")[1].split("```")[0]
        else:
            json_text = response.text
        
        data = json.loads(json_text)
        data["page"] = page_number + 1  # 페이지 번호도 기록
        all_results.append(data)
    
    except json.JSONDecodeError:
        print(f"JSON 파싱 실패: 페이지 {page_number+1}")
        print(response.text[:300])

# 결과 확인
print(all_results)
# for item in all_results:
#     print(f"페이지 {item['page']} → 기업: {item.get('company')}, 지표: {[m['name'] for m in item.get('metrics', [])]}")

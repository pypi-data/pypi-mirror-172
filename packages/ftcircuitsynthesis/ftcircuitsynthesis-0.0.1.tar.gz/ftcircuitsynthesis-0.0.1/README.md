# Fault-Tolerant Quantum Circuit Synthesis for Universal Fault-Tolerant Quantum Computing 
```
`* Project Title 란에 프로젝트 명 입력 
* 프로젝트에 대한 간단한 설명 작성 
```
- This project develops a quantum circuit synthesis algorithm for univeral fault-tolerant quantum computing based on concatenated codes
- The circuits of fault-tolerant quantum protocol should be executable in terms of locality constraint that a quantum chip has, but with retaining both the fault tolerance and the logic sequence of the protocol

## Table of Contents
- [Environment & Prerequisites]()(#environment-and-prerequisites)
- [Installation]()(#installation)
- [Usage]()(#usage)
- [Authors]()(#authors)

## Environment and Prerequisites
```
`* 개발 언어 및 실행환경 정보 작성 (예, OS, 컴파일러, Hardware 등)
* 소스코드를 실행하기 전에 설치해야 할 package나 의존성이 걸리는 문제들 기술 
```
- 개발언어:  Python 3
- OS:  Ubuntu 20.04

## Installation
```
`* 소스코드 설치 방법을 단계별 예제와 함께 설명 
* 만약 상기 파트에서 설명해야 할 내용이 많다면 별도의 파일(예, md, html 등) 작성 후, 링크로 삽입 추천 
```


```bash
`git clone https://gist.github.com/PurpleBooth/109311bb0361f32d87a2
```
- python 패키지로 별도의 빌드는 필요 없음

```bash
`cd code-package
make or pip install \<package-name\> 
```

1. numpy, simplejson(json 타입 데이터 처리 패키지)
	- "pip install numpy, simplejson"
	

## Usage

```
`* 소스코드 실행 및 사용 방법 설명 (Usage Example 포함)
```
### 패지키 임포트
import dijkstra\_qcmapper.dijkstra\_qcmapper as qcmapper

### 사용 API
- qcmapper 패키지의 synthesize 함수를 호출하는 것으로 회로 합성 수행 함
- 형식:
	“qcmapper.synthesize(qasm\_code=QASM경로, arguments=회로합성 옵션)"

- arguments:
	1. QASM 경로 : 회로 합성 대상 QASM (Quantum Assembly) 파일 (확장명 : .qasmf) 경로 
	2. 회로 합성 옵션 : 사전형 데이터 (양자칩 정보, 초기 큐빗 배치 방식 등)
		- 예시 : option = {“option": {"allow\_swap": True,
			“goal”: “system\_code",
			“iteration”: 10,
			“qubit\_connectivity": "user",
			“initial\_mapping\_option": "random"},
			“path\_job”: 결과물 저장할 경로,
			“qchip” : 양자칩 파일 경로}
							  
		- 옵션 항목 : 
			1) allow\_swap: 회로에 SWAP 을 포함할지 여부 (default: True)
			2) goal : 시스템 코드 생성 (default)
			3) iteration : 회로 합성 반복 횟수 (많은 수록 결과 회로가 compact 해짐)
			4) qubit\_connectivity: 양자칩 상 큐빗 연결성 (default : user, user 선택시 반드시 아래 양자칩 파일 경로 추가해야 함)
			5) path\_job: 결과물 저장할 경로 지정
			6) qchip : 양자칩 파일 (json 파일) 경로
			- 양자칩 파일 예시 : 
				{“device\_name”: 양자칩 이름,
				“dimension” : 양자칩 사이즈 정보,
				“qubit\_connectivity":  {
				“0”: 큐빗 0 과 연결된 큐빗 리스트,
				“1”: 큐빗 1 과 연결된 큐빗 리스트,
				..
				“n” : 큐빗 n 과 연결된 큐빗 리트스}
				}
	3. 출력 결과 : 사전형 데이터 (양자회로 시스템 코드, 회로 정적 분석 결과, 입력 양자칩 구조 등)
		- 시스템 코드 : 사전형 데이터 (초기 큐빗 배치도, 최종 큐빗 배치도, 회로)
		- 정적 분석 결과 (회로 깊이, 양자 게이트 수, 큐빗 수 등)

- Note : tests 디렉토리 내부에 사용 예제 (demo.py) 및 예제 QASM 과 양자칩 정보 포함되어 있음

## Authors
```
`* 개발에 참여한 개발자 정보 작성 
* 개발자 정보 표기방법:  \<성명\>  \<이메일 주소\>   
```
- 황용수 (양자기술연구단/양자컴퓨팅연구실) yhwang@etri.re.kr

## Version (optional)
```
`* 현재 버전 정보 입력 (예) major.minor.patch (1.0.0) / release date (2021.10.30) 
* 이전 버전 정보 및 관련 url 정보 
```
- 현재버전 : 0.1.12
- 배포일자 : 2022.07.22

## Thanks (optional)
```
`* 프로젝트 개발에 도움을 준 사람 또는 타 프로젝트 정보 입력  
```


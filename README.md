# mitosiscounter

늦었지만... 현재 상태 보고 겸 올립니다. db를 sqlite로 모아서 쓰는 안을 고민했고, sqlalchemy라는 ORM을 이용해서 sliderunner.sqlite와 midog++.sqlite를 묶어서 받는 것을 짰습니다. sqlalchemy를 쓰면 각 db 안의 table들의 colum row를 파이썬 variable처럼 다룰 수가 있어서, 마지막에 저희들만의 가중치를 가진 db를 생성하는 데에 도움을 줄 수 있을 것 같습니다. 
sliderunner.sqlite에서 class(true mitosis, false mitosis, maybe mitosis)와 위치만 따와서 따로 테이블을 만들었고 Midog++도 파일구조를 봐야겠지만 비슷하게 만드려고 합니다. 이후 이걸 합쳐놓은 데이터셋으로 AI를 학습시키고 pytorch로 저장해두려고 합니다. 
---아래는 아직 구축중, 클라우드 코드만 가지고 있음---
백엔드 측에서는 로그인을 하고, 인풋으로 xy cordinates와 40hpf에서 직접 위치 찾는 것을 받아서 ai로 넘기고, 그 결과값을 제시하는 방법으로 짜보려고 했습니다. sliderunner.py의 imagereceiver thread 방식을 차용해보고자 합니다

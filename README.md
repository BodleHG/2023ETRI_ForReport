# 2023ETRI For Report

## 프로젝트 구조
```
📦2023ETRI_ForReport
 ┣ 📂example
 ┃ ┣ 📜result.example.csharp
 ┃ ┗ 📜result_example.json
 ┣ 📂PyrexiaDsim
 ┃ ┣ 📂Agent
 ┃ ┃ ┣ 📂instance
 ┃ ┃ ┃ ┗ 📜config.py
 ┃ ┃ ┣ 📜Agentsim.py
 ┃ ┃ ┣ 📜agentsim_manager.py
 ┃ ┃ ┣ 📜dockerfile
 ┃ ┃ ┣ 📜human_agent.py
 ┃ ┃ ┣ 📜requirements.txt
 ┃ ┃ ┣ 📜rest_api.py
 ┃ ┃ ┗ 📜worker_model.py
 ┃ ┣ 📂Generator
 ┃ ┃ ┣ 📜config.py
 ┃ ┃ ┣ 📜config_for_local.py
 ┃ ┃ ┣ 📜container_generator.py
 ┃ ┃ ┣ 📜container_generator_for_local_test.py
 ┃ ┃ ┣ 📜dockerfile
 ┃ ┃ ┗ 📜requirements.txt
 ┃ ┣ 📂instance
 ┃ ┃ ┗ 📜config.json
 ┃ ┣ 📜config.py
 ┃ ┣ 📜container_generator_model.py
 ┃ ┣ 📜monitor_model.py
 ┃ ┣ 📜PyrexiaDsim.py
 ┃ ┣ 📜pyrexiaDsim_manager.py
 ┃ ┗ 📜rest_api.py
 ┣ 📂Pyrexiasim_Cam
 ┃ ┣ 📂data
 ┃ ┃ ┣ 📜person1.png
 ┃ ┃ ┗ 📜person2.png
 ┃ ┣ 📜ai_simulator.py
 ┃ ┗ 📜config.py
 ┣ 📂Pyrexiasim_Monitoring
 ┃ ┣ 📂instance
 ┃ ┃ ┗ 📜config.py
 ┃ ┣ 📜config.py
 ┃ ┣ 📜pyrexiasim.py
 ┃ ┣ 📜pyrexiasim_manager.py
 ┃ ┣ 📜telegram_manager.py
 ┃ ┣ 📜worker.py
 ┃ ┣ 📜worker_data_sender.py
 ┃ ┣ 📜worker_flush.py
 ┃ ┣ 📜worker_monitor.py
 ┃ ┗ 📜worker_remove.py
 ┣ 📜.gitignore
 ┣ 📜README.md
 ┗ 📜requirements.txt
```

## Pyrexiasim_Cam
- 각 Site를 관제하는 IP Cam에서 QR코드가 감지되었을 때 트리거링하는 모니터링 코드
  - OPENCV, PYZBAR 라이브러리를 사용하여 QR 코드 감지 및 디코딩
  - QR코드에는 Human Info(JSON)이 들어있음
  - Human Info 데이터의 Human_ID에 해당하는 작업자 트리거
    - Human Info를 저장하는 MongoDB - Collection에서 Human_ID에 해당하는 작업자 Document의 필드를 업데이트하여 트리거링하는 방식(human_exist)

## Pyrexiasim_Monitoring
- 데이터베이스를 주기적으로 모니터링하며, 트리거링 됐을 시(데이터베이스 필드 업데이트) 그에 해당하는 작업자 모델을 생성하고 체력을 연산, 임계값을 벗어났을 때(체력 부족, 체력 과다) 텔레그램을 통해 사용자에게 알림을 주는 코드
  - Pyevsim, Telegram 모듈 사용

## PyrexiaDsim
- 데이터베이스를 주기적으로 모니터링하며, Human의 체력이 임계값 아래로 떨어졌거나 가시화 도구에서 시뮬레이션 트리거링용 필드(simulation_activate)가 업데이트 됐을 시, 남은 작업시간을 30분마다의 state로 구분하여 시뮬레이션하는 코드
  - 모니터링 모델에서 데이터베이스가 트리거를 확인할 시, 트리거링 된 Human의 Container Generator Model 생성, 엔진에 insert
  - Container Generator Model 생성 시 현재 작업자의 상태를 snapshot하여 전달
  - Container Generator Model에서 사용자가 지정한 Simulation Instance 수만큼 작업자의 체력을 시뮬레이션을 수행하는 Docker Container 생성
  - 각 컨테이너에서 Ramdom으로 시나리오 생성, state만큼 반복하며 체력 연산을 수행함. 각 state별로 리스트로 저장하며, 시뮬레이션이 종료될 시 각 Container에서 DB에 Insert 및 Container 종료

## Example
- DB에 저장되어 있는 Database Document 구조 및 시뮬레이션 로그 예시
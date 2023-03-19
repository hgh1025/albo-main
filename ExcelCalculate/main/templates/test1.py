from collections import deque
n,m = map(int, input().split())

map = [list(map(int, input())) for _ in range(n)]

#bfs
cnt = 0


dx = [-1,1,0,0]
dy = [0,0,-1,1]
def bfs(x,y):
  q = deque()
  q.append((x,y)) # 노드 삽입

  while q:
    x,y = q.popleft() # 한번 방문한 노드 삭제
    for i in range(4):
      nx = x + dx[i]
      ny = y + dy[i]

      if nx <0 or ny <0 or nx >=n or ny >=m:
        return False

      if map[nx][ny] == 0: #위치의 숫자가 0이면 이동 불가
        return False

      if map[nx][ny] == 1:
        map[nx][ny] = map[nx][ny] +1 #위치의 숫자가 1이면 한칸이동
        q.append((nx,ny))
        return True
  

for i in range(n):
  for j in range(m):
    if bfs(i,j) == True:
      cnt += 1
      
print(cnt)
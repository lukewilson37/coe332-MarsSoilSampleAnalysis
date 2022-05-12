build:
	docker build -t alecsuggs/mssaapp:1.0.0 .

run:
	RIP=$$(docker inspect mssaredis | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name "MSSAapp" --env REDIS_IP=$${RIP} -p 5033:5000 alecsuggs/mssaapp:1.0.0 /app/app.py

stop:
	docker stop "MSSAapp"

image:
	docker images | grep alecsuggs

remove:
	docker rm "MSSAapp"

pull:
	docker pull alecsuggs/mssaapp:1.0.0

removei:
	docker rmi alecsuggs/mssaapp:1.0.0

redis:
	docker run -d -p 6433:6379 -v $(pwd)/data:/data:rw --name=mssaredis redis:6 --save 1 1

bwrk:
	docker build -t alecsuggs/mssawrk:1.0.0 .

rwrk:
	RIP=$$(docker inspect mssaredis | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run  --name "mssaworker" --env REDIS_IP=$${RIP} alecsuggs/mssawrk:1.0.0 /app/worker.py 

rmwrk:
	docker rm "mssaworker"

stopw:
	docker stop mssaworker

redo:
	make remove
	make stopw
	make rmwrk
	make build
	make bwrk
	make run
	make rwrk

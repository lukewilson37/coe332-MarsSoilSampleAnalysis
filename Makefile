build:
	docker build -t alecsuggs/mssaapp:1.0.0 .

run:
	docker run --name "MSSAapp" -p 5033:5000 alecsuggs/mssaapp:1.0.0 /app/app.py

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
	docker run -p 6433:6379 --name=mssaredis redis:6 

bwrk:
	docker build -t alecsuggs/mssawrk:1.0.0 .

rwrk:
	docker run  --name "mssaworker" alecsuggs/mssawrk:1.0.0 /app/worker.py 

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

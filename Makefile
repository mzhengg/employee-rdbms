# executes all commands necessary to launch the RDBMS
execute:
	docker login

	docker tag eRDBMS:latest mikaelzheng/eRDBMS:latest

	docker push mikaelzheng/eRDBMS:latest

	kubectl create deployment eRDBMS --image=mikaelzheng/eRDBMS:latest

# destroys the RDBMS
unexecute:
	kubectl delete deployment eRDBMS

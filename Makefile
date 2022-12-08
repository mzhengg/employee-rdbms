# execute all commands necessary to launch the RDBMS
execute:
# build images and run containers
	docker compose up -d

# access the interface
	docker exec -it interface bash

# destroy the RDBMS
unexecute:
# stop containers and delete images
	docker compose down --volumes --rmi all
## deployment

---

[WIP]

---

### deploy on chainmaker

1. compile memosolo.sol in {project dir}/contracts 
- use docker solc provided by Chainmaker official

    `docker pull chainmakerofficial/chainmaker-solidity-contract:2.0.0`

    go to {project dir}/contracts and run

    `docker run -it --name chainmaker-solidity-contract -v ${pwd}:/home chainmakerofficial/chainmaker-solidity-contract:2.0.0 bash`

    inside container, go to /home, and run

    `mkdir build`

    `solc --abi --bin  -o ./build memosolo.sol`

2. create a Chainmaker chain
3. get the chain **crypto-config** folder with CAs and org certs and user certs, place(copy) it to {project dir}/secrets
4. create a conn.txt in {project dir}/secrets/conn-config, it contains the chain node ip and host like`127.0.0.1:8888`



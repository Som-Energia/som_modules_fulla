# Com funciona

## Coses que farem al servidor

### Construim la imatge del erp
`docker build -t erpserver --build-arg GITHUB_TOKEN=el_nostre_token_per_accedir_a_repos_privats .`

### Construim la base de dades amb el destral
`docker-compose -f docker-compose-fulla-feta.yaml up`

### Guardem contenidor de Postgres a imatge
`docker container commit -a "SomEnergia" -m "Postgres som_modul_fulla" id_contenidor postgres:developer`

### Pugem les imatges al Harbour
TODO

## Com el fem servir en local
TODO: docker-compose que agafar imatges de Harbour


# **Práctica 2** Subsistema de Notificaciones
## Grupo 13: Javier Ye Zhang y Pablo Torija Martínez

### Parte 1: docker-compose
Requisitos previos:
- Tener Docker y Docker Compose instalados.

1. Iniciar Docker

2. Ir al directorio que contiene el docker-compose.yaml:
  `\Practica-AOS`

3. Ejecutar:
  ```
  $ docker-compose build
  $ docker-compose up
  ```

4. Abrir: `http://localhost:x/` en un navegador, sustituyendo `x` por el puerto correspondiente mostrado en el `docker-compose.yaml` (del 8001 al 8007).
    
### Parte 2: Kubernetes
Requisitos previos:
- Tener kubectl instalado.

1. Ir al directorio que contiene los manifiestos
  `\kubernetes`

2. Ejecutar:
  ```
  $ kubectl apply -f .
  ```

3. Esperar a que se creen los pods. Para comprobar el estado de los pods, ejecutar:
  ```
  $ kubectl get pods
  ```

4. Comprobar la IP externa en la que están disponibles los servicios, ejecutando:
  ```
  $ kubectl get services
  ```
La IP externa suele ser `localhost`.

5. Abrir: `http://localhost:x/` (o la IP que sea) en un navegador, sustituyendo `x` por el puerto correspondiente mostrado en cada manifiesto (del 8001 al 8007).

### Resolución de problemas
#### Kubernetes - la IP externa muestra el estado `<pending>`
Debido a que para la implementacion de kubernetes se han usado LoadBalancers, es necesario que estén libres los puertos 8001 al 8007 y 4011 al 4017. Para asegurarse de esto:
1. Ejecutar:
  ```
  $ netstat -aon
  ```
2. Encontrar el PID del proceso que ocupa estos puertos y ejecutar:
  ```
  $ taskkill /pid <pid> /F
  ```
Esto reiniciará Docker. Tras unos segundos, los servicios deberían ser accesibles.
# Grupo 13 - PRII3 - Sprint 1

## 0. Requisitos

Ubuntu 22.04 con ROS2 Humble. Si falta algo, instalar en una terminal:

```bash
sudo apt install git ros-humble-turtlesim python3-colcon-common-extensions
```

## 1. Descargar el código

Abrir una terminal y ejecutar:

```bash
cd ~
git clone https://github.com/JordiMartinez06/g13_prii3_ws.git
cd g13_prii3_ws
```

## 2. Compilar

Estando dentro de la carpeta `g13_prii3_ws`:

```bash
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

## 3. Ejecutar

En la misma terminal:

```bash
ros2 launch g13_prii3_turtlesim draw.launch.py
```

## 4. Detener, reanudar o reiniciar el dibujo

Abrir **otra terminal** (con el launch todavía en marcha) y ejecutar:

```bash
source /opt/ros/humble/setup.bash
source ~/g13_prii3_ws/install/setup.bash
```

Después, el servicio que se quiera probar:

```bash
ros2 service call /stop std_srvs/srv/Trigger
ros2 service call /resume std_srvs/srv/Trigger
ros2 service call /restart std_srvs/srv/Trigger
```

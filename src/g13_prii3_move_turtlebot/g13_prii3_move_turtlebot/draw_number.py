import time
import rclpy
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger

rclpy.init()
nodo = rclpy.create_node('draw_number')
pub = nodo.create_publisher(Twist, '/cmd_vel', 10)

pausado = False
reiniciar = False

def servicio_stop(peticion, respuesta):
    global pausado
    pausado = True
    respuesta.success = True
    return respuesta

def servicio_resume(peticion, respuesta):
    global pausado
    pausado = False
    respuesta.success = True
    return respuesta

def servicio_restart(peticion, respuesta):
    global pausado, reiniciar
    pausado = False
    reiniciar = True
    respuesta.success = True
    return respuesta

nodo.create_service(Trigger, 'stop', servicio_stop)
nodo.create_service(Trigger, 'resume', servicio_resume)
nodo.create_service(Trigger, 'restart', servicio_restart)


def mover(velocidad, giro, segundos):
    msg = Twist()
    msg.linear.x = velocidad
    msg.angular.z = giro

    tiempo = 0.0
    while tiempo < segundos:
        if reiniciar:
            return
        rclpy.spin_once(nodo, timeout_sec=0)
        if pausado:
            pub.publish(Twist())
        else:
            pub.publish(msg)
            tiempo = tiempo + 0.1
        time.sleep(0.1)

    pub.publish(Twist())

def avanzar(metros):
    mover(0.1, 0.0, metros / 0.1)

def girar_derecha():
    mover(0.0, -0.5, 3.14)

def media_vuelta():
    mover(0.0, -0.5, 6.28)



def dibujar_13():
    avanzar(1.0)
    girar_derecha()
    avanzar(0.3)
    avanzar(0.5)
    girar_derecha()
    avanzar(0.5)
    girar_derecha()
    avanzar(0.5)
    media_vuelta()
    avanzar(0.5)
    girar_derecha()
    avanzar(0.5)
    girar_derecha()
    avanzar(0.5)


def main():
    global reiniciar

    print('Esperando al robot...')
    while pub.get_subscription_count() == 0:
        time.sleep(0.5)

    while True:
        reiniciar = False
        print('Dibujando el 13')
        dibujar_13()
        if not reiniciar:
            print('¡Terminado! (llama a restart para repetir)')
            while not reiniciar:
                rclpy.spin_once(nodo, timeout_sec=0.1)
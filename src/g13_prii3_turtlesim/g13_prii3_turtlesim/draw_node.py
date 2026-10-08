import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, Empty
from turtlesim.srv import TeleportAbsolute, SetPen

P = math.pi / 2


def F(d):                      
    return ('mov', 1.0, 0.0, d)


def ir(x, y, th):
    return [('pen', False), ('tp', x, y, th), ('pen', True)]


PASOS = (
    ir(3, 7, -P) + [F(4)]
    + ir(5, 7, 0) + [F(2)]
    + ir(7, 7, -P) + [F(2)]
    + ir(7, 5, 2*P) + [F(1)]
    + ir(7, 5, -P) + [F(2)]
    + ir(7, 3, 2*P) + [F(2)]   
)


class Dibujo(Node):
    def __init__(self):
        super().__init__('dibujo')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.tp = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        self.pen = self.create_client(SetPen, '/turtle1/set_pen')
        self.reset = self.create_client(Empty, '/reset')
        self.create_service(Trigger, 'stop', self.stop)
        self.create_service(Trigger, 'resume', self.resume)
        self.create_service(Trigger, 'restart', self.restart)
        self.i = 0
        self.n = 0
        self.run = True
        self.create_timer(0.05, self.tick)

    def tick(self):
        if not (self.tp.service_is_ready() and self.pen.service_is_ready()):
            return
        if not self.run or self.i >= len(PASOS):
            return
        paso = PASOS[self.i]
        if paso[0] == 'pen':
            r = SetPen.Request()
            r.r, r.g, r.b, r.width = 255, 255, 255, 3
            r.off = 0 if paso[1] else 1
            self.pen.call_async(r)
            self.i += 1
        elif paso[0] == 'tp':
            r = TeleportAbsolute.Request()
            r.x, r.y, r.theta = float(paso[1]), float(paso[2]), float(paso[3])
            self.tp.call_async(r)
            self.i += 1
        else:
            msg = Twist()
            msg.linear.x = paso[1]
            msg.angular.z = paso[2]
            self.pub.publish(msg)
            self.n += 1
            if self.n >= round(paso[3] * 20):
                self.n = 0
                self.i += 1
                self.pub.publish(Twist())

    def stop(self, req, res):
        self.run = False
        self.pub.publish(Twist())
        res.success = True
        return res

    def resume(self, req, res):
        self.run = True
        res.success = True
        return res

    def restart(self, req, res):
        self.pub.publish(Twist())
        self.reset.call_async(Empty.Request())
        self.i = 0
        self.n = 0
        self.run = True
        res.success = True
        return res


def main():
    rclpy.init()
    rclpy.spin(Dibujo())


if __name__ == '__main__':
    main()

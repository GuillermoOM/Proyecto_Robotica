import sys, serial, time, os, sys
from math import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Calculo(QThread):
    def __init__(self, trayectoria = "infinito", x = 0, y = 0, z = 0):
        QThread.__init__(self)
        self.trayectoria = trayectoria
        self.x = x
        self.y = y
        self.z = z

    def __del__(self):
        self.wait()

    def send(self):
        lim_inf = sqrt(pow(5.5, 2) + pow(7.5, 2))
        lim_sup = 13
        magnitude = sqrt(pow(self.x,2) + pow(self.y,2) + pow(self.z,2))
        if lim_inf < magnitude and magnitude < lim_sup:
            angulos = QStringList()
            a = 0
            b = 0
            c = 0
            L1 = 0
            L2 = 5.5
            L3 = 7.5
            a = atan2(self.y, self.x)
            b = atan2(self.z - L1, sqrt(pow(self.x,2) + pow(self.y,2))) + acos((pow(self.x, 2) + pow(self.y, 2) + pow(L2, 2) - pow(L3, 2)) /(2 * L2 * sqrt(pow(self.x,2) + pow(self.y,2))))
            c = acos((pow(L2, 2) + pow(L3, 2) - pow(self.x, 2) - pow(self.y, 2) - pow(self.z - L1, 2))/(2*L3*L2)) - radians(90)
            angulos.clear()
            angulos.append("{}".format(a))
            angulos.append("{}".format(b))
            angulos.append("{}".format(c))
            time.sleep(0.1)
            self.emit(SIGNAL("update_m(QStringList)"), angulos)
        else:
            print "ERROR: fuera de limites!"
            time.sleep(1)

    def run(self): #Obtener angulos y mandarlos a principal
        step = 0.05
        if self.trayectoria == "manual":
            while True:
                self.send()

        if self.trayectoria == "infinito":
            print "infinito"
            i = 0
            while True:
                if i < 2*3.1416:
                    self.x = 4.5*cos(i)/(1+pow(sin(i), 2))
                    self.y = 9
                    self.z = 4 + 5*cos(i)*sin(i)/(1+pow(sin(i), 2))
                    print "{} {} {}".format(self.x, self.y, self.z)
                    self.send()
                    i += step
                else:
                    i = 0

        if self.trayectoria == "espiral":
            print "espiral"
            i = 0
            r = 0.5
            while True:
                if i < 2*3.1416:
                    self.x = 1*exp(0.15*i)*cos(i)
                    self.y = 9
                    self.z = 5 + 1*exp(0.15*i)*sin(i)
                    print "{} {} {}".format(self.x, self.y, self.z)
                    self.send()
                    i += step
                else:
                    i = 0

class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.bloques = []
        self.tarea = Calculo()
        
        ############LAYOUT###############
        self.setWindowTitle("PyQt Dialog demo")
        self.setFixedSize(550, 200)
        # BOTON INICIAR
        self.biniciar = QPushButton("Iniciar", self)
        self.biniciar.move(280, 165)
        self.biniciar.pressed.connect(self.iniciar)
        self.biniciar.setEnabled(False)

        # BOTON DETENER
        self.bdetener = QPushButton("Detener", self)
        self.bdetener.move(430, 165)
        self.bdetener.pressed.connect(self.detener)
        self.bdetener.setEnabled(False)

        # TRAYECTORIA:
        self.LTrayectoria = QLabel("Trayectoria", self)
        self.LTrayectoria.move(10, 20)

        ## INFINITO
        self.TCar = QRadioButton("Infinito", self)
        self.TCar.move(10, 40)
        self.TCar.setChecked(True)

        ## ESPIRAL
        self.TFlor = QRadioButton("Espiral", self)
        self.TFlor.move(10, 70)

        ## MANUAL
        self.TMan = QRadioButton("Manual:", self)
        self.TMan.toggled.connect(self.modoTrayectoria)
        self.TMan.move(10, 100)
        ### X
        self.DX = QLabel("X:", self)
        self.DX.move(10, 130)
        self.TX = QLineEdit("", self)
        self.TX.move(25, 130)
        self.TX.setFixedSize(40, 20)
        self.TX.setEnabled(False)
        ### Y
        self.DY = QLabel("Y:", self)
        self.DY.move(80, 130)
        self.TY = QLineEdit("", self)
        self.TY.move(95, 130)
        self.TY.setFixedSize(40, 20)
        self.TY.setEnabled(False)
        ### Z
        self.DZ = QLabel("Z:", self)
        self.DZ.move(150, 130)
        self.TZ = QLineEdit("", self)
        self.TZ.move(165, 130)
        self.TZ.setFixedSize(40, 20)
        self.TZ.setEnabled(False)

        # MATRIZ
        self.LMatriz = QLabel("Matriz", self)
        self.LMatriz.move(250, 20)
        for y in range(4):
            bloquesy = []
            for x in range(4):
                bloquesy.append(QLineEdit("", self))
                bloquesy[x].setFixedSize(60, 20)
                bloquesy[x].move(250 + 70 * x, 40 + 30 * y)
                bloquesy[x].setReadOnly(True)
                bloquesy[x].setText("0")
            self.bloques.append(bloquesy)
        
        ## POSICIONES ACTUALES
        PX = QLabel("X", self)
        PX.move(530, 45)
        PY = QLabel("Y", self)
        PY.move(530, 75)
        PZ = QLabel("Z", self)
        PZ.move(530, 105)

        # CONEXION
        self.ard = serial.Serial()
        self.ard.baudrate = 9600
        self.Lestado = QLabel("Serial:", self)
        self.Lestado.move(10, 170)
        self.puerto = QLineEdit("COM4", self)
        self.puerto.move(45, 166)
        self.puerto.setFixedSize(50,20)
        self.Bconectar = QPushButton("Conectar", self)
        self.Bconectar.move(100, 165)
        self.Bconectar.pressed.connect(self.conectar)
    
    ############EVENTOS###############

    def modoTrayectoria(self):
        if self.TMan.isChecked():
            self.TX.setEnabled(True)
            self.TY.setEnabled(True)
            self.TZ.setEnabled(True)
        else:
            self.TX.setEnabled(False)
            self.TY.setEnabled(False)
            self.TZ.setEnabled(False)

    def iniciar(self):
        correcto = True
        if not self.tarea.isRunning() and self.ard.is_open:
            print "Ejecutando trayectoria..."
            if self.TMan.isChecked():
                self.tarea = Calculo(trayectoria = "manual", x = float(self.TX.text()), y = float(self.TY.text()), z = float(self.TZ.text()))
            elif self.TCar.isChecked():
                self.tarea = Calculo(trayectoria = "infinito")
            elif self.TFlor.isChecked():
                self.tarea = Calculo(trayectoria = "espiral")
            self.connect(self.tarea, SIGNAL("update_m(QStringList)"), self.update_matrix)
            self.biniciar.setEnabled(False)
            self.bdetener.setEnabled(True)
            self.Bconectar.setEnabled(False)
            self.tarea.start()
    
    def detener(self):
        if self.tarea.isRunning():
            print "Parando Robot..."
            try:
                self.ard.write("0,105,0,180\n")
                self.ard.flush()
                if (self.ard.in_waiting):
                    print "in: " + self.ard.read(self.ard.in_waiting)
            except:
                pass
            self.biniciar.setEnabled(True)
            self.bdetener.setEnabled(False)
            self.Bconectar.setEnabled(True)
            self.tarea.terminate()

    def update_matrix(self, angulos): #recibir angulos del thread, completar matriz y mandar senial al robot
        a = float(angulos[0])
        b = float(angulos[1])
        c = float(angulos[2])
        for x in range(4): #bloques[Fila][Columna]
            self.bloques[3][x].setText("0")
        self.bloques[0][0].setText("{:.3f}".format(sin(b + c)*cos(a)))
        self.bloques[0][1].setText("{:.3f}".format(-sin(a)))
        self.bloques[0][2].setText("{:.3f}".format(cos(b + c)*cos(a)))
        self.bloques[0][3].setText("{:.3f}".format((cos(a)*(15*sin(b + c) + 11*cos(b)))/2))
        self.bloques[1][0].setText("{:.3f}".format(sin(b + c)*sin(a)))
        self.bloques[1][1].setText("{:.3f}".format(cos(a)))
        self.bloques[1][2].setText("{:.3f}".format(cos(b + c)*sin(a)))
        self.bloques[1][3].setText("{:.3f}".format((sin(a)*(15*sin(b + c) + 11*cos(b)))/2))
        self.bloques[2][0].setText("{:.3f}".format(-cos(b + c)))
        self.bloques[2][1].setText("{:.3f}".format(0))
        self.bloques[2][2].setText("{:.3f}".format(sin(b + c)))
        self.bloques[2][3].setText("{:.3f}".format((11*sin(b))/2 - (15*cos(b + c))/2))
        self.bloques[3][3].setText("1")

        try:
            self.ard.write("{:.0f},{:.0f},{:.0f},{:.0f}\n".format(degrees(a), degrees(b), degrees(c), 155))
            print "out: " + "{:.0f},{:.0f},{:.0f},{:.0f}".format(degrees(a), degrees(b), degrees(c), 155)
            self.ard.flush()
            if (self.ard.in_waiting):
                print "in: " + self.ard.read(self.ard.in_waiting)
        except serial.SerialException:
            print "Desconectado!"
            self.detener()
            self.Bconectar.setText("Conectar")
            self.biniciar.setEnabled(False)

    def conectar(self):
        if not self.ard.is_open:
            try:
                self.ard.port = "{}".format(self.puerto.text())
                self.ard.open()
                self.Bconectar.setText("Desconectar")
                self.biniciar.setEnabled(True)
            except serial.SerialException:
                print "Dispositivo no encontrado"

        else:
            self.ard.close()
            self.Bconectar.setText("Conectar")
            self.biniciar.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()

# Matriz Homogenea
# L1 = 0 cm
# L2 = 5.5 cm
# L3 = 7.5 cm
#
# [ sin(b + c)*cos(a), -sin(a), cos(b + c)*cos(a), (cos(a)*(15*sin(b + c) + 11*cos(b)))/2]
# [ sin(b + c)*sin(a),  cos(a), cos(b + c)*sin(a), (sin(a)*(15*sin(b + c) + 11*cos(b)))/2]
# [       -cos(b + c),       0,        sin(b + c),      (11*sin(b))/2 - (15*cos(b + c))/2]
# [                 0,       0,                 0,                                      1]
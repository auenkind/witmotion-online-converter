import csv, io, struct
import numpy as np

class WitMotionConverter:
    def toCsv(self, data):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["l", "t", "x", "y", "z"])
        writer.writerows(data)
        return output.getvalue()
    
    def get_accelectaions(self, data):
        marker = b'U' + b'Q'
        t = 0
        timeStep = 0.05
        msgs_num = 0
        res = []
        parts = data.split(marker)
        for part in parts:
            p = b'Q'+part
            q = self.get_acceleration(p)
            if q is not None:
                d = [msgs_num, t, q[0], q[1], q[2]]
                res.append(d)
                msgs_num += 1
            t += timeStep
        return res
    
    def get_acceleration(self, data):
        if len(data) < 7:
            return None
        cmd = struct.unpack('c', data[0:1])[0]
        if cmd == b'Q': # 0x54
            return np.array(struct.unpack('<hhh', data[1:7]))/32768.0*16.0
        return None

    def get_gyro(self, data):
        if len(data) < 7:
            return None
        cmd = struct.unpack('c', data[0:1])[0]
        if cmd == b'R': # 0x54
            return np.array(struct.unpack('<hhh', data[1:7]))/32768.0*2000.0
        return None

    def get_magnetic(self, data):
        if len(data) < 7:
            return None
        cmd = struct.unpack('c', data[0:1])[0]
        if cmd == b'T': # 0x54
            return np.array(struct.unpack('<hhh', data[1:7]))
        return None

    def get_angle(self, data):
        if len(data) < 7:
            return 
        cmd = struct.unpack('c', data[0:1])[0]
        if cmd == b'S': # 0x53
            return np.array(struct.unpack('<hhh', data[1:7]))/32768.0*180.0 
        return None

    def get_quaternion(self, data):
        if len(data) < 9:
            return None
        cmd = struct.unpack('c', data[0:1])[0]
        if cmd == b'Y':
            q = np.array(struct.unpack('<hhhh', data[1:9]))/32768.0
            return np.array([q[1],q[2],q[3],q[0]])
        return None
    
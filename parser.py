
import re

class GCodeParser:
    def __init__(self):
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_z = 0.0
        self.current_feed = 0.0

    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith(';'):
            return None
        line = line.upper()

        # 🔍 1. ตรวจจับ Modal Conflict (คำสั่งขยับตีกันเองในบรรทัดเดียว)
        all_g_moves = re.findall(r'(G00|G01|G0|G1)', line)
        errors = []
        if len(all_g_moves) > 1:
            errors.append(f"⚠️ Modal Conflict: พบคำสั่งเคลื่อนที่ซ้อนกัน {all_g_moves} ในบรรทัดเดียว!")

        g_match = re.search(r'(G00|G01|G0|G1)', line)
        if not g_match:
            return None
            
        cmd = g_match.group(1)
        if cmd == 'G0': cmd = 'G00'
        if cmd == 'G1': cmd = 'G01'

        x_match = re.search(r'X([\d.-]+)', line)
        y_match = re.search(r'Y([\d.-]+)', line)
        z_match = re.search(r'Z([\d.-]+)', line)
        f_match = re.search(r'F([\d.-]+)', line)

        x = float(x_match.group(1)) if x_match else self.current_x
        y = float(y_match.group(1)) if y_match else self.current_y
        z = float(z_match.group(1)) if z_match else self.current_z
        f = float(f_match.group(1)) if f_match else self.current_feed

        # 🔍 2. ตรวจจับ G00 Crash (ห้ามใช้ความเร็วสูงสุดวิ่งทิ่มลงใต้ผิวชิ้นงาน Z < 0)
        if cmd == 'G00' and z < 0.0:
            errors.append(f"💥 หายนะระวังชน! (G00 Rapid Crash): สั่งหัวกัดพุ่งลงเนื้อชิ้นงาน (Z={z}) ด้วยความเร็วสูงสุด เครื่องจะพัง!")

        if cmd == 'G01' and f == 0.0:
            errors.append("⚠️ คัดค้าน: ลืมตั้งค่า Feed rate (F) ในการกัดงาน หัวกัดจะหัก!")

        move_data = {
            "type": cmd,
            "start": (self.current_x, self.current_y, self.current_z),
            "end": (x, y, z),
            "feed": f,
            "errors": errors
        }

        self.current_x, self.current_y, self.current_z, self.current_feed = x, y, z, f
        return move_data
import math

class GCodeCalculator:
    @staticmethod
    def calculate_distance(start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]
        return math.sqrt(dx**2 + dy**2 + dz**2)

    @staticmethod
    def process_gcode(segments):
        total_rapid_dist = 0.0
        total_cut_dist = 0.0
        total_time_minutes = 0.0
        all_errors = []

        # 📐 กำหนดขนาดตู้จริงของเครื่อง CNC (Soft Limits สำหรับตรวจตู้ทะลุ)
        LIMIT_X_MIN, LIMIT_X_MAX = 0.0, 300.0
        LIMIT_Y_MIN, LIMIT_Y_MAX = 0.0, 300.0
        LIMIT_Z_MIN, LIMIT_Z_MAX = -50.0, 10.0

        for seg in segments:
            dist = GCodeCalculator.calculate_distance(seg["start"], seg["end"])
            
            if seg["type"] == "G00":
                total_rapid_dist += dist
                total_time_minutes += dist / 3000.0
            elif seg["type"] == "G01":
                total_cut_dist += dist
                if seg["feed"] > 0:
                    total_time_minutes += dist / seg["feed"]
            
            if "errors" in seg and seg["errors"]:
                all_errors.extend(seg["errors"])
                
            # 🔍 3. ตรวจจับการวิ่งทะลุขอบตู้ (Soft Limit Violation)
            ex, ey, ez = seg["end"]
            if not (LIMIT_X_MIN <= ex <= LIMIT_X_MAX):
                all_errors.append(f"🛑 วิ่งทะลุตู้แกน X! พิกัด {ex} มม. ออกนอกขอบเขตเครื่อง ({LIMIT_X_MIN} ถึง {LIMIT_X_MAX})")
            if not (LIMIT_Y_MIN <= ey <= LIMIT_Y_MAX):
                all_errors.append(f"🛑 วิ่งทะลุตู้แกน Y! พิกัด {ey} มม. ออกนอกขอบเขตเครื่อง ({LIMIT_Y_MIN} ถึง {LIMIT_Y_MAX})")
            if not (LIMIT_Z_MIN <= ez <= LIMIT_Z_MAX):
                all_errors.append(f"🛑 วิ่งทะลุตู้แกน Z! พิกัด {ez} มม. ออกนอกขอบเขตเครื่อง ({LIMIT_Z_MIN} ถึง {LIMIT_Z_MAX})")

        return {
            "rapid_distance": total_rapid_dist,
            "cutting_distance": total_cut_dist,
            "total_distance": total_rapid_dist + total_cut_dist,
            "estimated_time": total_time_minutes,
            "errors": list(set(all_errors))
        }
import streamlit as st
from parser import GCodeParser
from calculator import GCodeCalculator

# ตั้งค่าหน้าตาของหน้าเว็บแอปพลิเคชัน
st.set_page_config(page_title="Industrial G-Code Analyzer", page_icon="🛡️", layout="wide")

st.title("🛡️ Industrial G-Code Smart Analyzer")
st.subheader("ระบบตรวจจับข้อผิดพลาดและวิเคราะห์ G-Code อัจฉริยะระดับโรงงาน")
st.write("จำลองการตรวจสอบโค้ดมหาภัยที่เสี่ยงต่อความเสียหายของเครื่องจักร")

# สร้างแถบเมนูด้านซ้ายสำหรับป้อนข้อมูล G-Code
st.sidebar.header("📥 ข้อมูลอินพุต (Input)")

# โค้ดตัวอย่างมหาภัยเริ่มต้น
default_gcode = """G00 X10.0 Y20.0 Z-5.0 ; 💥 ชนแน่: ใช้ G00 ดิ่งลงเนื้อชิ้นงานลึก Z-5!
G00 G01 X50.0 Y20.0 Z2.0 F1000 ; ⚠️ คำสั่งขัดแย้ง: มีทั้ง G00 และ G01 ตีกันเอง
G01 X500.0 Y100.0 Z0.0 F1000 ; 🛑 ทะลุตู้: พิกัด X500 วิ่งเลยตู้เครื่องที่จำกัดไว้แค่ 300!"""

# ช่องให้ผู้ใช้ใส่หรือแก้ไข G-Code บนหน้าเว็บ
gcode_input = st.sidebar.text_area("วางโค้ด G-Code ที่นี่เพื่อทดสอบ:", value=default_gcode, height=250)

if st.sidebar.button("⚙️ เริ่มวิเคราะห์โค้ด (Analyze)", type="primary"):
    # แปลงข้อความที่ป้อนเข้ามาแยกเป็นรายบรรทัด
    sample_gcode = [line.strip() for line in gcode_input.split('\n') if line.strip()]
    
    parser = GCodeParser()
    segments = []

    # เริ่มวิเคราะห์ข้อมูลผ่าน Parser
    for line in sample_gcode:
        result = parser.parse_line(line)
        if result:
            segments.append(result)

    # คำนวณผลลัพธ์ผ่าน Calculator
    stats = GCodeCalculator.process_gcode(segments)

    # --- ส่วนการแสดงผลบนหน้าเว็บ Streamlit ---
    
    # 1. แสดงกล่องสรุปตัวเลขทางคณิตศาสตร์ (Metrics)
    st.markdown("### 📊 รายงานสรุปผลทางคณิตศาสตร์")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="ระยะทางรวมทั้งหมด (Total Distance)", value=f"{stats['total_distance']:.2f} มม.")
    with col2:
        st.metric(label="เวลาทำงานโดยประมาณ (Estimated Time)", value=f"{stats['estimated_time']:.4f} นาที")

    st.divider()

    # 2. แสดงผลระบบสแกนความปลอดภัยเด็ดขาด
    st.markdown("### 🛡️ ระบบตรวจจับข้อผิดพลาด (Industrial Scan)")
    
    if stats["errors"]:
        # ขีดเตือนสีแดงหากพบอันตรายร้ายแรง
        st.error(f"⚠️ ตรวจพบจุดอันตรายระดับร้ายแรงทั้งหมด {len(stats['errors'])} จุด ดังต่อไปนี้:")
        for err in stats["errors"]:
            st.warning(err)
    else:
        # ขึ้นแถบสีเขียวถ้าผ่านเกณฑ์
        st.success("✅ ปลอดภัยสูงสุด โค้ดผ่านเกณฑ์มาตรฐานโรงงาน ไม่มีสิ่งผิดปกติ")
        
else:
    st.info("💡 กรุณากดปุ่ม **'เริ่มวิเคราะห์โค้ด (Analyze)'** ที่แถบเมนูด้านซ้าย เพื่อเริ่มต้นระบบสแกนพิกัดเครื่องจักรครับ")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os

# Clean sans-serif font
plt.rcParams['font.sans-serif'] = 'Segoe UI'
plt.rcParams['font.family'] = 'sans-serif'

# Figure setup: 16:9 canvas
fig, ax = plt.subplots(figsize=(19, 10.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# -------------------------------------------------------------
# 1. Header & Logo Integration (Top area)
# -------------------------------------------------------------
logo_path = 'E:/MedStream/docs/logo.png'
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
    # [left, bottom, width, height]
    ax_logo = fig.add_axes([0.045, 0.85, 0.15, 0.11])
    ax_logo.imshow(logo_img)
    ax_logo.axis('off')

# Title & Subtitle next to logo
ax.text(21, 92.5, "MedStream : End-to-End System Architecture", 
        fontsize=23, fontweight='bold', color='#0F172A', va='center')
ax.text(21, 87.5, "IoT Edge Biosensors  •  Batch Data Pipeline  •  DuckDB Warehouse  •  Random Forest (97.2%)  •  Streamlit UI", 
        fontsize=11.5, color='#64748B', va='center')

# Thin divider below header
ax.plot([4.5, 95.5], [83.5, 83.5], color='#E2E8F0', lw=1.2)


# -------------------------------------------------------------
# Helper function to draw minimalist cards
# -------------------------------------------------------------
def draw_card(ax, x, y, w, h, title, subtitle="", items=None, 
              bg_color='#FFFFFF', border_color='#CBD5E1', title_color='#0F172A', 
              badge="", badge_color='#2563EB', badge_bg='#EFF6FF'):
    
    rect = patches.FancyBboxPatch((x, y), w, h,
                                  boxstyle="round,pad=0.2,rounding_size=1.2",
                                  facecolor=bg_color, edgecolor=border_color,
                                  linewidth=1.2, zorder=2)
    ax.add_patch(rect)
    
    if badge:
        ax.text(x + 1.5, y + h - 2.2, badge.upper(), fontsize=7.2, fontweight='bold',
                color=badge_color, zorder=3,
                bbox=dict(facecolor=badge_bg, edgecolor='none', boxstyle='round,pad=0.22'))
        title_y = y + h - 4.8
    else:
        title_y = y + h - 3.2
        
    ax.text(x + w/2, title_y, title, fontsize=10.5, fontweight='bold', 
            color=title_color, ha='center', va='center', zorder=3)
    
    curr_y = title_y - 2.5
    if subtitle:
        ax.text(x + w/2, curr_y, subtitle, fontsize=8.2, color='#64748B', 
                ha='center', va='center', zorder=3)
        curr_y -= 2.2
        
    if items:
        ax.plot([x + 1.5, x + w - 1.5], [curr_y + 0.8, curr_y + 0.8], color='#E2E8F0', lw=0.8, zorder=3)
        curr_y -= 1.6
        for it in items:
            ax.text(x + 1.8, curr_y, it, fontsize=8.0, color='#334155', ha='left', va='center', zorder=3)
            curr_y -= 2.0


def draw_arrow(ax, x1, y1, x2, y2, label="", label_pos=(0, 0), color='#64748B'):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5, mutation_scale=13),
                zorder=4)
    if label:
        lx = (x1 + x2)/2 + label_pos[0]
        ly = (y1 + y2)/2 + label_pos[1]
        ax.text(lx, ly, label, fontsize=7.8, fontweight='semibold', color=color,
                ha='center', va='center',
                bbox=dict(facecolor='#FFFFFF', edgecolor='#CBD5E1', boxstyle='round,pad=0.2', lw=0.7),
                zorder=5)


# -------------------------------------------------------------
# Background Groups
# -------------------------------------------------------------
# Upper Zone: IoT Edge Hardware
bg_iot = patches.FancyBboxPatch((4.5, 47), 54, 33,
                                boxstyle="round,pad=0.5,rounding_size=1.5",
                                facecolor='#F8FAFC', edgecolor='#E2E8F0',
                                linewidth=1.0, linestyle='--', zorder=1)
ax.add_patch(bg_iot)
ax.text(6, 77.8, "EDGE HARDWARE & LIVE BIOSENSING LAYER", fontsize=8.5, fontweight='bold', color='#475569', zorder=2)

# Lower Zone: Batch Data Pipeline
bg_batch = patches.FancyBboxPatch((4.5, 8.5), 54, 35,
                                  boxstyle="round,pad=0.5,rounding_size=1.5",
                                  facecolor='#F8FAFC', edgecolor='#E2E8F0',
                                  linewidth=1.0, linestyle='--', zorder=1)
ax.add_patch(bg_batch)
ax.text(6, 41.3, "HISTORICAL DATA & ETL PIPELINE (100K PATIENT RECORDS)", fontsize=8.5, fontweight='bold', color='#475569', zorder=2)

# Right Zone: Core Intelligence & Delivery
bg_core = patches.FancyBboxPatch((62.5, 8.5), 33, 71.5,
                                 boxstyle="round,pad=0.5,rounding_size=1.5",
                                 facecolor='#F0F7FF', edgecolor='#BFDBFE',
                                 linewidth=1.0, zorder=1)
ax.add_patch(bg_core)
ax.text(64, 77.8, "CENTRAL WAREHOUSE & AI CORE", fontsize=8.5, fontweight='bold', color='#1D4ED8', zorder=2)


# -------------------------------------------------------------
# 2. IoT Hardware Layer (Top-Left)
# -------------------------------------------------------------
# Biosensors
draw_card(ax, x=6.5, y=50, w=15.5, h=24,
          title="Patient Biosensors",
          subtitle="Non-invasive Vitals",
          items=[
              "• MAX30102 (SpO2 & HR)",
              "• MLX90614 (Body Temp)",
              "• AD8232 (3-Lead ECG)",
              "• 100 kHz Shared I2C Bus"
          ],
          bg_color='#FFFFFF', border_color='#93C5FD',
          badge="Inputs", badge_color='#2563EB', badge_bg='#EFF6FF')

# ESP32
draw_card(ax, x=33, y=50, w=17.5, h=24,
          title="ESP32 Microcontroller",
          subtitle="NodeMCU DevKit V1",
          items=[
              "• FreeRTOS Task Scheduling",
              "• ADC Sampling (ECG Pin 34)",
              "• OLED 0.96\" SSD1306 Display",
              "• Active Buzzer & Alert LED",
              "• Wi-Fi 2.4 GHz Telemetry"
          ],
          bg_color='#FFFFFF', border_color='#2563EB',
          badge="Edge Processing", badge_color='#1D4ED8', badge_bg='#DBEAFE')

# Arrow: Biosensors -> ESP32
draw_arrow(ax, 23.2, 62, 31.8, 62, label="I2C / ADC", color='#2563EB')


# -------------------------------------------------------------
# 3. Batch Data Pipeline Layer (Bottom-Left)
# -------------------------------------------------------------
# Raw Data
draw_card(ax, x=6.5, y=11.5, w=14, h=25.5,
          title="Raw Dataset",
          subtitle="CSV Storage",
          items=[
              "• 100,000 Patient Records",
              "• 9 Clinical Features",
              "• Glucose & HbA1c Levels",
              "• Age, Gender, BMI, History"
          ],
          bg_color='#FFFFFF', border_color='#CBD5E1',
          badge="Raw Source", badge_color='#64748B', badge_bg='#F1F5F9')

# Cleaning
draw_card(ax, x=24, y=11.5, w=15, h=25.5,
          title="Data Cleaning",
          subtitle="MedStream.ipynb",
          items=[
              "• Deduplication & Imputation",
              "• Smoking History Mapping",
              "• Gender One-Hot Encoding",
              "• Output: 96,128 Valid Rows"
          ],
          bg_color='#FFFFFF', border_color='#CBD5E1',
          badge="ETL Clean", badge_color='#475569', badge_bg='#F1F5F9')

# EDA
draw_card(ax, x=42, y=11.5, w=14.5, h=25.5,
          title="EDA & Insights",
          subtitle="EDA.ipynb",
          items=[
              "• Correlation Matrix",
              "• Distribution & Outliers",
              "• Biomarker Separation",
              "• Feature Selection"
          ],
          bg_color='#FFFFFF', border_color='#CBD5E1',
          badge="Analysis", badge_color='#475569', badge_bg='#F1F5F9')

# Arrows: Raw -> Clean -> EDA
draw_arrow(ax, 21.2, 24.2, 23.2, 24.2, color='#64748B')
draw_arrow(ax, 39.8, 24.2, 41.2, 24.2, color='#64748B')


# -------------------------------------------------------------
# 4. Central Data Warehouse & AI Engine (Right Side)
# -------------------------------------------------------------
# DuckDB
draw_card(ax, x=65, y=55.5, w=28, h=19.5,
          title="Data Warehouse (DuckDB)",
          subtitle="In-Process Embedded OLAP Engine",
          items=[
              "• High-Performance Columnar Storage (`patients_analytics`)",
              "• Ingests Cleaned Cohort + Real-time Streaming Logs",
              "• Zero-overhead fast SQL analytical queries"
          ],
          bg_color='#FFFFFF', border_color='#3B82F6',
          badge="Unified Storage", badge_color='#1E40AF', badge_bg='#DBEAFE')

# AI Model (increased height, properly spaced)
draw_card(ax, x=65, y=33.5, w=28, h=18.0,
          title="AI Risk Predictor (Random Forest)",
          subtitle="Trained on 96,128 Validated Records",
          items=[
              "• 97.2% Classification Accuracy | High Recall for At-Risk",
              "• Top Predictive Weights: Blood Glucose & HbA1c",
              "• Exported Artifact: `models/diabetes_model.pkl`"
          ],
          bg_color='#FFFFFF', border_color='#10B981',
          badge="Machine Learning", badge_color='#065F46', badge_bg='#D1FAE5')

# Streamlit App
draw_card(ax, x=65, y=11.5, w=28, h=18.0,
          title="MedStream Dashboard (Streamlit)",
          subtitle="Interactive Clinical Decision Support UI",
          items=[
              "• Tab 1: Patient Clinical Risk Assessment & Triage",
              "• Tab 2: DuckDB Population Analytics & Cohorts",
              "• Live Telemetry Display & Diagnostic Alerting"
          ],
          bg_color='#FFFFFF', border_color='#2563EB',
          badge="Application", badge_color='#1D4ED8', badge_bg='#EFF6FF')


# -------------------------------------------------------------
# 5. Connecting Arrows (Clean & Non-overlapping)
# -------------------------------------------------------------
# Arrow: ESP32 -> DuckDB (Wi-Fi Telemetry)
draw_arrow(ax, 51.5, 62, 64.2, 62, 
           label="Wi-Fi (JSON / HTTP)", label_pos=(0, 2.2), color='#2563EB')

# Arrow: EDA -> DuckDB (Warehouse Ingestion)
ax.annotate("", xy=(64.2, 58.0), xytext=(57.2, 24.2),
            arrowprops=dict(arrowstyle="-|>", color='#64748B', lw=1.5, 
                            connectionstyle="angle,angleA=0,angleB=90,rad=3", mutation_scale=13),
            zorder=4)
ax.text(59.5, 38, "DuckDB Ingestion", fontsize=7.8, fontweight='semibold', color='#475569',
        rotation=90, ha='center', va='center',
        bbox=dict(facecolor='#FFFFFF', edgecolor='#CBD5E1', boxstyle='round,pad=0.2', lw=0.7),
        zorder=5)

# Arrow: DuckDB -> AI Model
draw_arrow(ax, 79, 54.8, 79, 52.2, label="Feature Extraction", label_pos=(6.8, 0), color='#10B981')

# Arrow: AI Model -> Streamlit Dashboard
draw_arrow(ax, 79, 32.8, 79, 30.2, label="Inference Engine", label_pos=(6.4, 0), color='#2563EB')


# Save high-res outputs
output_png = 'E:/MedStream/docs/pipeline_diagram_iot.png'
output_jpg = 'E:/MedStream/docs/pipeline_diagram_iot.jpg'
plt.savefig(output_png, dpi=300, bbox_inches='tight')
plt.savefig(output_jpg, dpi=300, bbox_inches='tight')
plt.savefig('E:/MedStream/docs/pipeline_diagram.jpg', dpi=300, bbox_inches='tight')
plt.close()
print("Diagram perfectly rendered!")

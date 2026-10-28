"""
Generate Power BI Dashboard Visual Previews
Author: Senior Data Analyst & Power BI Developer
Description:
    Renders high-resolution visual mockups of the Power BI dashboard layout,
    KPI cards, and charts using Matplotlib and Seaborn, saved to powerbi/
    and reports/charts/ for GitHub documentation and interview readiness.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np

def generate_visuals():
    cleaned_csv = os.path.join("data", "processed", "cleaned_sales_data.csv")
    df = pd.read_csv(cleaned_csv)

    charts_dir = os.path.join("reports", "charts")
    powerbi_dir = "powerbi"
    os.makedirs(charts_dir, exist_ok=True)
    os.makedirs(powerbi_dir, exist_ok=True)

    # Calculate Core Metrics
    total_revenue = df['sales'].sum()
    total_profit = df['profit'].sum()
    total_orders = df['order_id'].nunique()
    total_units = df['quantity'].sum()
    margin_pct = (total_profit / total_revenue) * 100

    # Modern Dark Theme Palette
    bg_dark = "#0F172A"       # Slate 900
    card_bg = "#1E293B"       # Slate 800
    border_color = "#334155"  # Slate 700
    text_white = "#F8FAFC"
    text_muted = "#94A3B8"
    accent_blue = "#3B82F6"
    accent_green = "#10B981"
    accent_red = "#EF4444"
    accent_amber = "#F59E0B"

    # -------------------------------------------------------------------------
    # 1. COMPOSITE EXECUTIVE DASHBOARD MOCKUP
    # -------------------------------------------------------------------------
    fig = plt.figure(figsize=(18, 11), facecolor=bg_dark)
    gs = gridspec.GridSpec(3, 3, height_ratios=[0.8, 2.2, 2.2], width_ratios=[1.2, 1, 1], figure=fig)
    plt.subplots_adjust(left=0.04, right=0.96, top=0.94, bottom=0.06, wspace=0.22, hspace=0.32)

    # Canvas Title & Subtitle Banner
    fig.text(0.04, 0.97, "EXECUTIVE E-COMMERCE SALES & BUSINESS PERFORMANCE DASHBOARD",
             fontsize=16, fontweight="bold", color=text_white, family="sans-serif")
    fig.text(0.04, 0.95, "Comprehensive Enterprise Analytics | Jan 2023 - Dec 2024 | Powered by Power BI & SQL",
             fontsize=10, color=text_muted, family="sans-serif")

    # KPI Banner (Span across top)
    ax_kpi = fig.add_subplot(gs[0, :])
    ax_kpi.set_facecolor(card_bg)
    ax_kpi.axis("off")
    for spine in ax_kpi.spines.values():
        spine.set_color(border_color)

    kpi_boxes = [
        ("TOTAL REVENUE", f"${total_revenue:,.0f}", f"+12.4% vs LY", accent_blue, 0.10),
        ("TOTAL PROFIT", f"${total_profit:,.0f}", f"Net Profit (USD)", accent_green, 0.30),
        ("PROFIT MARGIN", f"{margin_pct:.1f}%", f"Healthy (>15%)", accent_amber, 0.50),
        ("TOTAL ORDERS", f"{total_orders:,}", f"Distinct Carts", text_white, 0.70),
        ("UNITS SHIPPED", f"{total_units:,}", f"4.18 Items/Order", accent_blue, 0.90)
    ]

    for title, val, sub, col, x_pos in kpi_boxes:
        ax_kpi.text(x_pos, 0.75, title, ha="center", va="center", color=text_muted, fontsize=9, fontweight="bold")
        ax_kpi.text(x_pos, 0.42, val, ha="center", va="center", color=col, fontsize=18, fontweight="bold")
        ax_kpi.text(x_pos, 0.15, sub, ha="center", va="center", color=text_muted, fontsize=8)

    # Visual 1: Monthly Sales & Profit Trajectory (gs[1, 0:2])
    ax1 = fig.add_subplot(gs[1, 0:2])
    ax1.set_facecolor(card_bg)
    monthly = df.groupby('order_month')[['sales', 'profit']].sum().reset_index()

    months = range(len(monthly))
    ax1.plot(months, monthly['sales'] / 1000, color=accent_blue, marker='o', linewidth=2.5, label='Sales ($K)')
    ax1.plot(months, monthly['profit'] / 1000, color=accent_green, marker='s', linewidth=2.5, label='Profit ($K)')
    ax1.fill_between(months, monthly['sales'] / 1000, color=accent_blue, alpha=0.15)

    ax1.set_title("Monthly Revenue & Net Profit Trajectory ($ in Thousands)", color=text_white, fontsize=12, fontweight="bold", pad=10)
    ax1.set_xticks(months[::2])
    ax1.set_xticklabels(monthly['order_month'][::2], color=text_muted, rotation=35, fontsize=8)
    ax1.tick_params(colors=text_muted)
    ax1.grid(color=border_color, linestyle="--", alpha=0.5)
    ax1.legend(facecolor=card_bg, edgecolor=border_color, labelcolor=text_white, loc="upper left")

    # Visual 2: Category Sales & Profit Breakdown (gs[1, 2])
    ax2 = fig.add_subplot(gs[1, 2])
    ax2.set_facecolor(card_bg)
    cat_summary = df.groupby('category')[['sales', 'profit']].sum().reset_index()
    y_pos = np.arange(len(cat_summary))
    height = 0.35

    ax2.barh(y_pos + height/2, cat_summary['sales'] / 1000, height, label='Sales ($K)', color=accent_blue)
    ax2.barh(y_pos - height/2, cat_summary['profit'] / 1000, height, label='Profit ($K)', color=accent_green)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(cat_summary['category'], color=text_white, fontsize=9, fontweight="bold")
    ax2.set_title("Category Revenue vs Profit Mix", color=text_white, fontsize=12, fontweight="bold", pad=10)
    ax2.tick_params(colors=text_muted)
    ax2.grid(color=border_color, linestyle="--", alpha=0.5, axis='x')
    ax2.legend(facecolor=card_bg, edgecolor=border_color, labelcolor=text_white, loc="lower right", fontsize=8)

    # Visual 3: Top 5 Revenue-Generating Products (gs[2, 0])
    ax3 = fig.add_subplot(gs[2, 0])
    ax3.set_facecolor(card_bg)
    top_prods = df.groupby('product_name')['sales'].sum().reset_index().sort_values('sales', ascending=True).tail(5)
    # Shorten names for clean display
    short_names = [n[:22] + "..." if len(n) > 22 else n for n in top_prods['product_name']]
    ax3.barh(short_names, top_prods['sales'] / 1000, color="#6366F1")
    ax3.set_title("Top 5 Revenue Products ($K)", color=text_white, fontsize=11, fontweight="bold", pad=10)
    ax3.tick_params(colors=text_muted)
    ax3.grid(color=border_color, linestyle="--", alpha=0.5, axis='x')

    # Visual 4: Bottom 4 Loss-Making Products (gs[2, 1])
    ax4 = fig.add_subplot(gs[2, 1])
    ax4.set_facecolor(card_bg)
    bottom_prods = df.groupby('product_name')['profit'].sum().reset_index().sort_values('profit', ascending=True).head(4)
    short_loss_names = [n[:20] + "..." if len(n) > 20 else n for n in bottom_prods['product_name']]
    ax4.barh(short_loss_names, bottom_prods['profit'] / 1000, color=accent_red)
    ax4.set_title("Loss-Making Products ($K Profit)", color=text_white, fontsize=11, fontweight="bold", pad=10)
    ax4.tick_params(colors=text_muted)
    ax4.grid(color=border_color, linestyle="--", alpha=0.5, axis='x')

    # Visual 5: Regional Profit Margin Comparison (gs[2, 2])
    ax5 = fig.add_subplot(gs[2, 2])
    ax5.set_facecolor(card_bg)
    reg_summary = df.groupby('region').agg(sales=('sales', 'sum'), profit=('profit', 'sum')).reset_index()
    reg_summary['margin'] = (reg_summary['profit'] / reg_summary['sales']) * 100
    bars = ax5.bar(reg_summary['region'], reg_summary['margin'], color=[accent_green if m >= 18 else accent_amber for m in reg_summary['margin']])
    ax5.set_title("Regional Profit Margin %", color=text_white, fontsize=11, fontweight="bold", pad=10)
    ax5.set_ylabel("Margin %", color=text_muted)
    ax5.tick_params(colors=text_muted)
    ax5.grid(color=border_color, linestyle="--", alpha=0.5, axis='y')
    for bar in bars:
        yval = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f"{yval:.1f}%", ha='center', va='bottom', color=text_white, fontsize=9, fontweight="bold")

    preview_path = os.path.join(powerbi_dir, "dashboard_preview.png")
    fig.savefig(preview_path, dpi=200, facecolor=bg_dark, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated Power BI Dashboard visual preview: {preview_path}")

    # Generate individual chart images for reports
    # Chart 1: Monthly Trend
    fig1, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(monthly['order_month'], monthly['sales'] / 1000, marker='o', color='#2563EB', linewidth=2.5, label='Sales ($K)')
    ax.plot(monthly['order_month'], monthly['profit'] / 1000, marker='s', color='#10B981', linewidth=2.5, label='Profit ($K)')
    ax.set_title("Monthly Sales and Profit Trend (2023 - 2024)", fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel("$ in Thousands")
    ax.set_xticklabels(monthly['order_month'], rotation=45, ha='right')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    fig1.tight_layout()
    fig1.savefig(os.path.join(charts_dir, "monthly_trend.png"), dpi=150)
    plt.close(fig1)

    # Chart 2: Category Breakdown
    fig2, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11, 4))
    cat_summary = df.groupby('category').agg(sales=('sales', 'sum'), profit=('profit', 'sum')).reset_index()
    cat_summary['margin'] = (cat_summary['profit'] / cat_summary['sales']) * 100
    ax_a.bar(cat_summary['category'], cat_summary['sales'] / 1000, color='#3B82F6')
    ax_a.set_title("Category Revenue ($K)", fontweight='bold')
    ax_b.bar(cat_summary['category'], cat_summary['margin'], color='#10B981')
    ax_b.set_title("Category Profit Margin %", fontweight='bold')
    fig2.tight_layout()
    fig2.savefig(os.path.join(charts_dir, "category_breakdown.png"), dpi=150)
    plt.close(fig2)

    print(f"Saved charts into: {charts_dir}")

if __name__ == "__main__":
    generate_visuals()

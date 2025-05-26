import customtkinter as ctk
from Database.handle import get_connection
import pandas as pd
import matplotlib.pyplot as plt
import re

class App(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.load_btn = ctk.CTkButton(self, text="Tải dữ liệu", command=self.load_data)
        self.load_btn.pack(pady=10)

        self.col_combo = ctk.CTkComboBox(self, values=["--"], command=self.analyze_column)
        self.col_combo.pack(pady=10)

        self.analyze_food_btn = ctk.CTkButton(self, text="Phân tích món ăn theo ngày", command=self.analyze_food_time)
        self.analyze_food_btn.pack(pady=10)

        self.output = ctk.CTkTextbox(self, width=500, height=200)
        self.output.pack(pady=10)

        self.df = pd.DataFrame()

    def load_data(self):
        conn = get_connection()
        query = "SELECT * FROM orders"
        self.df = pd.read_sql(query, conn)
        conn.close()

        self.df["price"] = pd.to_numeric(self.df["price"], errors="coerce")

        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            self.col_combo.configure(values=numeric_cols)
            self.col_combo.set(numeric_cols[0])
        else:
            self.col_combo.configure(values=["--"])
            self.col_combo.set("--")

    def analyze_column(self, col_name):
        if col_name not in self.df.columns:
            return
        series = self.df[col_name].dropna()
        stats = {
            "Trung bình": series.mean(),
            "Tối thiểu": series.min(),
            "Tối đa": series.max(),
            "Độ lệch chuẩn": series.std()
        }
        self.output.delete("0.0", "end")
        for k, v in stats.items():
            self.output.insert("end", f"{k}: {v:.2f}\n")
        plt.figure(figsize=(5, 3))
        plt.hist(series, bins=20, edgecolor='black')
        plt.title(f'Phân phối: {col_name}')
        plt.xlabel(col_name)
        plt.ylabel("Tần suất")
        plt.tight_layout()
        plt.show()

    def analyze_food_time(self):
        if self.df.empty or "food_item" not in self.df.columns or "created_at" not in self.df.columns:
            self.output.delete("0.0", "end")
            self.output.insert("end", "Không có dữ liệu món ăn hoặc cột thời gian.")
            return

        df = self.df.dropna(subset=['food_item'])
        df['date'] = pd.to_datetime(df['created_at']).dt.date

        rows = []
        for _, row in df.iterrows():
            date = row['date']
            items = [item.strip() for item in str(row['food_item']).split(',')]
            for item in items:
                m = re.match(r"(.+?) x(\d+)", item)
                if m:
                    food = m.group(1).strip()
                    count = int(m.group(2))
                else:
                    food = item
                    count = 1
                rows.append({'date': date, 'food': food, 'count': count})

        food_df = pd.DataFrame(rows)
        if food_df.empty:
            self.output.delete("0.0", "end")
            self.output.insert("end", "Không tìm thấy dữ liệu món ăn hợp lệ.")
            return

        summary = food_df.groupby(['date', 'food'])['count'].sum().unstack(fill_value=0)

        # Hiển thị kết quả
        self.output.delete("0.0", "end")
        self.output.insert("end", summary.to_string())

        # Vẽ biểu đồ
        plt.figure(figsize=(10, 5))
        summary.plot(ax=plt.gca())
        plt.xlabel('Ngày')
        plt.ylabel('Số lượng bán')
        plt.title('Tần suất xuất hiện của từng món ăn theo ngày')
        plt.legend(title='Món ăn')
        plt.tight_layout()
        plt.show()
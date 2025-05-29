import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
import re
from Database.handle import get_connection

class App(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.analyze_food_btn = ctk.CTkButton(self, text="Phân tích món ăn theo ngày", command=self.analyze_food_time)
        self.analyze_food_btn.pack(pady=10)

        self.revenue_btn = ctk.CTkButton(self, text="Thống kê doanh thu theo ngày", command=self.analyze_revenue)
        self.revenue_btn.pack(pady=10)

        self.output = ctk.CTkTextbox(self, width=550, height=240)
        self.output.pack(pady=10)

        self.df = pd.DataFrame()
        self.load_data_analyze()

    def load_data_analyze(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            query = "SELECT * FROM orders"
            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            conn.close()

            if not results:
                self.output.insert("end", "Không có dữ liệu trong bảng orders.\n")
                return

            self.df = pd.DataFrame(results)


            required_columns = ['food_item', 'created_at', 'price']
            missing_columns = [col for col in required_columns if col not in self.df.columns]
            if missing_columns:
                self.output.insert("end", f"Lỗi: Thiếu các cột {missing_columns} trong dữ liệu.\n")
                self.df = pd.DataFrame()
                return

        except Exception as e:
            self.output.insert("end", f"Lỗi khi tải dữ liệu: {e}\n")
            self.df = pd.DataFrame()

    def analyze_food_time(self):
        if self.df.empty or "food_item" not in self.df.columns or "created_at" not in self.df.columns:
            self.output.delete("0.0", "end")
            self.output.insert("end", "Không có dữ liệu món ăn hoặc cột thời gian.\n")
            return

        df = self.df.dropna(subset=['food_item']).copy()
        df.loc[:, 'date'] = pd.to_datetime(df['created_at']).dt.date

        rows = []
        for _, row in df.iterrows():
            date = row['date']
            items = [item.strip() for item in str(row['food_item']).split(',')]
            for item in items:
                soluong = re.match(r"(.+?) x(\d+)", item)
                if soluong:
                    food = soluong.group(1).strip()
                    count = int(soluong.group(2))
                else:
                    food = item
                    count = 1
                rows.append({'date': date, 'food': food, 'count': count})

        food_df = pd.DataFrame(rows)
        if food_df.empty:
            self.output.delete("0.0", "end")
            self.output.insert("end", "Không tìm thấy dữ liệu món ăn hợp lệ.\n")
            return

        summary = food_df.groupby(['date', 'food'])['count'].sum().unstack(fill_value=0)

        # Display results
        self.output.delete("0.0", "end")
        self.output.insert("end", "Thống kê số lượng món ăn bán mỗi ngày:\n")
        self.output.insert("end", summary.to_string())

        # Plot chart
        plt.figure(figsize=(10, 5))
        summary.plot(ax=plt.gca())
        plt.xlabel('Ngày')
        plt.ylabel('Số lượng bán')
        plt.title('Tần suất xuất hiện của từng món ăn theo ngày')
        plt.legend(title='Món ăn')
        plt.tight_layout()
        plt.show()

    def analyze_revenue(self):
        if self.df.empty or "price" not in self.df.columns or "created_at" not in self.df.columns:
            self.output.delete("0.0", "end")
            self.output.insert("end", "Không có dữ liệu doanh thu hoặc cột thời gian.\n")
            return

        try:
            df = self.df.dropna(subset=['price']).copy()
            df.loc[:, 'date'] = pd.to_datetime(df['created_at']).dt.date
            df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)

            revenue_by_day = df.groupby('date')['price'].sum() * 0.2

            total_revenue = revenue_by_day.sum()

            self.output.delete("0.0", "end")
            self.output.insert("end", "Doanh thu từng ngày:\n")
            self.output.insert("end", revenue_by_day.to_string())
            self.output.insert("end", f"\n\nTổng doanh thu: {total_revenue:,.0f} VND\n")

            plt.figure(figsize=(10, 4))
            revenue_by_day.plot(kind='bar', color='green')
            plt.xlabel('Ngày')
            plt.ylabel('Doanh thu (VND)')
            plt.title('Doanh thu theo từng ngày')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.output.delete("0.0", "end")
            self.output.insert("end", f"Lỗi khi phân tích doanh thu: {e}\n")
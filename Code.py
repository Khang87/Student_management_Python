import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

DATA_FILE = 'hrm_data.json'

def load_json(path):
    if not os.path.exists(path):
        return {'employees': [], 'contracts': [], 'degrees': [], 'attendance': []}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

db = load_json(DATA_FILE)

def get_contracts(emp_id):
    for c in db['contracts']:
        if c['employee_id'] == emp_id:
            return c['contracts']
    return []
def set_contracts(emp_id, contracts_list):
    for c in db['contracts']:
        if c['employee_id'] == emp_id:
            c['contracts'] = contracts_list
            break
    else:
        db['contracts'].append({"employee_id": emp_id, "contracts": contracts_list})
    save_json(DATA_FILE, db)

def get_degrees(emp_id):
    for d in db['degrees']:
        if d['employee_id'] == emp_id:
            return d['degrees']
    return []
def set_degrees(emp_id, degrees_list):
    for d in db['degrees']:
        if d['employee_id'] == emp_id:
            d['degrees'] = degrees_list
            break
    else:
        db['degrees'].append({"employee_id": emp_id, "degrees": degrees_list})
    save_json(DATA_FILE, db)

def get_attendance(emp_id):
    for a in db['attendance']:
        if a['employee_id'] == emp_id:
            return a['attendance']
    return []
def set_attendance(emp_id, attendance_list):
    for a in db['attendance']:
        if a['employee_id'] == emp_id:
            a['attendance'] = attendance_list
            break
    else:
        db['attendance'].append({"employee_id": emp_id, "attendance": attendance_list})
    save_json(DATA_FILE, db)

class HRMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý nhân sự chuyên nghiệp")
        self.geometry("1200x730")
        self.configure(bg="#EAF6FA")
        self.selected_emp = None

        lbl = tk.Label(self, text="DANH SÁCH NHÂN VIÊN", font=("Arial", 15, "bold"), bg="#EAF6FA", fg="#074173")
        lbl.pack(pady=7)
        columns = ('id', 'name', 'dob', 'gender', 'position', 'dept', 'team', 'city')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=10)
        for col, text, w in zip(columns,
                                ['Mã NV', 'Họ và tên', 'Ngày sinh', 'Giới tính', 'Chức vụ', 'Phòng ban', 'Bộ phận', 'Quê quán'],
                                [80, 170, 100, 70, 130, 160, 130, 110]):
            self.tree.heading(col, text=text)
            self.tree.column(col, width=w)
        self.tree.pack(fill='x', padx=12)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        btn_frame = tk.Frame(self, bg="#EAF6FA")
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Thêm", width=12, command=self.add_employee, bg="#38B000", fg="white", font=('Arial', 12, 'bold')).pack(side='left', padx=8)
        tk.Button(btn_frame, text="Sửa", width=12, command=self.edit_employee, bg="#3A86FF", fg="white", font=('Arial', 12, 'bold')).pack(side='left', padx=8)
        tk.Button(btn_frame, text="Xóa", width=12, command=self.delete_employee, bg="#E84545", fg="white", font=('Arial', 12, 'bold')).pack(side='left', padx=8)
        tk.Button(btn_frame, text="Tìm kiếm", width=12, command=self.search_employee, bg="#E1AC00", fg="white", font=('Arial', 12, 'bold')).pack(side='left', padx=8)
        tk.Button(btn_frame, text="Reset", width=12, command=self.load_data, bg="#8D99AE", fg="white", font=('Arial', 12, 'bold')).pack(side='left', padx=8)

        self.detail_frame = tk.Frame(self, bg="#BFDCE5")
        self.detail_frame.pack(fill='both', expand=True, padx=14, pady=7)
        self.detail_widgets = {}
        self.create_detail_panel()
        self.load_data()

    def load_data(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        ds = data if data is not None else db['employees']
        for emp in ds:
            self.tree.insert('', 'end', values=(emp['id'], emp['name'], emp['dob'], emp['gender'],
                                                emp['position'], emp['dept'], emp['team'], emp['city']))
        self.show_employee_detail(None)

    def create_detail_panel(self):
        f_left = tk.Frame(self.detail_frame, width=270, bg="#BFDCE5")
        f_left.pack(side='left', fill='y', padx=8, pady=8)
        self.detail_widgets['lbl_info'] = tk.Label(f_left, text="Chọn nhân viên để xem chi tiết", font=('Arial', 12), bg="#BFDCE5", anchor='w', justify='left')
        self.detail_widgets['lbl_info'].pack(anchor='nw', pady=10)
        self.detail_widgets['lbl_info2'] = tk.Label(f_left, text="", font=('Arial', 10), bg="#BFDCE5", anchor='w', justify='left')
        self.detail_widgets['lbl_info2'].pack(anchor='nw')

        f_right = tk.Frame(self.detail_frame, bg="#BFDCE5")
        f_right.pack(side='left', fill='both', expand=True)
        self.tabs = ttk.Notebook(f_right)
        self.tabs.pack(expand=True, fill='both', padx=6, pady=6)

        # Tab hợp đồng
        self.tab_contract = tk.Frame(self.tabs, bg="#F7F7F7")
        self.tabs.add(self.tab_contract, text="Hợp đồng")
        self.contract_tree = ttk.Treeview(self.tab_contract, columns=('số', 'loại', 'trạng_thái', 'ký_ngày'), show='headings', height=4)
        for col, text, w in zip(('số', 'loại', 'trạng_thái', 'ký_ngày'),
                                ['Số HĐ', 'Loại hợp đồng', 'Trạng thái', 'Ngày ký'],
                                [70, 180, 110, 100]):
            self.contract_tree.heading(col, text=text)
            self.contract_tree.column(col, width=w)
        self.contract_tree.pack(fill='x', pady=10)
        btn_frame_ct = tk.Frame(self.tab_contract, bg="#F7F7F7")
        btn_frame_ct.pack(pady=2)
        tk.Button(btn_frame_ct, text="Thêm", width=8, command=self.add_contract, bg="#38B000", fg="white").pack(side='left', padx=3)
        tk.Button(btn_frame_ct, text="Sửa", width=8, command=self.edit_contract, bg="#3A86FF", fg="white").pack(side='left', padx=3)
        tk.Button(btn_frame_ct, text="Xóa", width=8, command=self.delete_contract, bg="#E84545", fg="white").pack(side='left', padx=3)

        # Tab trình độ
        self.tab_trinhdo = tk.Frame(self.tabs, bg="#F7F7F7")
        self.tabs.add(self.tab_trinhdo, text="Trình độ")
        self.trinhdo_tree = ttk.Treeview(self.tab_trinhdo, columns=('Bằng cấp', 'Chuyên ngành', 'Năm TN'), show='headings', height=4)
        for col, text, w in zip(('Bằng cấp', 'Chuyên ngành', 'Năm TN'),
                                ['Bằng cấp', 'Chuyên ngành', 'Năm TN'],
                                [100, 180, 70]):
            self.trinhdo_tree.heading(col, text=text)
            self.trinhdo_tree.column(col, width=w)
        self.trinhdo_tree.pack(fill='x', pady=10)
        btn_frame_td = tk.Frame(self.tab_trinhdo, bg="#F7F7F7")
        btn_frame_td.pack(pady=2)
        tk.Button(btn_frame_td, text="Thêm", width=8, command=self.add_trinhdo, bg="#38B000", fg="white").pack(side='left', padx=3)
        tk.Button(btn_frame_td, text="Sửa", width=8, command=self.edit_trinhdo, bg="#3A86FF", fg="white").pack(side='left', padx=3)
        tk.Button(btn_frame_td, text="Xóa", width=8, command=self.delete_trinhdo, bg="#E84545", fg="white").pack(side='left', padx=3)

        # Tab điểm danh
        self.tab_diemdanh = tk.Frame(self.tabs, bg="#F7F7F7")
        self.tabs.add(self.tab_diemdanh, text="Điểm danh")
        self.diemdanh_tree = ttk.Treeview(self.tab_diemdanh, columns=('ngay', 'trang_thai'), show='headings', height=6)
        for col, text, w in zip(('ngay', 'trang_thai'), ['Ngày', 'Trạng thái'], [110, 120]):
            self.diemdanh_tree.heading(col, text=text)
            self.diemdanh_tree.column(col, width=w)
        self.diemdanh_tree.pack(fill='x', pady=10)
        tk.Button(self.tab_diemdanh, text="Cập nhật trạng thái", command=self.update_diemdanh, bg="#8D99AE", fg="white", font=("Arial", 11, 'bold')).pack(pady=5)

        # Tab chấm công lương
        self.tab_luong = tk.Frame(self.tabs, bg="#F7F7F7")
        self.tabs.add(self.tab_luong, text="Chấm công & Lương")
        self.lbl_luong = tk.Label(self.tab_luong, text="", font=('Arial', 12, "bold"), bg="#F7F7F7", fg="#2C3333")
        self.lbl_luong.pack(pady=20)

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            self.selected_emp = None
            self.show_employee_detail(None)
            return
        values = self.tree.item(selected[0], 'values')
        emp_id = values[0]
        emp = next((e for e in db['employees'] if e['id'] == emp_id), None)
        self.selected_emp = emp
        self.show_employee_detail(emp)

    def show_employee_detail(self, emp):
        if not emp:
            self.detail_widgets['lbl_info'].config(text="Chọn nhân viên để xem chi tiết")
            self.detail_widgets['lbl_info2'].config(text="")
            for tree in [self.contract_tree, self.trinhdo_tree, self.diemdanh_tree]:
                for row in tree.get_children():
                    tree.delete(row)
            self.lbl_luong.config(text="")
            return
        txt = f"Họ tên: {emp['name']}\nMã NV: {emp['id']}\nNgày sinh: {emp['dob']}\nGiới tính: {emp['gender']}\nChức vụ: {emp['position']}\nPhòng ban: {emp['dept']}\nĐịa chỉ: {emp['city']}"
        self.detail_widgets['lbl_info'].config(text=txt)
        self.detail_widgets['lbl_info2'].config(text=f"Phòng/Bộ phận: {emp['team']}\nĐơn vị: {emp['branch']}")

        # Tab hợp đồng
        for row in self.contract_tree.get_children():
            self.contract_tree.delete(row)
        for hd in get_contracts(emp['id']):
            self.contract_tree.insert('', 'end', values=(hd['số'], hd['loại'], hd['trạng_thái'], hd['ký_ngày']))
        # Tab trình độ
        for row in self.trinhdo_tree.get_children():
            self.trinhdo_tree.delete(row)
        for td in get_degrees(emp['id']):
            self.trinhdo_tree.insert('', 'end', values=(td['Bằng cấp'], td['Chuyên ngành'], td['Năm TN']))
        # Tab điểm danh
        for row in self.diemdanh_tree.get_children():
            self.diemdanh_tree.delete(row)
        diem_danh = get_attendance(emp['id'])
        for item in diem_danh:
            self.diemdanh_tree.insert('', 'end', values=(item['ngay'], item['trang_thai']))
        # Tab lương
        so_cong = sum(1 for dd in diem_danh if dd['trang_thai'].lower() == 'có mặt')
        luong_ngay = emp.get('salary_base', 0)
        tong_luong = so_cong * luong_ngay
        self.lbl_luong.config(text=f"Số ngày công: {so_cong} | Lương/ngày: {luong_ngay:,} đ\nTỔNG LƯƠNG: {tong_luong:,} đ")

    def update_diemdanh(self):
        emp = self.selected_emp
        if not emp:
            messagebox.showinfo("Chọn nhân viên", "Vui lòng chọn nhân viên trước!")
            return
        selected = self.diemdanh_tree.selection()
        if not selected:
            messagebox.showinfo("Chọn ngày", "Vui lòng chọn ngày để cập nhật trạng thái!")
            return
        idx = self.diemdanh_tree.index(selected[0])
        diem_danh = get_attendance(emp['id'])
        trang_thai_moi = simpledialog.askstring("Cập nhật", "Nhập trạng thái mới (Có mặt/Vắng/Xin nghỉ):")
        if not trang_thai_moi:
            return
        diem_danh[idx]['trang_thai'] = trang_thai_moi.strip()
        set_attendance(emp['id'], diem_danh)
        self.show_employee_detail(emp)

    def add_employee(self):
        self.show_employee_window("Thêm nhân viên")

    def edit_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn nhân viên cần sửa.")
            return
        values = self.tree.item(selected[0], 'values')
        emp_id = values[0]
        emp = next((e for e in db['employees'] if e['id'] == emp_id), None)
        self.show_employee_window("Sửa thông tin", emp)

    def delete_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Vui lòng chọn nhân viên để xóa.")
            return
        ans = messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa nhân viên này?")
        if ans:
            values = self.tree.item(selected[0], 'values')
            emp_id = values[0]
            db['employees'] = [e for e in db['employees'] if e['id'] != emp_id]
            db['contracts'] = [c for c in db['contracts'] if c['employee_id'] != emp_id]
            db['degrees'] = [d for d in db['degrees'] if d['employee_id'] != emp_id]
            db['attendance'] = [a for a in db['attendance'] if a['employee_id'] != emp_id]
            save_json(DATA_FILE, db)
            self.load_data()
            messagebox.showinfo("Đã xóa", "Đã xóa nhân viên.")

    def search_employee(self):
        kw = simpledialog.askstring("Tìm kiếm", "Nhập mã NV hoặc tên nhân viên:")
        if not kw:
            return
        kw = kw.strip().lower()
        results = [emp for emp in db['employees'] if kw in emp['id'].lower() or kw in emp['name'].lower()]
        if results:
            self.load_data(results)
        else:
            messagebox.showinfo("Không tìm thấy", "Không có nhân viên phù hợp!")

    def show_employee_window(self, title, emp=None):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("450x470")
        win.resizable(False, False)
        bgc = "#E3FDFD"
        win.configure(bg=bgc)

        fields = [
            ("Mã NV", 'id'),
            ("Họ và tên", 'name'),
            ("Ngày sinh", 'dob'),
            ("Giới tính", 'gender'),
            ("Chức vụ", 'position'),
            ("Phòng ban", 'dept'),
            ("Bộ phận", 'team'),
            ("Đơn vị", 'branch'),
            ("Quê quán", 'city'),
            ("Lương/ngày", 'salary_base'),
        ]
        vars = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(win, text=label + ":", bg=bgc, font=("Arial", 11)).place(x=25, y=20 + 37*i)
            val = str(emp[key]) if emp and key in emp else ""
            v = tk.StringVar(value=val)
            vars[key] = v
            ent = tk.Entry(win, textvariable=v, font=("Arial", 11), width=25)
            ent.place(x=155, y=20 + 37*i)
            if key == "id" and emp:
                ent.config(state="readonly")

        def submit():
            values = {key: v.get().strip() for key, v in vars.items()}
            if not all(values.values()):
                messagebox.showwarning("Thiếu thông tin", "Hãy nhập đủ các trường.")
                return
            try:
                values['salary_base'] = int(values['salary_base'])
            except:
                messagebox.showerror("Lỗi", "Lương/ngày phải là số!")
                return
            if emp:  # Sửa
                for e in db['employees']:
                    if e['id'] == emp['id']:
                        for key in vars:
                            e[key] = values[key]
                        break
            else:    # Thêm mới
                if any(e['id'] == values['id'] for e in db['employees']):
                    messagebox.showerror("Lỗi", "Mã nhân viên đã tồn tại.")
                    return
                db['employees'].append(values)
                set_contracts(values['id'], [])
                set_degrees(values['id'], [])
                diem_danh = [{'ngay': f'{str(i).zfill(2)}/06/2025', 'trang_thai': 'Có mặt'} for i in range(1, 6)]
                set_attendance(values['id'], diem_danh)
            save_json(DATA_FILE, db)
            self.load_data()
            win.destroy()

        tk.Button(win, text="Lưu", width=14, bg="#50C9CE", fg="white", font=('Arial', 12, 'bold'), command=submit).place(x=85, y=415)
        tk.Button(win, text="Hủy", width=14, bg="#E84545", fg="white", font=('Arial', 12, 'bold'), command=win.destroy).place(x=235, y=415)

    # ====== HỢP ĐỒNG ======
    def add_contract(self):
        emp = self.selected_emp
        if not emp:
            messagebox.showinfo("Thông báo", "Chọn nhân viên trước!")
            return
        self.show_contract_window(emp, "add")

    def edit_contract(self):
        emp = self.selected_emp
        if not emp:
            messagebox.showinfo("Thông báo", "Chọn nhân viên trước!")
            return
        selected = self.contract_tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Chọn hợp đồng để sửa!")
            return
        idx = self.contract_tree.index(selected[0])
        self.show_contract_window(emp, "edit", idx)

    def delete_contract(self):
        emp = self.selected_emp
        if not emp:
            messagebox.showinfo("Thông báo", "Chọn nhân viên trước!")
            return
        selected = self.contract_tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Chọn hợp đồng để xóa!")
            return
        idx = self.contract_tree.index(selected[0])
        all_contracts = get_contracts(emp['id'])
        if messagebox.askyesno("Xóa", "Bạn chắc chắn muốn xóa hợp đồng này?"):
            del all_contracts[idx]
            set_contracts(emp['id'], all_contracts)
            self.show_employee_detail(emp)

    def show_contract_window(self, emp, mode, idx=None):
        win = tk.Toplevel(self)
        win.title("Cập nhật hợp đồng")
        win.geometry("370x230")
        win.resizable(False, False)
        bgc = "#E3FDFD"
        win.configure(bg=bgc)
        fields = [
            ("Số HĐ", 'số'),
            ("Loại hợp đồng", 'loại'),
            ("Trạng thái", 'trạng_thái'),
            ("Ngày ký", 'ký_ngày'),
        ]
        vals = {k: "" for _, k in fields}
        all_contracts = get_contracts(emp['id'])
        if mode == "edit" and idx is not None and idx < len(all_contracts):
            vals = all_contracts[idx].copy()
        vars = {k: tk.StringVar(value=vals[k]) for _, k in fields}
        for i, (label, key) in enumerate(fields):
            tk.Label(win, text=label+":", bg=bgc).place(x=18, y=25+37*i)
            tk.Entry(win, textvariable=vars[key], width=26).place(x=120, y=25+37*i)
        def submit():
            data = {k: v.get().strip() for k,v in vars.items()}
            if not all(data.values()):
                messagebox.showwarning("Thiếu", "Nhập đầy đủ thông tin!")
                return
            if mode == "add":
                all_contracts.append(data)
            else:
                all_contracts[idx] = data
            set_contracts(emp['id'], all_contracts)
            self.show_employee_detail(emp)
            win.destroy()
        tk.Button(win, text="Lưu", width=10, bg="#50C9CE", fg="white", command=submit).place(x=70, y=180)
        tk.Button(win, text="Hủy", width=10, bg="#E84545", fg="white", command=win.destroy).place(x=190, y=180)

    # ====== TRÌNH ĐỘ ======
    def add_trinhdo(self):
        emp = self.selected_emp
        if not emp:
            messagebox.showinfo("Thông báo", "Chọn nhân viên trước!")
            return
        self.show_trinhdo_window(emp, "add")

    def edit_trinhdo(self):
        emp = self.selected_emp
        if not emp:
            messagebox.showinfo("Thông báo", "Chọn nhân viên trước!")
            return
        selected = self.trinhdo_tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Chọn trình độ để sửa!")
            return
        idx = self.trinhdo_tree.index(selected[0])
        self.show_trinhdo_window(emp, "edit", idx)

    def delete_trinhdo(self):
        emp = self.selected_emp
        if not emp:
            messagebox.showinfo("Thông báo", "Chọn nhân viên trước!")
            return
        selected = self.trinhdo_tree.selection()
        if not selected:
            messagebox.showinfo("Thông báo", "Chọn trình độ để xóa!")
            return
        idx = self.trinhdo_tree.index(selected[0])
        all_degrees = get_degrees(emp['id'])
        if messagebox.askyesno("Xóa", "Bạn chắc chắn muốn xóa trình độ này?"):
            del all_degrees[idx]
            set_degrees(emp['id'], all_degrees)
            self.show_employee_detail(emp)

    def show_trinhdo_window(self, emp, mode, idx=None):
        win = tk.Toplevel(self)
        win.title("Cập nhật trình độ")
        win.geometry("370x200")
        win.resizable(False, False)
        bgc = "#E3FDFD"
        win.configure(bg=bgc)
        fields = [
            ("Bằng cấp", 'Bằng cấp'),
            ("Chuyên ngành", 'Chuyên ngành'),
            ("Năm TN", 'Năm TN'),
        ]
        vals = {k: "" for _, k in fields}
        all_degrees = get_degrees(emp['id'])
        if mode == "edit" and idx is not None and idx < len(all_degrees):
            vals = all_degrees[idx].copy()
        vars = {k: tk.StringVar(value=vals[k]) for _, k in fields}
        for i, (label, key) in enumerate(fields):
            tk.Label(win, text=label+":", bg=bgc).place(x=18, y=25+37*i)
            tk.Entry(win, textvariable=vars[key], width=26).place(x=120, y=25+37*i)
        def submit():
            data = {k: v.get().strip() for k,v in vars.items()}
            if not all(data.values()):
                messagebox.showwarning("Thiếu", "Nhập đầy đủ thông tin!")
                return
            if mode == "add":
                all_degrees.append(data)
            else:
                all_degrees[idx] = data
            set_degrees(emp['id'], all_degrees)
            self.show_employee_detail(emp)
            win.destroy()
        tk.Button(win, text="Lưu", width=10, bg="#50C9CE", fg="white", command=submit).place(x=70, y=155)
        tk.Button(win, text="Hủy", width=10, bg="#E84545", fg="white", command=win.destroy).place(x=190, y=155)

if __name__ == "__main__":
    app = HRMApp()
    app.mainloop()



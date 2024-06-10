import tkinter as tk

import Computer Vision.MODEL.DepartmentMode import DepartmentModel
import DepartmentController

window = tk.Tk()
window.title("Python App")
window.geometry("600x400")


def onClick():
    print("Button Clicked here")
    name = txtA.get("1.0", "end").replace('\n','')
    numer = txtB.get("1.0", "end").replace('\n','')
    location = txtC.get("1.0", "end").replace('\n','')
    s1 = DepartmentModel(10, name, numer, location)
    DepartmentController().insertDepartment(s1)

labelA = tk.Label(text = "Dept Name: ")
labelA.place (x =5 ,y =5 ,width = 80 ,height = 30)

txtA = tk.Text()
txtA.place(x = 85 ,y =5 ,width = 100 ,height = 30)

labelB = tk.Label(text = "Dept Number: ")
labelB.place (x = 5, y =35 ,width = 80 ,height = 30)

txtB = tk.Text()
txtB.place(x = 85 ,y =35 ,width = 100 ,height = 30)


labelC = tk.Label(text = "Dept Loc: ")
labelC.place (x = 5 ,y =65 ,width = 80 ,height = 30)

txtC = tk.Text()
txtC.place(x = 85 ,y =65 ,width = 100 ,height = 30)


button = tk .Button (text = " Save ", command= onClick)
button.place (x = 5 ,y = 155 ,width =100 ,height = 50)
window.mainloop()


#cursor = conn.cursor()
#cursor.execute("INSERT INTO DEPARTMENT (IDDepartment, DepartmentName, DepartmentNumber, DepartmentLocation) VALUES (3, 'ABC', 'DEF', '12345')")
#conn.commit()
#cursor = conn.cursor()
# cursor.execute("SELECT MAX(IDDepartment) FROM DEPARTMENT")
# row = cursor.fetchone()
# while row:
#     abc = row
#     print (row[0])
#     row = cursor.fetchone()
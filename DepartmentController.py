import pyodbc


class DepartmentController:
    def __init__(self):
        self.conn = pyodbc.connect(driver='{SQL Server}', server='NGTIENDAT', database='Dept',
                                   trusted_connection='yes')

    def insertDepartment(self, objDepartment):
        print(objDepartment.DeptName, objDepartment.DeptNum, objDepartment.DeptLoc)
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(IDDepartment) FROM DEPARTMENT")
        row = cursor.fetchone()
        newIDDept = row[0] + 1
        print(newIDDept)

        SQLCMD = "INSERT INTO DEPARTMENT VALUES (?, ?, ?, ?)"

        cursor = self.conn.cursor()
        cursor.execute(SQLCMD, newIDDept, objDepartment.DeptName, objDepartment.DeptNum, objDepartment.DeptLoc)
        self.conn.commit()

import mysql.connector# requires  mysql-connector-python module
import xlrd#requires xlrd module
def excelfn(location,query):
    conn=mysql.connector.connect(host="localhost",user="root",passwd="PWD123",database="csr")
    cursor=conn.cursor()
    fh=xlrd.open_workbook(location) #open excel file
    sheet=fh.sheet_by_index(0)
    sheet.cell_value(0,0)
    qset=[]
    for i in range(1,110):
        qset.append(tuple(sheet.row_values(i)))
    cursor.executemany(query,qset)
    conn.commit()
    conn.close()#closing connection
    

#connectfn(".\\DummyCOMPANIES.xlsx","insert into maincsr_companytable(id,company_name,no_of_employees,phone,email,address,description,activity_status,total_amount_donated,cap_available)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
#connectfn(".\\DummyNGOs.xlsx","insert into maincsr_ngotable(id,ngo_name,no_of_employees,phone,email,address,description,activity_status,total_recd,min_cap_reqd)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
connectfn(".\\DummyNGOs.xlsx","insert into maincsr_ngotable(id,regis_num,state,district,ngo_name,no_of_employees,phone,email,address,description,activity_status,total_recd,min_cap_reqd,sectors)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
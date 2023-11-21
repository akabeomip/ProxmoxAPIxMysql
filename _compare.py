import pymysql

def copy_tables(source_config, destination_config, source_table, destination_table):
    # Kết nối đến cơ sở dữ liệu nguồn
    source_conn = pymysql.connect(**source_config)
    source_cursor = source_conn.cursor()

    # Kết nối đến cơ sở dữ liệu đích
    destination_conn = pymysql.connect(**destination_config)
    destination_cursor = destination_conn.cursor()

    try:
        # Truy vấn dữ liệu từ bảng nguồn
        source_cursor.execute(f"SELECT * FROM {source_table}")
        data = source_cursor.fetchall()
        column_names = [column[0] for column in source_cursor.description]
        # Tạo bảng đích (nếu chưa tồn tại)
        #destination_cursor.execute(f"CREATE TABLE IF NOT EXISTS {destination_table} LIKE {source_table}")

        # Chèn dữ liệu vào bảng đích
        for row in data:
            row_dict = dict(zip(column_names, row))
            placeholders = ', '.join(['%s'] * len(row_dict))
            columns = ', '.join(row_dict.keys())
            values = tuple(row_dict.values())
            query = f"INSERT INTO {destination_table} ({columns}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE"
            update_clause = ', '.join([f"{column} = VALUES({column})" for column in row_dict.keys()])
            query += f" {update_clause}"
            #destination_cursor.execute(f"INSERT INTO {destination_table} VALUES {row} ON DUPLICATE KEY UPDATE")
            destination_cursor.execute(query, values)

        # Commit các thay đổi vào cơ sở dữ liệu đích
        destination_conn.commit()

        print("Copy bảng thành công.")
    except Exception as e:
        print(f"Lỗi khi copy bảng: {str(e)}")
        destination_conn.rollback()
    finally:
        # Đóng kết nối
        source_cursor.close()
        source_conn.close()
        destination_cursor.close()
        destination_conn.close()

def compare_mysql_tables(connection1, table1, connection2, table2):
    # Kết nối đến cơ sở dữ liệu 1
    conn1 = pymysql.connect(**connection1)
    cursor1 = conn1.cursor()

    # Kết nối đến cơ sở dữ liệu 2
    conn2 = pymysql.connect(**connection2)
    cursor2 = conn2.cursor()

    # Truy vấn dữ liệu từ bảng 1
    cursor1.execute(f"SELECT * FROM {table1}")
    data1 = cursor1.fetchall()

    # Truy vấn dữ liệu từ bảng 2
    cursor2.execute(f"SELECT * FROM {table2}")
    data2 = cursor2.fetchall()

    # So sánh dữ liệu
    try:
        if data1 == data2:
            print("Hai bảng giống nhau.")
        else:
            copy_tables(connection1, table1, connection2, table2)
        print("Kiểm tra hoàn thành.")
    except Exception as e:
        print(f"Lỗi khi kiểm tra bảng: {str(e)}")
    finally:
        # Đóng kết nối
        cursor1.close()
        conn1.close()
        cursor2.close()
        conn2.close()

def compare_databases(source_config, destination_config):
    # Kết nối đến cơ sở dữ liệu nguồn
    source_conn = pymysql.connect(**source_config)
    source_cursor = source_conn.cursor()

    # Kết nối đến cơ sở dữ liệu đích
    destination_conn = pymysql.connect(**destination_config)
    destination_cursor = destination_conn.cursor()

    try:
        # Lấy danh sách tất cả các bảng từ cơ sở dữ liệu nguồn
        source_cursor.execute("SHOW TABLES")
        source_tables = source_cursor.fetchall()

        # Lấy danh sách tất cả các bảng từ cơ sở dữ liệu đích
        destination_cursor.execute("SHOW TABLES")
        destination_tables = destination_cursor.fetchall()

        # Kiểm tra sự khác biệt giữa các bảng
        for source_table in source_tables:
            if source_table not in destination_tables:
                print(f"Bảng {source_table} không tồn tại trong cơ sở dữ liệu đích.")
            else:
                # # Lấy thông tin cấu trúc bảng từ cơ sở dữ liệu nguồn
                # source_cursor.execute(f"SHOW CREATE TABLE {source_table}")
                # source_table_structure = source_cursor.fetchone()[1]
                
                # # Lấy thông tin cấu trúc bảng từ cơ sở dữ liệu đích
                # destination_cursor.execute(f"SHOW CREATE TABLE {source_table}")
                # destination_table_structure = destination_cursor.fetchone()[1]
                copy_tables(source_config, destination_config, source_table[0], source_table[0])

                # # So sánh cấu trúc của hai bảng
                # if source_table_structure != destination_table_structure:
                #     print(f"Cấu trúc của bảng {source_table} khác nhau giữa hai cơ sở dữ liệu.")

        print("Kiểm tra hoàn thành.")
    except Exception as e:
        print(f"Lỗi khi kiểm tra: {str(e)}")
    finally:
        # Đóng kết nối
        source_cursor.close()
        source_conn.close()
        destination_cursor.close()
        destination_conn.close()


# Thông tin kết nối cơ sở dữ liệu
# connection1 = {
#     'host': '10.1.9.200',
#     'user': 'lechidai',
#     'password': 'Admin@123',
#     'database': 'proxmoxapi'
# }

# connection2 = {
#     'host': '10.1.9.200',
#     'user': 'lechidai',
#     'password': 'Admin@123',
#     'database': 'proxmoxapinew'
# }

# So sánh bảng
# compare_mysql_tables(connection1, table1, connection2, table2)
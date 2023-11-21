import mysql.connector
import json

def connect():
    connection = mysql.connector.connect(
        host="10.1.9.200",
        user="lechidai",
        password="Admin@123",
        database="proxmoxapinew"
    )
    return connection

def VMs(data):
    connection = connect() 
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO VMs (VMID, PoolID, NodeID, Hostname, IP, NumberOfDisks, OSName, Version, Status, CPUs, DiskMemory, RAM)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    VMID = VALUES(VMID),
    PoolID = VALUES(PoolID),
    NodeID = VALUES(NodeID),
    Hostname = VALUES(Hostname),
    IP = VALUES(IP),
    NumberOfDisks = VALUES(NumberOfDisks),
    OSName = VALUES(OSName),
    Version = VALUES(Version),
    Status = VALUES(Status),
    CPUs = VALUES(CPUs),
    DiskMemory = VALUES(DiskMemory),
    RAM = VALUES(RAM)
"""
    if data['IP'] == None:
        data
    values = (
        data['VMID'],
        data['PoolID'],
        data['NodeID'],
        data['Hostname'],
        json.dumps(data['IP']),  # Chuyển đổi mảng IP thành chuỗi JSON
        data['NumberOfDisks'],
        data['OSName'],
        data['Version'],
        data['Status'],
        data['CPUs'],
        data['DiskMemory(GB)'],
        data['RAM(GB)']
    )
    cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()

def Pools(data):
    connection = connect()

# Tạo đối tượng cursor
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO Pools (PoolID, NumberOfVMs, NumberOfStorages)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
    PoolID = VALUES(PoolID),
    NumberOfVMs = VALUES(NumberOfVMs),
    NumberOfStorages = VALUES(NumberOfStorages)
"""
    values = (
        data['PoolID'],
        data['NumberOfVMs'],
        data['NumberOfStorages']
    )
    cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()

def Nodes(data):
    connection = connect()
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO Nodes (NodeID, CountVMs, CountStorages, ClusterID, Status)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    NodeID = VALUES(NodeID),
    CountVMs = VALUES(CountVMs),
    CountStorages = VALUES(CountStorages),
    ClusterID = VALUES(ClusterID),
    Status = VALUES(Status)
"""
    values = (
        data['NodeID'],
        data['CountVMs'],
        data['CountStorages'],                                                              
        data['ClusterID'],
        data['Status']
    )
    cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()

def Disks(data):
    connection = connect()
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO Disks (VMID, DiskName, StorageID, Capacity)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    VMID = VALUES(VMID),
    DiskName = VALUES(DiskName),
    StorageID = VALUES(StorageID),
    Capacity = VALUES(Capacity)
"""
    values = (
        data['VMID'],
        data['DiskName'],
        data['StorageID'],
        data['Capacity']
    )
    cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()

def Storages(data):
    connection = connect()
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO Storages (StorageID, StorageCapacity, AvailableCapacity, Type, Status, NodeID)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    StorageID = VALUES(StorageID),
    StorageCapacity = VALUES(StorageCapacity),
    AvailableCapacity = VALUES(AvailableCapacity),
    Type = VALUES(Type),
    Status = VALUES(Status),
    NodeID = VALUES(NodeID)
"""
    values = (
        data['StorageID'],
        data['Storage Capacity (GB)'],
        data['Available Capacity (GB)'],
        data['Type'],
        data['Status'],
        data['NodeID']
    )
    cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()

def Clusters(data):
    connection = connect()
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO Clusters (ClusterID, CountNode)
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE
    ClusterID = VALUES(ClusterID),
    CountNode = VALUES(CountNode)
"""
    values = (
        data['ClusterID'],
        data['CountNode']
    )
    cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()

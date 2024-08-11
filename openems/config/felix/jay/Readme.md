### After all pre-defined configuration, these are configuration changes:
## Edge Felix Configuration Changes (localhost 8080):
#### 1) Set up the Modbus TCP Protocol which is receiving the data through Pymodbus.
   
![image](https://github.com/user-attachments/assets/b94bc015-40c2-4e44-b7e7-4b7d75c2b090)

#### 2) Create a meter for Production will receive the Power values from PyModbus

![image](https://github.com/user-attachments/assets/87b76e3e-e605-4070-9f10-0ddd11ad68c1)

#### 3) Create a meter for Consumption will receive the Power values from PyModbus 

![image](https://github.com/user-attachments/assets/b98c39d0-344a-42b8-9da5-b267ace3a48d)

#### 4) Create a separate storage system which will receive the Active Power and Soc from PyModbus through the above Modbus. 

![image](https://github.com/user-attachments/assets/4f06f347-ace5-44f7-8b1a-2b013689da8b)

#### 5) This is configured to display the meter "storage_system_1" in the Storage System section in OpenEMS UI

![image](https://github.com/user-attachments/assets/fbedf152-dd6b-4296-9250-dc945d335ef2)

#### 6) Set up the InfuxDB to store data and display the history graphs.
#### i) Create a database named db to store OpenEMS Edge UI data.
#### ii) And run it at port 8086. 

![image](https://github.com/user-attachments/assets/784c278f-ec17-4ab4-a12f-0f476da2e0a4)

## Backend Felix Configuration Changes (localhost 8079):

#### 1)  Set up the InfuxDB to store data and display the history graphs.
#### i) Create a separate database named db1 to store OpenEMS Backend data.
#### ii) And run it at port 8086. 

![image](https://github.com/user-attachments/assets/038665bf-6162-424b-b854-fa87c48ae657)

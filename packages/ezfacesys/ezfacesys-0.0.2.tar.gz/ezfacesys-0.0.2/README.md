### 软件安装

```
pip install ezfacesys
```

### 功能

1. 人脸录入
   打开摄像头后英文输入法输入s多保存几张图片，空格退出
   文件格式要求

   ```
   id.name.jpg
   例如：
   1.Tom.jpg
   ```
   ```
   例：
   from ezfacesys.face_save import entering_face
   path = 'G:\\img\\'
   name = 'jom'
   entering_face(path, name)
   # s保存图片，空格退出
   ```

2. 数据训练

   drill函数

   ```
   参数两个：
   第一个是保存的的图片的跟目录，第二个参数是数据训练集的文件的报错位置（.yml后缀）
   ```
   ```
   例：
   from ezfacesys.drill_data import drill
   path = 'G:\\img\\'
   path2 = 'G:\\img\\trainer\\trainer1.yml'
   cate_path = r'D:\openCV\opencv\sources\data\haarcascades\haarcascade_frontalface_alt2.xml'
   drill(path, cate_path, path2)
   ```
   

3. 人脸识别
   空格退出
   recognition函数
   
   ```
   参数两个：
   第一个是保存的的图片的跟目录，第二个参数是数据训练集的文件的路径
   
   ```
   ```
   例：
   from ezfacesys.face_recognition import recognition
   path = 'G:\\img\\'
   path2 = 'G:\\img\\trainer\\trainer1.yml'
   recognition(path, path2)
   ```

   
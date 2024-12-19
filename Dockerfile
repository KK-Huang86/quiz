# 使用官方的 Python 映像作為基礎映像
FROM python:latest

# 設置工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝依賴
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製所有源代碼到容器內
COPY . .



# 執行 Django 應用
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
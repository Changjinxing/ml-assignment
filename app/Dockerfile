# 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制应用程序代码到容器中
COPY . .

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 启动应用程序
CMD ["python", "translation_service.py"]

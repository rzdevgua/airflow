import sys

print(sys.executable)

# import site
# import os

# # 获取所有的 site-packages 路径
# site_packages = site.getsitepackages()

# for path in site_packages:
#     airflow_path = os.path.join(path, 'airflow')
#     if os.path.exists(airflow_path):
#         print(airflow_path)
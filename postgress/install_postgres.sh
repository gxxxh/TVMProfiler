# 权限问题时，添加用于进docker用户组
 sudo gpasswd -a $USER docker
# 切换当前用户所属用户组
newgrp docker

# 创建镜像
docker build -t postgres-db-gh ./

# 运行
docker run -d --name postgres-db-gh -p 5432:5432 postgres-db-gh
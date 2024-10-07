# 服务器npm部署北冥坞系统

**连接服务器**
```
ssh -Y dachuang@xxx.xxx.xxx.90
curl -I www.google.com  # 测试网络连接
```

**创建新的git分支**
```
git branch docker
git checkout docker     # 切换到docker分支
```

**将之前对git仓库的修改提交到docker分支**
```
git add .
git commit -m "尝试docker部署方案"
```

**切换回main分支**
```
git checkout main
```

**卸载容器**
```
docker ps   # 查看容器运行状态
sudo docker compose -f docker-compose.yaml -p learnwaresingle down
docker ps   # 再次查看容器运行状态
```

**设置git仓库忽略 deploy/docker-compose/Learnware/Learnware/目录**
```
(base) git rm -r --cached deploy/docker-compose/Learnware/Learnware
(base) vim .gitignore

/deploy/docker-compose/Learnware/Learnware/     # 忽略该目录

(base) git status
(base) git add .gitignore
(base) git commit -m "update .gitignore to ignore deploy/docker-compose/Learnware/"
```

**设置前端访问本机的后端**
```
(base) vim frontend/packages/main/.env

#VITE_BACKEND_URL=
#VITE_BACKEND_URL='http://114.213.205.90:8088'
VITE_BACKEND_URL='http://114.213.205.90:8081'       #8088端口没有对外开放，改为使用8081端口！

(base) vim frontend/packages/admin/.env

VITE_BACKEND_URL='http://114.213.205.90:8081'
```

**安装Python依赖**
```
pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**设置后端admin用户的密码**
```
(base) vim backend/database/sqlalchmy.py

class SQLAlchemy(Database):
    DATASET_INIT_DATA = [
        # "INSERT INTO tb_user (username, nickname, email, password, role, register, email_confirm_time) VALUES ('admin',  'adminitrator', 'admin@localhost', :admin_password, 2, :now, :now)",
        "INSERT INTO tb_user (username, nickname, email, password, role, register, email_confirm_time) VALUES ('admin',  'adminitrator', 'admin@localhost', '12345678', 2, :now, :now)",
        "INSERT INTO tb_user (username, nickname, email, password, role, register, email_confirm_time) VALUES ('lzy',  'adminitrator', '1571547820@qq.com', '12345678', 2, :now, :now)",
        "INSERT INTO tb_user (username, nickname, email, password, role, register, email_confirm_time) VALUES ('mmy',  'adminitrator', '3428585219@qq.com', '12345678', 2, :now, :now)",
        "INSERT INTO tb_user (username, nickname, email, password, role, register, email_confirm_time) VALUES ('wmx',  'adminitrator', '1224659817@qq.com', '12345678', 2, :now, :now)",
        "INSERT INTO tb_user (username, nickname, email, password, role, register, email_confirm_time) VALUES ('cry',  'adminitrator', '1928407107@qq.com', '12345678', 2, :now, :now)",
        "INSERT INTO tb_user (username, nickname, email, password, role, register, email_confirm_time) VALUES ('lt',  'adminitrator', '2084694891@qq.com', '12345678', 2, :now, :now)",
        "INSERT INTO tb_user (username, nickname, email, password, role, register, email_confirm_time) VALUES ('whd',  'adminitrator', '852669612@qq.com', '12345678', 2, :now, :now)",
        "INSERT INTO tb_user (username, nickname, email, password, role, register, email_confirm_time) VALUES ('ljp',  'adminitrator', '2315787362@qq.com', '12345678', 2, :now, :now)",
        "INSERT INTO tb_global_counter (name, value) VALUES ('learnware_id', 0)",
    ]

(base) git add backend/database/sqlalchmy.py
(base) git commit -m "change backend/database/sqlalchemy.py to set the init user"
```

**安装redis**
```
(base) sudo apt upgrade
(base) sudo apt update
(base) sudo apt install redis-server
(base) sudo vim /etc/redis/redis.conf

supervised systemd

(base) sudo systemctl start redis.service
Job for redis-server.service failed because the control process exited with error code.
See "systemctl status redis-server.service" and "journalctl -xeu redis-server.service" for details.

(base) sudo redis-server /etc/redis/redis.conf
(base) redis-cli
```

**启动后端**
```
(base) dachuang@master:~/Beimingwu$ cd backend/
(base) dachuang@master:~/Beimingwu/backend$ PYTHONPATH=. python scripts/main.py &
/home/dachuang/anaconda3/lib/python3.12/site-packages/transformers/utils/generic.py:441: FutureWarning: `torch.utils._pytree._register_pytree_node` is deprecated. Please use `torch.utils._pytree.register_pytree_node` instead.
  _torch_pytree._register_pytree_node(
[WARNING] - 2024-10-06 18:16:51,804 - __init__.py - hetero_map_table_organizer - No market mapping to reload!
Downloading tokenizer_config.json: 100%|████████| 48.0/48.0 [00:00<00:00, 142kB/s]
Downloading vocab.txt: 100%|████████████████████| 232k/232k [00:00<00:00, 335kB/s]
Downloading tokenizer.json: 100%|███████████████| 466k/466k [00:00<00:00, 823kB/s]
Downloading config.json: 100%|███████████████████| 570/570 [00:00<00:00, 2.73MB/s]
/home/dachuang/anaconda3/lib/python3.12/site-packages/torch/nn/modules/transformer.py:307: UserWarning: enable_nested_tensor is True, but self.use_nested_tensor is False because encoder_layer was not TransformerEncoderLayer
  warnings.warn(f"enable_nested_tensor is True, but self.use_nested_tensor is False because {why_not_sparsity_fast_path}")
 * Serving Flask app 'main'
 * Debug mode: on
```

**安装npm和pnpm包管理器**
```
sudo apt install npm
npm -v
npm config set registry https://registry.npmmirror.com/
cd frontend/
sudo npm cache clean -f
npm config set registry https://registry.npm.taobao.org
npm config get registry
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
npm config set proxy http://127.0.0.1:7890
npm config set https-proxy http://127.0.0.1:7890
sudo npm i -g pnpm
pnpm i
```

**安装zellij**
```
curl -L https://github.com/zellij-org/zellij/releases/download/v0.37.1/zellij-x86_64-unknown-linux-musl.tar.gz -o zellij.tar.gz
tar -xf zellij.tar.gz
sudo mv zellij /usr/local/bin/
zellij --version
```

**启动前端**
```
zellij       # 启动zellij，并打开两个不同的终端，分别运行以下命令
pnpm dev:main 
pnpm dev:admin 
```

**修改后端CORS代码**
```
(base) vim scripts/main.py

# CORS(app)

# CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "Content-Type,Authorization", "methods": ["GET", "POST", "OPTIONS"]}})    # add this

CORS(app, resources={
    r"/*": {
        "origins": ["http://114.213.205.90:5173","http://114.213.205.90:5174"],  # 指定允许
的来源
        "allow_headers": ["Content-Type", "Authorization"],  # 允许的请求头
        "methods": ["GET", "POST", "OPTIONS"],  # 允许的请求方法
        "supports_credentials": True  # 允许带凭证的跨域请求（如 cookies）
    }
})
```

**删除掉密码验证相关代码**
```
(base) vim restful/auth.py

        if user is None:
            result["code"] = 51
            result["msg"] = "Account not exist."
            pass
        elif user["email_confirm_time"] is None:
            result["code"] = 54
            result["msg"] = "Email not verified."
            pass
        #elif not flask_bcrypt.check_password_hash(user["password"], password):
        #    result["code"] = 52
        #    result["msg"] = "Incorrect password."
```

**重新启动后端**
```
cd backend/
sudo kill -9 $(sudo lsof -t -i:8081)     # 关闭之前的后端进程
find . -name "__pycache__" -type d -exec rm -r {} + # 清除缓存
PYTHONPATH=. python scripts/main.py &
```

**本机终端测试后端能否成功登录**
*以下代码需在本机终端运行*
```
➜  ~ curl -I http://114.213.205.90:8081/auth/login
HTTP/1.1 405 METHOD NOT ALLOWED
Content-Length: 70
Access-Control-Allow-Origin: *
Allow: OPTIONS, POST
Connection: keep-alive
Content-Type: application/json
Date: Sun, 06 Oct 2024 12:58:25 GMT
Keep-Alive: timeout=4
Proxy-Connection: keep-alive
Server: Werkzeug/3.0.3 Python/3.12.4

➜  ~ curl -X POST http://114.213.205.90:8081/auth/login -H "Content-Type: application/json" -d '{"email": "admin@localhost", "password": "12345678"}'
{
    "code": 0,
    "msg": "Login success.",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyODIyMTk4MiwianRpIjoiZjIyYjg2N2ItNjM3Ny00OGZjLWFkMDktMmE3MDQwMThiOGFhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzI4MjIxOTgyLCJjc3JmIjoiMGZkNDcxYmQtMDVjZC00ZTZkLWExZmItMmQ3MTIyMGMwM2Q2IiwiZXhwIjoxNzI4MzA4MzgyfQ.TpjAtOkjE7TtF-zvWSvftW1BDb8CNevYuetEMBKrkNA"
    }
}
```

**测试前端登录功能**
前端不需要专门重启，直接刷新页面测试即可。
确定能重新登录后，直接关掉zellij窗口即可，前端和后端进程都不会因此关闭（只要不主动杀进程或者ctrl+c退出，进程都会保持运行）。




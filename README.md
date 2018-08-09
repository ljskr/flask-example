# flask-example

## 1. 结构说明
目录层次：
```
.
├── config.py               # 项目环境变量配置文件
├── gulpfile.js             # gulp 配置文件
├── log                     # log 保存路径
├── log.conf                # log 配置文件
├── package.json            # gulp所依赖的npm包
├── README.md
├── requirements.txt        # 项目所依赖的python包
├── run.py                  # 主运行文件    (开发模式)
├── run.uwsgi.ini           # 主运行配置文件 (生产模式)
└── webapp
    ├── __init__.py         # 创建flask app，注册module
    ├── core                # module1（示例）
    │   └── __init__.py
    ├── main                # module2（示例）
    │   ├── __init__.py
    │   └── views.py
    ├── static              # 静态资源目录
    │   ├── favicon.ico
    │   ├── css             # 自己的css文件(按模块设立子文件夹)
    │   ├── img
    │   ├── js              # 自己的js文件(按模块设立子文件夹)
    │   └── lib             # 所有第三方库存放路径(js/css)
    └── templates           # 模板目录(按模块设立子文件夹)
```

`gulpfile.js` 和 `package.json` 是与打包发布有关的配置文件。使用 gulp 对css、js文件进行压缩、添加hash值等。需要安装 npm 和 gulp。使用参见生产打包一节。

## 2. 准备工作

由于是python项目，相应的python依赖包需要先行安装。

运行以下命令进行项目依赖包安装：
```
pip install -r requirements.txt
```

若需要打包发布，对css、js等静态资源进行压缩、添加hash值等，则额外需要安装 node.js 和 gulp 。参见生产打包一节。

## 3. 日常开发

对于日常开发，仅需要运行以下命令即可：
```
python run.py
```

web 所监听的 host 和 port 由 `config.py` 文件中指定，log 输出由 `log.conf` 配置文件指定。按需修改即可。

每个 flask 的模块 (blueprint) 创建一个文件夹，在 `__init__.py` 中实现 module_init 函数，进行对 blueprint 的注册（参见示例中的例子）。文件夹内至少分 **views.py** 和 **model.py**。 views 定义视图和路由， model 定义模型。

静态资源统一放在 `static` 目录下，其中 `lib` 存放第三方库，自己的 css、js 则存放在 css、js 目录下，并且最好是按模块设立子文件夹存放。

模板目录统一放在 `templates` 目录下，最好也是按模块设立子文件夹。

## 4. 生产环境运行

官方不建议在生产环境中直接使用 app.run() 的方式运行。这里使用了 **uwsgi + nginx** 的方式进行部署。

### 4.1 配置文件修改

配置信息一般由根目录下的 `config.py` 文件进行配置。如果要对生产环境的配置进行修改，可以有三种方式：

* 直接修改 `config.py` 。
* 在根目录中创建一个 `instance` 目录，目录中创建一个 `config.py` 配置文件，把需要修改的变量定义在这个配置文件中。
* 运行之前定义一个环境变量 `APP_CONFIG_FILE`，该环境变量指定一个配置文件路径，把需要修改的变量定义在这个配置文件中。

建议使用第二或第三种方式。

### 4.2 uwsgi

`uwsgi` 在 `requirements.txt` 中已经声明，所以可以直接使用。运行方式如下：

```
sudo uwsgi --ini run.uwsgi.ini
```

`run.uwsgi.ini` 配置文件中的内容可根据官方说明进行修改。这里配置了以 www-data 用户运行，所以请务必**确保 www-data 用户对 log 目录有读写权限**，否则可能会启动失败。

### 4.3 nginx

nginx 的安装使用不在本教程中。这里只提一下需要对 nginx 做的配置。

在 nginx 中增加如下配置：
```
server {
    # 监听端口
    listen 80;

    server_name _;
    # 若只允许特定的域名访问，则使用下面的 server_name 设置
    #server_name mydomain.com;
    #server_name mydomain1.com mydomain2.com;

    # 让 nginx 处理静态资源
    location /static/ {
        # 这里配置 webapp 目录的绝对路径
        alias /path/to/application/webapp/static;
    }

    location /favicon.ico {
        # 这里配置 webapp 目录的绝对路径
        root /path/to/application/webapp/static;
    }

    # 代理转发
    location / {
        include uwsgi_params;
        # 此处的 socket 路径需要跟 uwsgi 中定义的一致
        uwsgi_pass unix:///tmp/web-flask-example.socket;
        # uwsgi_pass 127.0.0.1:8080;
    }
}
```
**注意**： fedora 之类的发行版可能会限制 socket 文件的访问，导致 nginx 无法读取 /tmp/*.socket 文件。症状表现为返回 502 错误，error 日志中报找不到文件错误。若需要解决该问题，其中一个方法是设置 selinux ，另一个方法就是不使用 socket 进行通信，改为使用端口监听。

## 5. 静态资源压缩发布（生产打包，高级，选做）

一般生产发布的工程，都需要对 css、js 进行压缩、添加 hash 值等，节省带宽，提高加载速度，避免不正确的浏览器缓存。

这里使用 gulp 工具对静态资源进行预处理。 gulp 是 node.js 中的工具，使用之前先安装 node.js 和 npm 。

npm 的项目依赖定义在 `package.json` 文件中。所以可以在项目根目录中执行如下命令，安装 gulp 工具及相关依赖：

```
npm install
```

安装完毕后，使用 gulp 命令进行静态资源预处理：
```
gulp
```

gulp 的任务定义在 `gulpfile.js` 文件中。

这里把 css、js 处理后生成的文件存放在 `webapp/static/dist/` 文件夹下，把 templates 处理后生成的文件存放在 `webapp/templates_dist/` 文件夹下。

应用时，直接修改 `config.py` 配置中的 `TEMPLATE_FOLDER` ：
```
# 模板目录名
TEMPLATE_FOLDER = "templates"

改为 ->
# 模板目录名
TEMPLATE_FOLDER = "templates_dist"
``` 

然后再启动项目即可。

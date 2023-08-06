# django专用的超轻量级消息队列 django_task_mq
---------
## 功能：  
    broker,消费端,生产端,先进先出,topic，优先级等
## 原理：  
  - 使用orm作用在django数据库内，形成先进先出表，生产者插入内容，消费者读取内容
## 优点：
  - 可支持多消费进程，使用简单，无需其他第三方依赖
## 使用流程：

  #### 初始化
  - 在你的app目录下，新建任意名称py文件
  - 在文件导入并使用 mq_init 函数，如文件示例：
  ```
import os
from django_task_mq import mq_init
mq_init(os.path.dirname(os.path.abspath(__file__)))
  ```
  - 运行后会自动生成消息队列数据表，之后请清空该文件内容。
  - 请手动执行命令 python(3) manage.py makemigrations
  - 请手动执行命令 python(3) manage.py migrate 来同步数据库
  #### 设置生产者
  - 在任意views.py文件中导入并调用 mq_producer() 即可新增生产者，插入消息。
  - （注意，DB_django_task_mq为默认的消息表，请提前导入后使用）
  - 文件示例
  ```
from django_task_mq import mq_producer
mq_producer(DB_django_task_mq,topic='',message={})
  ```
  #### 新增消费者
  - 在一开始创建的py文件中导入并调用 mq_consumer 函数
  - 文件示例: （请复制文件示例使用，其中第三行需要手写settings.py父文件夹名称，MyApp请替换为您的app名称，play函数请替换成您的运行消费业务的函数）
  ```
import os,sys,django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings'%'') # 引号中请输入您的setting父级目录名
django.setup()
from MyApp.models import DB_django_task_mq
from django_task_mq import mq_consumer
from MyApp.views import play
mq_consumer(DB_django_task_mq,play,topic='')
  ```
  - 用python(3)命令来直接启动该文件，即可新增一个消费者进程。
  - 建议使用 nohup python(3) 文件.py 命令来后台启动。
  
## 第三方依赖包:  
  暂无

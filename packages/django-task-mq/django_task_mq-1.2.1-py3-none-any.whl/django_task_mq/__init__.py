import os,time,json

def mq_init(base_url):
    file_path = os.path.join(base_url,'models.py')
    fp = open(file_path,'r',encoding='utf-8')
    if 'DB_django_task_mq' in fp.read():
        print('Please don`t repeat this,or you can delete "class DB_django_task_mq" from "models.py",then do this again!')
        fp.close()
    else:
        fp = open(file_path,'a+')
        fp.writelines(['\n'*4,'class DB_django_task_mq(models.Model):','\n    topic = models.CharField(max_length=100,null=True,blank=True,default="")',
                       '\n    message = models.TextField(default="{}")','\n    status = models.BooleanField(default=True)','\n    task_id = models.CharField(max_length=100,null=True,blank=True,default="")','\n    def __str__(self):','\n        return self.topic'])
        fp.close()
        file_path = os.path.join(base_url,'admin.py')
        fp = open(file_path,'a+')
        fp.writelines(['\n'*4,'admin.site.register(DB_django_task_mq)'])
        fp.close()
        time.sleep(0.5)

def mq_producer(DB_django_task_mq,topic,message):
    mq = DB_django_task_mq.objects.create(topic=topic,message=json.dumps(message))
    return mq.id

def mq_consumer(DB_django_task_mq,fun,topic):
    while True:
        time.sleep(1)
        mq = DB_django_task_mq.objects.filter(status=True,topic=topic).first()
        if mq:
            print('\n[BEGIN]:',mq.id,mq.topic)
            mq.status = False
            mq.save()
            try:
                fun(mq.message)
            except Exception as e:
                print('[ERROR]:',e)
            finally:
                mq.delete()
                print('[OVER]')
        else:pass
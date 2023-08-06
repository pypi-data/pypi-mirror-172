# pywong

#### 介绍
Python工具,封装常用操作.

#### 安装教程

1.  pip安装
    ```python
    pip install pywong
    pip install pywong==1.1.1
    ```

#### 使用说明

1.  db操作示例
    
    - mysql:
    ```python
    from pywong.db.mysql.settings import DEFAULT, DATABASES
    from pywong.db.mysql.utils import DbHelper
    
    
    def run():
        """run方法"""
        DEFAULT['host'] = '127.0.0.1'
        DEFAULT['password'] = '123456'
    
        DATABASES['default_database'] = 'demo'
    
        db_help = DbHelper(host=DEFAULT['host'], user=DEFAULT['user'], password=DEFAULT['password'],
                           port=DEFAULT['port'], database=DATABASES['default_database'])
    
        sql = 'SELECT * FROM sys_user'
        print(db_help.execute(sql))
    
    
    if __name__ == "__main__":
        """main方法"""
        run()
    
    输出：
    [{'id': 1, 'dept_id': 4, 'status': None, 'remark': None}]
    ```
    - postgresql:
    ```python
    from pywong.db.postgresql.settings import DEFAULT, DATABASES
    from pywong.db.postgresql.utils import DbHelper
    
    
    def run():
        """run方法"""
        DEFAULT['host'] = '127.0.0.1'
        DEFAULT['password'] = '123456'
    
        DATABASES['default_database'] = 'demo'
    
        db_help = DbHelper(host=DEFAULT['host'], user=DEFAULT['user'], password=DEFAULT['password'],
                           port=DEFAULT['port'], database=DATABASES['default_database'])
    
        sql = 'SELECT * FROM sys_user'
        print(db_help.execute(sql))
    
    
    if __name__ == "__main__":
        """main方法"""
        run()
    
    输出：
    [{'id': 1, 'dept_id': 4, 'status': None, 'remark': None}]
    ```
    - mssql:
    ```python
    from pywong.db.mssql.settings import DEFAULT, DATABASES
    from pywong.db.mssql.utils import DbHelper
    
    
    def run():
        """run方法"""
        DEFAULT['server'] = '127.0.0.1'
        DEFAULT['password'] = '123456'
    
        DATABASES['default_database'] = 'demo'
    
        db_help = DbHelper(server=DEFAULT['server'], user=DEFAULT['user'], password=DEFAULT['password'],
                       port=DEFAULT['port'], database=DATABASES['default_database'])
    
        sql = 'SELECT * FROM sys_user'
        print(db_help.execute(sql))
    
    
    if __name__ == "__main__":
        """main方法"""
        run()
    
    输出：
    [{'id': 1, 'dept_id': 4, 'status': None, 'remark': None}]
    ```
    - 快捷操作:
    ```python
    from pywong.db.mysql.settings import DEFAULT, DATABASES
    from pywong.app.db_tools import get_db_helper
    from pywong.db.settings import DATABASE_TYPE
    
    
    def run():
        """run方法"""
        DEFAULT['host'] = '127.0.0.1'
        DEFAULT['password'] = '123456'
    
        DATABASES['default_database'] = 'demo'
    
        mysql_helper, _, _ = get_db_helper(DATABASE_TYPE.MYSQL)
    
        sql = 'SELECT * FROM sys_user'
    
        print(mysql_helper.execute(sql))


    if __name__ == "__main__":
        """main方法"""
        run()
    
    输出：
    [{'id': 1, 'dept_id': 4, 'status': None, 'remark': None}]
    ```
2.  资源监测示例
    ```python
    from pywong.monitor.resource_monitor import Resource
    import time
    
    
    def run():
        """run方法"""
        system_monitor = Resource()
        while True:
            time.sleep(2)
            print(system_monitor.memory)
            print(system_monitor.cpu)
            print(system_monitor.hard_disk)
    
    
    if __name__ == '__main__':
        """main方法"""
        run()
    
    输出：
    Memory usage rate: 54.2%
    CPU usage rate: 0.0%
    HardDisk C:\ usage rate: 38.5%
    HardDisk D:\ usage rate: 9.4%
    ```
3.  ml及异常值检测示例
    
    - KNNClassifier:
    ```python
    from pywong.ml.sk.knn import KNNClassifier
    from pywong.db.postgresql.settings import DEFAULT, DATABASES
    
    
    def run():
        """run方法"""
        DEFAULT['host'] = '127.0.0.1'
        DEFAULT['password'] = '123456'
    
        DATABASES['default_database'] = 'ems'
    
        knn = KNNClassifier(name='knn', k=1)
        knn_clf = knn.fit(target='zls_value', 
                          sql="SELECT zls_value, qty, state FROM data_all", 
                          test_size=0.1)
        print(knn_clf.predict_inner())
        print(knn_clf.score())
        knn_clf.save()
    
    
    if __name__ == '__main__':
        """main方法"""
        run()
    
    输出：
    [0.]
    1.0
    保存D:\model\knn.model.
    ```
    - MLinearRegression:
     ```python
    from pywong.ml.sk.linear_regression import MLinearRegression
    from pywong.db.postgresql.settings import DEFAULT, DATABASES
    
    
    def run():
        """run方法"""
        DEFAULT['host'] = '124.222.138.109'
        DEFAULT['password'] = 'ghy123'
    
        DATABASES['default_database'] = 'ems'
    
        lin_reg = MLinearRegression('lin_reg')
        lin_reg.fit(target='zls_value', 
                    sql="SELECT zls_value, qty, state FROM data_all", 
                    test_size=0.1)
    
        print(lin_reg.coef_)
        print(lin_reg.intercept_)
    
    
    if __name__ == '__main__':
        """main方法"""
        run()
    
    输出：
    [2.57626055e-02 1.54789412e+02]
    81.00259523809521
    ```
    - 其他:
    ```python
    略
    ```
    

#### 版本说明
    
1.  pywong 3.1.0
    
    功能列表：
    
    - MySql、PostgreSql和SqlServer驱动.

    - 资源监测.

    - KNNClassifier、MLinearRegression、RandomForest和TimeSeriesProphet封装.

    - 异常值检测.
    
2.  pywong 3.1.1
    
    功能列表：
    
    - 略
    
    更新内容：
    
    - 适配CentOS 7.x系统
    
3.  pywong 3.1.2
    
    功能列表：
    
    - 略
    
    更新内容：
    
    - 优化get_db_helper函数
    
# Common Liabrary

ilabservice 算法公共库


## 健康检测

    from intelab_python_tool.tools.Web.flaskAPI import Monitor
    Mt = Monitor(scheduler_list)
    Mt.run()
    
    scheduler_list: list
    such as :  [
                [service_name, monitor_log_path, monitor_type, scheduler_period_type, 
                scheduler_period, dingtalk_function
                restart_flag, args],
                ]
    
    service_name: 如果监控日志，则是重启服务时的服务名；如果是接口测试，则是url
    monitor_log_path: 如果监控日志，则是监控的日志文件的绝对路径；如果是接口测试，则是访问接口的方式get or post
    monitor_type: 'l'表示监控日志, 'a'表示监控接口
    scheduler_period_type: 定时任务的类型，'h'表示按小时，'m'表示按分钟
    scheduler_period:  定时任务的时长， 多少小时/多少分钟
    dingtalk_function: 发送报警的函数
    restart_flag: 是否需要重启服务
    args: 接口测试时需要传入的参数
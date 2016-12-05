# cliff

参考 [Cliff Documentation](http://docs.openstack.org/developer/cliff/)

cliff -- Command Line Interface Formulation Framework

openstack中一个用来构建命令行交互形式代码的框架：

## 简介

cliff框架用来方便快速开发类似git的多层次的交互式命令程序。主程序处理基本的参数，而将其他的参数和
功能传递给子命令执行。充分利用python的动态加载功能，子命令部分能够作为独立程序编写，打包和发布。
这样的组织形式为子命令提供了统一的框架视图，适合开发人员方便的组织代码。

### 基本对象

cliff通过以下四种对象的组合达成了命令行交互

The Appliacton
通过实现cliff.app.App子类，shell提示下的主入口。用来完成全局操作，例如公共参数，日志设置等操作。

The CommandManager
通过cliff.commandmanager.CommandManager来动态加载子命令插件，默认的实现机制是通过
[setuptools entry points](https://pythonhosted.org/setuptools/pkg_resources.html#entry-points)完成。

The Command
实际工作的类是通过cliff.command.Command实现。在这里实现正式的业务逻辑，而其他的对象和类实现大多是
用来构建框架

The Interactive Application
主程序还可以通过实现cliff.interactive.InteractiveApp实例来完成交互式的命令行框架。

### command

以下说明了3种最常用的command，可以匹配常见的增删改，查询，显示这样的操作。

#### Command

command类是一个子命令的具体实现，用户一般需要实现get_parse和take_action。
get_parse采用了argparse模块的方法注册子命令行的参数。
take_action获取参数值和进行逻辑处理，并进行特定的输出。

命令的注册，通过下面的方法向commandmanager中注册对应的command
```
# 注册子命令类对应子命令名称
self.command_manager.add_command('complete', cliff.complete.CompleteCommand)

# 子命令实现
class ActionDelete(Command):
    """Delete an action from the api"""
    def get_parser(self, prog_name):
        parser = super(ActionDelete, self).get_parser(prog_name)
        parser.add_argument(dest='action_id',
                            help='ID of the action')
        return parser

    def take_action(self, parsed_args):
        self.app.client.actions.delete(parsed_args.action_id)
        logging.info('Action {0} deleted'.format(parsed_args.action_id))
```

#### Lister

显示多条数据的command，命令显示结果类似查询结果的展示。lister提供了方便的实现和多种显示格式
类cliff.lister.Lister是Command类的子类，通过take_action方法返回数据，返回值是包含了两个成员的元组。
第一个元组元素为对应字段名称的元组，第二个为可迭代对象。

Lister支持多种输出格式，包括csv,table,value,yaml,json

#### ShowOne

显示某个对象的属性的command，通过cliff.show.ShowOne实现命令和支持多种格式显示。
返回值是包含了两个成员的元组，第一个是字段名称，第二个是可迭代对象

ShowOne支持多种输出格式，包括table,value,shell,yaml,json

### 交互模式

在没有指定子命令时可以进入交互模式。

```
[root@e7e075eedc924227a0254d212df133e0 ~(keystone_admin)]# freezer
(freezer) ?

Shell commands (type help <topic>):
===================================
cmdenvironment  edit  hi       l   list  pause  r    save  shell      show
ed              help  history  li  load  py     run  set   shortcuts

Undocumented commands:
======================
EOF  eof  exit  q  quit

Application commands (type help <topic>):
=========================================
action-create  backup-show      help        job-show         session-end       
action-delete  client-delete    job-abort   job-start        session-list      
action-list    client-list      job-create  job-stop         session-remove-job
action-show    client-register  job-delete  job-update       session-show      
action-update  client-show      job-get     session-add-job  session-start     
backup-list    complete         job-list    session-create   session-update    

(freezer) 
```


### demo

```
# App主入口，在CommandManager中注册了子命令
class DemoApp(App):

    def __init__(self):
        super(DemoApp, self).__init__(
            description='cliff demo app',
            version='0.1',
            command_manager=CommandManager('cliff.demo'),
            deferred_help=True,
            )

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)

def main(argv=sys.argv[1:]):
    myapp = DemoApp()
    return myapp.run(argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
```

```
# simplecommand的实现
class Simple(Command):
    "A simple command that prints a message."

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('sending greeting')
        self.log.debug('debugging')
        self.app.stdout.write('hi!\n')
		
# 控制输出的级别
(.venv)$ cliffdemo simple
sending greeting
hi!

(.venv)$ cliffdemo -v simple
prepare_to_run_command Simple
sending greeting
debugging
hi!
clean_up Simple

(.venv)$ cliffdemo -q simple
hi!		
```
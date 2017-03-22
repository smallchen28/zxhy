# python测试相关的工具

## 简介

单元测试是python开发中很重要的一部分。OPENSTACK中涵盖了主流的单元测试框架，因此学习和使用单元测试是必备的技能。

这里初步总结了各个工具的功能并且阅读了部分库的文档。后续结合实际代码再进一步总结。

## 各类工具总结

### 编写测试代码部分

1.unittest

标准库，包含了基本的概念和方法

2.mock

python3.3时加入标准库，模拟被测对象的行为

3.testtools

基于unittest的扩展框架，提供了更友好的方法。主要使用此框架编写用例

4.fixtures

单元测试中辅助模块，用于构建测试场景。参考unittest中的fixture概念。

fixtures模块是一个第三方模块，提供了一种简单的创建fixture类和对象的机制，并且也提供了一些内置的fixture。

5.testscenarios
场景测试

### 组织管理测试代码

1.coverage

单元测试中辅助模块，用于检查覆盖率

2.python-subunit

对测试输出进行流式处理，分析和统计测试结果。主要的执行入口

3.testrepository

在subunit更上一层的管理

### 其他

1.nose

2.mox/mox3


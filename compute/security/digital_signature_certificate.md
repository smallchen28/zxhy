# 数字签名和数字证书

 到底什么是“数字签名”（digital signature）和“数字证书”digital certificate）？对这些问题的理解，一直模模糊糊，很多细节搞不清楚。
 
今天，读完一篇[ 通俗易懂的文章](http://www.youdzone.com/signature.html)后，思路豁然开朗。为了加深记忆， 这篇文章的[翻译版](http://www.ruanyifeng.com/blog/2011/08/what_is_a_digital_signature.html)记录如下。

## 原理

1. 鲍勃有两把钥匙，一把是公钥，另一把是私钥。

![1](./pic/4efcd50a8dc6430080f6196f9d9e8617.png)
 
2. 鲍勃把公钥送给他的朋友们----帕蒂、道格、苏珊----每人一把。

![2](./pic/46533beff63c4ec3ac1717eb0b833a75.png) 
 
3. 苏珊要给鲍勃写一封保密的信。她写完后用鲍勃的公钥加密，就可以达到保密的效果。

![3](./pic/59c10cf13bee4092bd98fa6e60bd7381.png)
 
4. 鲍勃收信后，用私钥解密，就看到了信件内容。这里要强调的是，只要鲍勃的私钥不泄露，这封信就是安全的，即使落在别人手里，也无法解密。

![4](./pic/d6fc67913aa74adb8888b7b3060a7bed.png)
 
5. 鲍勃给苏珊回信，决定采用“数字签名”。他写完后先用Hash函数，生成信件的**摘要（digest）**。

![5](./pic/f7b56607cff04df9ae6ab299b9cd4e17.png)
 
6. 然后，鲍勃使用私钥，对这个摘要加密，生成**“ 数字签名”（signature）。**

![6](./pic/91ab401bd3b14623b10a67efd1100cc9.png)
 
7. 鲍勃将这个签名，附在信件下面，一起发给苏珊。

![7](./pic/0b7c09b7b4a34782adaeebd6cfa8674f.png)
 
8. 苏珊收信后，取下数字签名，用鲍勃的公钥解密，得到信件的摘要。由此证明，这封信确实是鲍勃发出的。

![8](./pic/c758627e85434239af300adcc9c05c98.png)

9. 苏珊再对信件本身使用Hash函数，将得到的结果，与上一步得到的摘要进行对比。如果两者一致，就证明这封信未被修改过。

![9](./pic/bc3e95fd2c8941d197ecaf8b8f45f376.png) 

10. 复杂的情况出现了。道格想欺骗苏珊，他偷偷使用了苏珊的电脑，用自己的公钥换走了鲍勃的公钥。此时，苏珊实际拥有的是道格的公钥，但是还以为这是鲍勃的公钥。因此，道格就可以冒充鲍勃，用自己的私钥做成“数字签名”，写信给苏珊，让苏珊用假的鲍勃公钥进行解密。

![10](./pic/1d4885ca07dd4b1699c83136aade2f94.png) 

11. 后来，苏珊感觉不对劲，发现自己无法确定公钥是否真的属于鲍勃。她想到了一个办法，要求鲍勃去找**“证书中心”（certificate authority，简称CA）**，为公钥做认证。证书中心用自己的私钥，对鲍勃的公钥和一些相关信息一起加密，生成**“ 数字证书”（Digital Certificate）**。

![11](./pic/1104ef6c8cd9437d8c11aad3829fa514.png)

12. 鲍勃拿到数字证书以后，就可以放心了。以后再给苏珊写信，只要在签名的同时，再附上数字证书就行了。

![12](./pic/79b85e8df702424baf9e1aef61aa2936.png)

13. 苏珊收信后，用CA的公钥解开数字证书，就可以拿到鲍勃真实的公钥了，然后就能证明“数字签名”是否真的是鲍勃签的。

![13](./pic/1a165d8efc834d3d80774d22dc1c13e6.png) 

## 应用

下面，我们看一个应用"数字证书"的实例：https协议。这个协议主要用于网页加密。

1. 首先，客户端向服务器发出加密请求。

![1](./pic/587c5b77212d4dc0b9fa94b0ee0b14f9.png)

2. 服务器用自己的私钥加密网页以后，连同本身的数字证书，一起发送给客户端。

![2](./pic/e85e27fd2da443938b392a263d37cf07.png)

3. 客户端（浏览器）的“证书管理器”，有“受信任的根证书颁发机构”列表。客户端会根据这张列表，查看解开数字证书的公钥是否在列表之内。

![3](./pic/72e4905da2664937ba612a9b7270f1c3.png)

4. 如果数字证书记载的网址，与你正在浏览的网址不一致，就说明这张证书可能被冒用，浏览器会发出警告。

![4](./pic/98c05d28c385476c8e9256abc670c985.png)

5. 如果这张数字证书不是由受信任的机构颁发的，浏览器会发出另一种警告。

![5](./pic/d8ca5bf9d1014552867c6c21831da200.png)

6. 如果数字证书是可靠的，客户端就可以使用证书中的服务器公钥，对信息进行加密，然后与服务器交换加密信息。

![6](./pic/91361ea2751c4bc9bc86c5ec48115724.png)

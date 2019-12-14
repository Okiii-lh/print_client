#### 树莓派+python实现远程打印机

++++

实验室搬来一台打印机，因为机型较旧，只能使用usb链接打印，单独拿台式做打印服务成本太高，正好有个闲置树莓派板子，准备用其做打印服务端，客户端服务端都用python实现
![打印机](https://github.com/Okery/print_client/blob/master/img/print.JPG)

打印机本机

树莓派型号为3b

![树莓派3B](https://github.com/Okery/print_client/blob/master/img/raspberry.JPG)

#### 思路

想着电脑做一个客户端，树莓派usb链接打印机，树莓派运行服务端

客户端选择文件，上传到服务端，服务端保存文件，并将文件打印，打印完毕后删掉源文件，初步想法是这样，看看能不能实现不用保存文件，直接进行打印

#### 实现
客户端初步界面如下
![打印客户端](https://github.com/Okery/print_client/blob/master/img/client.JPG)

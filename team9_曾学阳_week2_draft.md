# team_曾学阳_week2_final.md

## 一、实验概述

本次实验围绕 Linux 基础操作、Python/C++ 环境搭建、ROS1 Noetic 安装与入门、Turtlesim 仿真及通信机制展开，通过理论学习与实操结合，完成从环境配置到功能实现的全流程任务，加深对机器人操作系统基础框架与开发流程的理解。

## 二、实验环境

- 操作系统：Ubuntu 20.04 LTS（兼容 ROS1 Noetic）
- 开发工具：Visual Studio Code（VSCode）
- 核心框架：ROS1 Noetic
- 仿真模块：Turtlesim

## 三、实验任务与步骤

### （一）任务1：Linux 基础命令练习

#### 1. 文件管理操作（创建 / 移动 / 删除）

- 创建文件与目录：使用 `mkdir` 创建多级目录 `test_dir/sub_dir`，使用 `touch` 创建空文件 `test.txt`，命令如下：

```bash
mkdir -p test_dir/sub_dir  # 递归创建多级目录
touch test_dir/test.txt    # 在 test_dir 下创建空文件
ls -lah test_dir           # 查看目录内容（含隐藏文件与详细信息）
```

- 移动文件（并重命名）：

```bash
mv test_dir/test.txt test_dir/sub_dir/moved_test.txt
```

- 删除文件与目录（注意风险）：

```bash
rm -rf test_dir  # 谨慎使用！强制递归删除目录
```

操作效果截图：

![文件管理操作示例](screenshots/screenshot_01.png)

#### 2. 软件安装（apt 工具）

通过 apt 安装常用工具 `tree`（目录结构可视化工具）：

```bash
sudo apt update            # 更新软件源列表
sudo apt install tree      # 安装 tree 工具
tree ~/                    # 测试工具，查看家目录结构
```

操作效果截图：

![安装 tree 工具示例](screenshots/screenshot_02.png)

#### 3. 进程管理（ps 与 kill）

查看进程并筛选（示例：查找 firefox）：

```bash
ps aux | grep firefox
```

终止进程（用实际 PID 替换 12345）：

```bash
kill -9 12345
```

操作效果截图：

![进程管理示例（ps / kill）](screenshots/screenshot_03.png)

### （二）任务2：C++ 编程练习

#### C++ 简单程序（输入数字求和）

创建 `sum_cpp.cpp`，示例代码：

```cpp
#include <iostream>
using namespace std;

int main() {
    int num1, num2;
    cout << "Enter first number: ";
    cin >> num1;
    cout << "Enter second number: ";
    cin >> num2;
    cout << "Sum: " << num1 + num2 << endl;
    return 0;
}
```

编译与运行：

```bash
g++ sum_cpp.cpp -o sum_cpp  # 编译代码
./sum_cpp                  # 运行程序
```

编译运行截图：

![C++ 编译与运行示例](screenshots/screenshot_04.png)

#### 3. VSCode 调试配置

安装插件：在 VSCode 扩展市场安装 `C/C++` 插件。

调试配置示例（保存为 `.vscode/launch.json`）：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "C++: 调试当前目录下的可执行文件",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/code/sum_cpp.exe",
      "args": [],
      "stopAtEntry": false,
      "cwd": "${workspaceFolder}/code",
      "environment": [],
      "externalConsole": true,
      "MIMode": "gdb",
      "miDebuggerPath": "gdb.exe",
      "setupCommands": [
        {
          "description": "为 gdb 启用整齐打印",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        }
      ]
    }
  ]
}
```

调试 / 编译 / 运行截图（占位）：

- ![VSCode 调试示例](screenshots/screenshot_05.png)
- ![调试运行示例](screenshots/screenshot_06.png)

### （三）任务3：ROS1 安装验证

#### 1. ROS Noetic 安装（关键命令）

```bash
# 设置软件源
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
# 添加密钥
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C6548
# 安装 ROS Noetic（完整版）
sudo apt update
sudo apt install ros-noetic-desktop-full
# 初始化 rosdep
sudo rosdep init
rosdep update
# 添加环境变量（写入 ~/.bashrc）
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

安装验证截图：

![ROS 安装示例 1](screenshots/screenshot_07.png)
![ROS 安装示例 2](screenshots/screenshot_08.png)

#### 2. 安装验证（运行 roscore 等）

```bash
roscore
rosnode list
echo $ROS_PACKAGE_PATH
```

验证效果截图：

![roscore 输出示例](screenshots/screenshot_09.png)

### （四）任务4：CATKIN 工作空间与功能包

#### 1. 创建 Catkin 工作空间

```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

#### 2. 创建功能包与 HelloWorld 节点

```bash
cd ~/catkin_ws/src
catkin_create_pkg beginner_tutorials roscpp rospy std_msgs
```

示例 Python 节点 `hello_ros.py`（放在 `beginner_tutorials/scripts`）：

```python
#!/usr/bin/env python3
import rospy

if __name__ == "__main__":
    rospy.init_node("hello_ros_node")
    rospy.loginfo("Hello World from ROS Python Node!")
    rospy.spin()
```

设置可执行权限并运行：

```bash
chmod +x ~/catkin_ws/src/beginner_tutorials/scripts/hello_ros.py
cd ~/catkin_ws
catkin_make
source devel/setup.bash
rosrun beginner_tutorials hello_ros.py
```

操作效果截图：

![Catkin Hello ROS 运行示例](screenshots/screenshot_10.png)

### （五）任务5：Turtlesim 小乌龟基础

#### 1. 键盘控制小乌龟

```bash
# 终端1：启动 roscore
roscore
# 终端2：启动 Turtlesim 仿真节点
rosrun turtlesim turtlesim_node
# 终端3：启动键盘控制节点
rosrun turtlesim turtle_teleop_key
```

按终端提示（如 `i` 前进、`j` 左转、`l` 右转）控制小乌龟移动。

#### 2. 使用 `rostopic` 控制小乌龟（示例）

```bash
rostopic pub -r 1 /turtle1/cmd_vel geometry_msgs/Twist "linear:\
    x: 1.0\
    y: 0.0\
    z: 0.0"
```

#### 3. 程序控制小乌龟画圆（`turtle_circle.py`）

```python
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def turtle_circle():
    rospy.init_node("turtle_circle_node", anonymous=True)
    pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    rate = rospy.Rate(10)
    vel_msg = Twist()

    while not rospy.is_shutdown():
        vel_msg.linear.x = 0.5
        vel_msg.angular.z = 0.5
        pub.publish(vel_msg)
        rate.sleep()

if __name__ == "__main__":
    try:
        turtle_circle()
    except rospy.ROSInterruptException:
        pass
```

运行效果截图：

![Turtlesim 示意图](screenshots/screenshot_11.png)

### （六）任务6：多乌龟 launch + rqt_graph

#### 1. `multi_turtle.launch` 示例（放在 `beginner_tutorials/launch/`）

```xml
<launch>
    <!-- 启动两只 turtlesim，各自位于不同命名空间 -->
    <node name="turtlesim1" pkg="turtlesim" type="turtlesim_node" ns="turtle1" />
    <node name="turtlesim2" pkg="turtlesim" type="turtlesim_node" ns="turtle2" />
    <node name="rqt_graph" pkg="rqt_graph" type="rqt_graph" />
</launch>
```

#### 2. 启动 launch 并控制多乌龟

```bash
cd ~/catkin_ws
source devel/setup.bash
roslaunch beginner_tutorials multi_turtle.launch
```

可视化：

```bash
rqt_graph
rqt_plot /turtle1/cmd_vel/linear/x
```

## 四、实验总结

- **知识掌握**：
  通过本次实验，熟练掌握了 Linux 下的文件/进程/软件管理等常用命令；能够独立完成 Python / C++ 开发环境以及 ROS1 Noetic 的安装与配置；理解了 ROS 工作空间、功能包、节点、话题之间的核心关系，学会使用 launch 文件对多节点进行批量管理，并利用 Turtlesim 配合 rqt_graph、rqt_plot 对话题通信和运动轨迹进行可视化分析。

- **问题与解决**：
  - 问题1：`rosdep update` 长时间卡住或网络超时。  
    - 解决：更换国内镜像源（如阿里云、清华等），或手动更新 rosdep 配置文件，多次重试后完成初始化。  
  - 问题2：多乌龟场景中话题名称混乱，控制指令无法作用到目标小乌龟。  
    - 解决：先通过 `rostopic list` 确认实际话题名称，再使用命名空间（`ns`）对不同 turtlesim 实例进行隔离，并结合 `remap` 对话题进行重映射，最终实现对每只小乌龟的独立稳定控制。

<!-- 注：将实际截图放到 `screenshots/` 目录并替换以上占位图片 -->
# team_曾学阳_week2_final.md

## 一、实验概述

本次实验围绕 Linux 基础操作、Python/C++ 环境搭建、ROS1 Noetic 安装与入门、Turtlesim 仿真及通信机制展开，通过理论学习与实操结合，完成从环境配置到功能实现的全流程任务，加深对机器人操作系统基础框架与开发流程的理解。

## 二、实验环境

- 操作系统：Ubuntu 20.04 LTS（兼容 ROS1 Noetic）
- 开发工具：Visual Studio Code（VSCode）
- 核心框架：ROS1 Noetic
- 仿真模块：Turtlesim

## 三、实验任务与步骤

### （一）任务1：Linux 基础命令练习

#### 1. 文件管理操作（创建 / 移动 / 删除）

- 创建文件与目录：使用 `mkdir` 创建多级目录 `test_dir/sub_dir`，使用 `touch` 创建空文件 `test.txt`，命令如下：

```bash
mkdir -p test_dir/sub_dir  # 递归创建多级目录
touch test_dir/test.txt    # 在 test_dir 下创建空文件
ls -lah test_dir           # 查看目录内容（含隐藏文件与详细信息）
```

- 移动文件（并重命名）：

```bash
mv test_dir/test.txt test_dir/sub_dir/moved_test.txt
```

- 删除文件与目录（注意风险）：

```bash
rm -rf test_dir  # 谨慎使用！强制递归删除目录
```

操作效果截图：

![截图 01：文件管理操作示例](screenshots/screenshot_07.png)

#### 2. 软件安装（apt 工具）

通过 apt 安装常用工具 `tree`（目录结构可视化工具）：

```bash
sudo apt update            # 更新软件源列表
sudo apt install tree      # 安装 tree 工具
tree ~/                    # 测试工具，查看家目录结构
```

操作效果截图：

![截图 02：安装 tree 工具示例](screenshots/screenshot_13.png)

#### 3. 进程管理（ps 与 kill）

查看进程并筛选（示例：查找 firefox）：

```bash
ps aux | grep firefox
```
![截图 01：文件管理操作示例](screenshots/screenshot_01.png)
终止进程（用实际 PID 替换 12345）：

```bash
![截图 02：安装 tree 工具示例](screenshots/screenshot_13.png)
```

操作效果截图：
![截图 03：进程管理示例（ps / kill）](screenshots/screenshot_149.png)


### （二）任务2：C++ *编程练习*
![截图 05：C++ 编译与运行示例](screenshots/screenshot_147.png)
#### C++ 简单程序（输入数字求和）

创建 `sum_cpp.cpp`，示例代码：
![截图 06：VSCode 调试配置与运行示例](screenshots/screenshot_18.png)
```cpp
#include <iostream>
using namespace std;
![截图 01：文件管理操作示例](screenshots/screenshot_06.png)
int main() {
        int num1, num2;
        cout << "Enter first number: ";
![截图 03：进程管理示例（ps / kill）](screenshots/screenshot_08.png)
        cout << "Enter second number: ";
![截图 07：ROS 安装与 roscore 启动示例](screenshots/screenshot_04.png)
![截图 05：C++ 编译与运行示例](screenshots/screenshot_10.png)
        return 0;
![截图 06：VSCode 调试配置与运行示例](screenshots/screenshot_11.png)
```

![截图 90：ROS 安装与 roscore 启动示例](screenshots/screenshot_12.png)

![截图 07：ROS 安装与 roscore 启动示例](screenshots/screenshot_13.png)
g++ sum_cpp.cpp -o sum_cpp  # 编译代码
./sum_cpp                  # 运行程序
#### 3. VSCode 调试配置

安装插件：在 VSCode 扩展市场安装 `C/C++` 插件。

调试配置示例（将下面的 JSON 保存为 `.vscode/launch.json`）：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "C++: 调试当前目录下的可执行文件",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/code/sum_cpp.exe",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${workspaceFolder}/code",
            "environment": [],
            "externalConsole": true,
            "MIMode": "gdb",
            "miDebuggerPath": "gdb.exe",
            "setupCommands": [
                {
                    "description": "为 gdb 启用整齐打印",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```

调试 / 编译 / 运行截图（按需替换下面的占位图片）：

- ![Catkin 工作空间与 hello_ros 运行示例](screenshots/screenshot_08.png)
- ![C++ 编译与运行示例](screenshots/screenshot_146.png)
- ![Turtlesim 键盘控制示例](screenshots/screenshot_14.png)


true
<!-- 注：文中所有“操作效果截图/运行效果截图/调试效果截图”等均为占位，请将实际截图放到 `screenshots/` 目录并替换示例 -->
            ]
        }
    ]
}



- ![ROS 安装 - 验证 3](screenshots/screenshot_19.png)

说明：如果你想显示不同截图，只需把目标图片放到 `screenshots/` 并命名为 `screenshot_17.png` 或 `screenshot_18.png` 等（或修改上面的占位名）。

#### 2. 安装验证

启动核心服务：

```bash
roscore
```

查看节点：

```bash
rosnode list
```

查看 ROS 包路径：

```bash
echo $ROS_PACKAGE_PATH
```

验证效果截图：



![截图 07：ROS 安装与 roscore 启动示例](screenshots/screenshot_19.png)

### （四）任务4：CATKIN 工作空间与功能包

#### 1. 创建 Catkin 工作空间

```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

#### 2. 创建功能包与 HelloWorld 节点

```bash
cd ~/catkin_ws/src
catkin_create_pkg beginner_tutorials roscpp rospy std_msgs
```

示例 Python 节点 `hello_ros.py`（放在 `beginner_tutorials/scripts`）：

```python
#!/usr/bin/env python3
import rospy

if __name__ == "__main__":
        rospy.init_node("hello_ros_node")
        rospy.loginfo("Hello World from ROS Python Node!")
        rospy.spin()
```

设置可执行权限并运行：

```bash
chmod +x ~/catkin_ws/src/beginner_tutorials/scripts/hello_ros.py
cd ~/catkin_ws
catkin_make
source devel/setup.bash
rosrun beginner_tutorials hello_ros.py
```

操作效果截图：![截图 07：创建功能包与 HelloWorld 节点](screenshots/screenshot_18.png)


### （五）任务5：Turtlesim 小乌龟基础

#### 1. 键盘控制小乌龟

```bash
# 终端1：启动 roscore
roscore
# 终端2：启动 Turtlesim 仿真节点
rosrun turtlesim turtlesim_node
# 终端3：启动键盘控制节点
rosrun turtlesim turtle_teleop_key
```

按终端提示（如 `i` 前进、`j` 左转、`l` 右转）控制小乌龟移动。

#### 2. 使用 `rostopic` 控制小乌龟（示例）

```bash
rostopic pub -r 1 /turtle1/cmd_vel geometry_msgs/Twist "linear:\
    x: 1.0\
    y: 0.0\
    z: 0.0\
angular:\
    x: 0.0\
    y: 0.0\
    z: 0.0"
```

#### 3. 程序控制小乌龟画圆（`turtle_circle.py`）

```python
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def turtle_circle():
        rospy.init_node("turtle_circle_node", anonymous=True)
        pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
        rate = rospy.Rate(10)
        vel_msg = Twist()

        while not rospy.is_shutdown():
                vel_msg.linear.x = 0.5
                vel_msg.angular.z = 0.5
                pub.publish(vel_msg)
                rate.sleep()

if __name__ == "__main__":
        try:
                turtle_circle()
        except rospy.ROSInterruptException:
                pass
```

运行示例：

```bash
chmod +x ~/catkin_ws/src/beginner_tutorials/scripts/turtle_circle.py
cd ~/catkin_ws
catkin_make
source devel/setup.bash
rosrun beginner_tutorials turtle_circle.py
```

运行效果截图：

![截图 09：Turtlesim 键盘控制示例](screenshots/screenshot_145.png)

### （六）任务6：多乌龟 launch + rqt_graph

#### 1. `multi_turtle.launch` 示例（放在 `beginner_tutorials/launch/`）

```xml
<launch>
    <!-- 启动两只 turtlesim，各自位于不同命名空间 -->
    <node name="turtlesim1" pkg="turtlesim" type="turtlesim_node" ns="turtle1" />
    <node name="turtlesim2" pkg="turtlesim" type="turtlesim_node" ns="turtle2" />
    <node name="rqt_graph" pkg="rqt_graph" type="rqt_graph" />
</launch>
```


#### 2. 启动 launch 并控制多乌龟

```bash
cd ~/catkin_ws
source devel/setup.bash
roslaunch beginner_tutorials multi_turtle.launch
```

示例控制命令：

```bash
rostopic pub -r 1 /turtle1/cmd_vel geometry_msgs/Twist "linear:\
    x: 1.0\
    y: 0.0\
    z: 0.0\
angular:\
    x: 0.0\
    y: 0.0\
    z: 0.0"

rostopic pub -r 1 /turtle2/cmd_vel geometry_msgs/Twist "linear:\
    x: 0.5\
    y: 0.0\
    z: 0.0\
angular:\
    x: 0.0\
    y: 0.0\
    z: 0.8"
```

可视化：

```bash
rqt_graph
rqt_plot /turtle1/cmd_vel/linear/x
```


## 四、实验总结

- **知识掌握**：  
  通过本次实验，熟练掌握了 Linux 下的文件/进程/软件管理等常用命令；能够独立完成 Python / C++ 开发环境以及 ROS1 Noetic 的安装与配置；理解了 ROS 工作空间、功能包、节点、话题之间的核心关系，学会使用 launch 文件对多节点进行批量管理，并利用 Turtlesim 配合 rqt_graph、rqt_plot 对话题通信和运动轨迹进行可视化分析。

- **问题与解决**：  
  - 问题1：`rosdep update` 长时间卡住或网络超时。  
    - 解决：更换国内镜像源（如阿里云、清华等），或手动更新 rosdep 配置文件，多次重试后完成初始化。  
  - 问题2：多乌龟场景中话题名称混乱，控制指令无法作用到目标小乌龟。  
    - 解决：先通过 `rostopic list` 确认实际话题名称，再使用命名空间（`ns`）对不同 turtlesim 实例进行隔离，并结合 `remap` 对话题进行重映射，最终实现对每只小乌龟的独立稳定控制。

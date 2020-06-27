# python实现多级跳转登入跳板机


- jumplogin.py解决自动登入跳板机终端命令行被覆盖的问题


- macos下 "homebrew" 管理工具安装

```
官网：https://brew.sh/
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
$ xcode-select --install
$ brew install wget
```

- iterm2安装
```
官网地址：https://www.iterm2.com/downloads.html
$ wget https://iterm2.com/downloads/stable/iTerm2-3_3_11.zip
$ unzip iTerm2-3_3_11.zip
$ mv iTerm.app ~/Applications
```

- 在 mac 下，实现与服务器进行便捷的文件上传和下载操作。
```
项目介绍

步骤
1.安装支持rz和sz命令的lrzsz：brew install lrzsz

等了挺长时间的。

2.在本地/usr/local/bin/目录下保存iterm2-send-zmodem.sh 和iterm2-recv-zmodem.sh两个脚本

3.设置一下两个脚本的权限，一般 chmod 777 就行了

$ chmod 777 /usr/local/bin/iterm2-*
4.设置Iterm2的Tirgger特性，profiles->default->editProfiles->Advanced中的Tirgger

添加两条trigger，分别设置 Regular expression，Action，Parameters，Instant如下：

1.第一条
        Regular expression: rz waiting to receive.\*\*B0100
        Action: Run Silent Coprocess
        Parameters: /usr/local/bin/iterm2-send-zmodem.sh
        Instant: checked
2.第二条
        Regular expression: \*\*B00000000000000
        Action: Run Silent Coprocess
        Parameters: /usr/local/bin/iterm2-recv-zmodem.sh
        Instant: checked
```

- macos终端bash-shell修改
```
创建并写入如下内容
[erick@ErickdeAir ~]$ cat .bash_profile
export BASH_SILENCE_DEPRECATION_WARNING=1

PS1='\[\033]0;$TITLEPREFIX:$PWD\007\]'
PS1="$PS1"'\[\033[32m\]'
PS1="$PS1"'\u@\h '
PS1="$PS1"'\[\033[33m\]'
PS1="$PS1"'\W'
PS1="$PS1"'\[\033[0m\]'
export PS1="[$PS1]\$ "

在如下文件中添加
[erick@ErickdeAir ~]$ cat /etc/profile
alias ll='ls -lG'
alias ls='ls -G'
alias grep='grep --color=auto'
```

- macos终端zsh-shell修改
```
在如下文件中修改和添加
[erick@ErickdeAir ~]$ cat /etc/zshrc
# Default prompt
#PS1="%n@%m %1~ %# "
PS1="[%n@%m %1~]$ "
autoload -U colors && colors
PROMPT="[%{$fg[green]%}%n@%m %{$reset_color%}%{$fg[yellow]%}%1~%{$reset_color%}]$ "

alias ll='ls -lhG'
alias ls='ls -G'
alias grep='grep --color=auto'
```

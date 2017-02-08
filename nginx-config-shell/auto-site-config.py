#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys;

vhost_dir = 'conf'+os.path.sep+'vhost'+os.path.sep;

print 'Please enter a domain as server_name:\r';
server_name = raw_input('>:');

print 'Please enter the app to access the entrance to the directory as root:\r';
root = raw_input('>:');

# 生成root目录下的.user.ini文件,指定网站作用域目录
if os.path.exists(root)==False:
	print "root wrong. Not exists"
	sys.exit(0)

hf = open(root+os.path.sep+'.user.ini','wb')
if hf==False:
	print "Can't write .user.ini config file"
	sys.exit(0)

hf.write('open_basedir='+root[0:-7]+':/tmp/:/proc/');
hf.close()

# 生成nginx的conf文件
conf = open(vhost_dir+server_name+'.conf','wb')
if conf==False:
	print "Can't write vhost config file"
	sys.exit(0)

# 创建 error_log 文件
os.system('sudo mkdir -p /var/log/nginx');
os.system('sudo touch  /var/log/nginx'+server_name+'-error.log');

vhost_conf = '''server
    {
        listen 80;
        server_name %s;
        index index.html index.htm index.php default.html default.htm default.php;
        root  "%s";

        charset utf-8;

       	include tp-rewrite.conf;

        access_log on;
        error_log  /var/log/nginx/%s.log error;

        sendfile on;


        #error_page   404   /404.html;
        include enable-php-pathinfo.conf;

        location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$
        {
            expires      30d;
        }

        location ~ .*\.(js|css)?$
        {
            expires      12h;
        }

        location ~ /\.
        {
            deny all;
        }


    }
''' % (server_name,root,server_name+'-error');
conf.write(vhost_conf);
conf.close()

os.system('sudo cp -r conf /usr/local/nginx/');
os.system('sudo /usr/bin/nginx -t');
os.system('sudo lnmp restart');

import os;

os.system('sudo cp -r conf /usr/local/nginx/');
os.system('sudo /usr/bin/nginx -t');
os.system('sudo lnmp restart');

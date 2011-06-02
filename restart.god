python static/merge.py
ps x -u work|ack server_god_dev\.py|ack python|awk '{print $1}'|xargs kill
./server_god_dev.py

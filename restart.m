python static/merge.py
ps x -u work|ack server_u\.py|ack python|awk '{print $1}'|xargs kill
./server_m_dev.py

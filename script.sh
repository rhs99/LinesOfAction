mkfifo pipe
g++ ai.cpp -o ai
python3 main.py < pipe | ./ai | tee pipe
rm pipe
# python3 two.py < pipe | ./one > pipe  # using this instead will not show output in the terminal

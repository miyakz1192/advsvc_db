./dbopetool.py  --listrec  | grep RECORD | awk -F "=" '{print $2}' | while read line; do ./dbopetool.py --savewav ${line}; done

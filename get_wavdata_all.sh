
./dbopetool.py --listrec | awk -F "ID=" '{print $2}' | awk -F "," '{print $1}' | grep -v "^$" | while read line; do ./dbopetool.py --savewav ${line}; done

# ./dbopetool.py  --listrec  | grep "ID=" | awk -F "ID=" '{print $2}' | while read line; do ./dbopetool.py --savewav ${line}; done

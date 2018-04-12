#/bin/bash
if [ -f mmaserver.pid ]; then
	echo "WARNING!!! mmaserver.pid file exists. Will attempt to start anyway. The old PID is--"
	cat mmaserver.pid
fi

nohup python ./SimpleWebServer-Modified.py >> mmaserver.log &
echo $! > mmaserver.pid

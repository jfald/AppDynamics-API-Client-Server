#/bin/bash
if [ -f mmaserver.pid ] ; then
	kill $(cat mmaserver.pid)
else
	echo "Couldn't find mmaserver.pid. Is the server really running, if so kill manually"
	exit 1
fi
sleep 5

if [ -f mmaserver.pid ] ; then

	if ps -p $(cat mmaserver.pid) > /dev/null
	then
		kill -9 $(cat mmaserver.pid)
		echo "Had to hard kill the server."
	fi
else
	rm mmaserver.pid
	exit 0
fi

rm mmaserver.pid


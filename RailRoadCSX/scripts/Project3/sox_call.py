from subprocess import call
call(["ls","-al"])

command="ls -al | awk '{print $9}' | tail -n +4"

call([command])
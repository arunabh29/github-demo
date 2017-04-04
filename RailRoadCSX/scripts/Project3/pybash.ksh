
declare -a arr

arr=`ls -al | awk '{print $9}' | tail -n +4`

declare -a joined

joined=($(./pytest.py ${arr[@]}))
echo ${joined[@]}
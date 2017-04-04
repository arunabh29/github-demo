# Adding comment to test commit
# can also take diff between HEAD and HEAD^
# arr=`git diff HEAD HEAD^ --name-only`
arr=`git log | grep commit | head -n +2 | awk '{print $2}'`
cgh_set=""
for k in "${arr[@]}" ;
do
# echo "$k"
cgh_set=${cgh_set}"$k";
done

echo Finding differences between commits: $cgh_set
git diff $cgh_set --name-only > ./jira_attachment.txt

# Sleeping 5 seconds before invoking python
sleep 5
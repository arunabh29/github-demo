
WORK_DIR=$1
CHANGESET_FILE_PATH=$2


echo "ChangeSet File Path is: ${CHANGESET_FILE_PATH}" 


    for each in `ssh lnx21261 cat ${CHANGESET_FILE_PATH}` ;
     do
       FILE_TYPE=`echo $each | cut -f2 -d"."`
   
       if [ ${FILE_TYPE} == gnt ]
        then
         DEST_DIR="/opt/local/software/pt854/psoft/cblbin"
         echo "Destination dir is: " ${DEST_DIR}
         echo "Actual path: " ${WORK_DIR}/$each
         scp ${WORK_DIR}/$each z_mzauto@lnx21256:${DEST_DIR}/     
       fi


       if [ ${FILE_TYPE} == cbl ]
        then
         DEST_DIR="/opt/local/software/pt854/psoft/src/cbl"
         echo "Destination dir is: " ${DEST_DIR}
         echo "Actual path: " ${WORK_DIR}/$each
         scp ${WORK_DIR}/$each z_mzauto@lnx21256:${DEST_DIR}/
       fi


       if [ ${FILE_TYPE} == in -o ${FILE_TYPE} == xml -o ${FILE_TYPE} == template ]
        then
         DEST_DIR="/opt/local/data/psoft/cntl"
         echo "Destination dir is: " ${DEST_DIR}
         echo "Actual path: " ${WORK_DIR}/$each
         scp ${WORK_DIR}/$each z_mzauto@lnx21256:${DEST_DIR}/
       fi
   
   
       if [ ${FILE_TYPE} == datin -o ${FILE_TYPE} == DATIN -o ${FILE_TYPE} == csv ]
        then
         DEST_DIR="/opt/local/data/psoft/input"
         echo "Destination dir is: " ${DEST_DIR}
         echo "Actual path: " ${WORK_DIR}/$each
         scp ${WORK_DIR}/$each z_mzauto@lnx21256:${DEST_DIR}/
       fi


       if [ ${FILE_TYPE} == sqr -o ${FILE_TYPE} == sqc ]
        then
         DEST_DIR="/opt/local/software/pt854/psoft/sqr"
         echo "Destination dir is: " ${DEST_DIR}
         echo "Actual path: " ${WORK_DIR}/$each
         scp ${WORK_DIR}/$each z_mzauto@lnx21256:${DEST_DIR}/
       fi
   
   
       if [ ${FILE_TYPE} == sh ]
        then
         # DEST_DIR="/opt/software/batch/scripts"
         # su -c "mkdir -p $DEST_DIR" z_mzauto
         # scp ${WORK_DIR}/$each z_mzauto@lnx21256:${DEST_DIR}/
         echo "Actual path: " ${WORK_DIR}/$each
       fi

    done
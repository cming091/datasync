if [ $# -ne 1 ]; then
    echo "error param!"
    echo "Usage: $0 dev|test|product"
    exit 1
fi

echo "第一个参数为：$1"

export ENV_CONF=$1


jobs=("inbound" "outbound" "materials" "boxes")


logPath=$(pwd)'/log/log/'

cleanFile(){
    if [ -e $1 ];then
        echo ' '> $1
    else
        echo 'nofile',$1
    fi
}

start(){
    for job in ${jobs[@]}; do
        logFile=${logPath}${job}.log
        echo $job,$logFile
        cleanFile $logFile
        nohup python3 -u run.py $job >$logFile 2>&1 &
        sleep 1
    done
}

start





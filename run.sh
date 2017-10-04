#/bin/bash
mode=$1

if [[ $mode != "dev" ]]; then
    redirect="&> /dev/null"
fi

echo $redirect

cd Interface && node server.js $redirect &
cd Backend && python3 manage.py runserver

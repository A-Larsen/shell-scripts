#!/bin/bash

cd /home/nyquist/Development/tst
templatePath=/home/nyquist/Development/tst/templates/"$1"/


# how to write a man page: 
# /opt/google/chrome/xdg-mine
# $ man man
# groff ?
helpOption(){
cat <<_HELP
NAME
       tst - a command line tool to open vim to a template for testing ideas

SYNOPSIS
       tst {language} [template]
       tst -h

COMMANDS
       language      language species the programing language you want 
                     to write your test in. It is chosen by extension 
                     name

                     Example: $ tst js
                     this will open a test for a javascript program

       template      tells tst what template you want to use. located in
                     /home/\$USER/Development/tst/\$LANGUAGE\template.
                     if no template is specified the default template is 
                     used.


OPTIONS
       -h      displays help  

SEE ALSO
    tstsave runtst mktst
    
_HELP
}

open(){
    cd $1
    rm -R *

    case $1 in 
        js)
            if [[ $2 == "basic_express" ]]; then
                npm install --save express
            fi
        ;;
    esac

    cat ${templatePath}/"$2" > tst."$1"
    chmod +x tst."$1"
}

# handle options/flags
if (( $# > 0 )); then
    while (( $# != 0 )); do
        case $1 in
            -h)
                helpOption | less
                exit
                # shift
            ;;
            py|c|cpp|js|sh|pl|kts|java)
                break
            ;;
            *)
                echo "argument \"${1}\" is not valid"
                exit 1
            ;;
        esac
    done
else
    echo "arguments are required"
    exit 2
fi

#get exit statuses and handle errors/exceptions
declare -A exceptions

open_argument2=${2}

[[ -f "${templatePath}/$2" ]]; exceptions["template-does-not-exist"]=$?

[[ ! -z "$2" ]]; exceptions["no-template-argument"]=$?


for throw in ${!exceptions[@]}; do
    if [[ ${exceptions[$throw]} == "1" ]]; then

        case $throw in
            template-does-not-exist)
                printf "\
template does not exist\n\
using basic template instead\n"
                read null
                # open $1 basic
                open_argument2="basic"
                break
            ;;
            no-template-argument)
                # : #apperantly the same as pass in python
                # open $1 basic
                open_argument2="basic"
                break
            ;;
            *)
                echo "an error has occured"
                exit 3
            ;;
        esac
    fi
done

open $1 ${open_argument2}
# vim --remote-tab tst."$1" 
vim tst."$1" 

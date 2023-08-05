#!/bin/bash

##### ANPP CONFIG START #####
# default Workspace dir, all projects are here
export defaultPath=~/zengjf

# project dir info 
projects=(
    'M0-project'
    'M8-project'
)

# product dir info 
products=(
    'M0'
    'k62v1_64'
)

# kernel dir info 
kernels=(
    'kernel-4.9'
    'kernel-4.19'
)

# dts dir info 
dtss=(
    'arch/arm64/boot/dts/mediatek/'
    'arch/arm64/boot/dts/mediatek/'
)

# bootloaderStage1 dir info 
bootloaderStage1s=(
    'vendor/mediatek/proprietary/bootable/bootloader/preloader'
    'vendor/mediatek/proprietary/bootable/bootloader/preloader'
)

# bootloaderStage2 dir info 
bootloaderStage2s=(
    'vendor/mediatek/proprietary/bootable/bootloader/lk'
    'vendor/mediatek/proprietary/bootable/bootloader/lk'
)

# out dir info 
outs=(
    'out/target/product'
    'out/target/product'
)

# efuse dir info 
efuses=(
    'vendor/mediatek/proprietary/scripts/sign-image_v2'
    'vendor/mediatek/proprietary/scripts/sign-image_v2'
)

# image dir info 
images=(
    '.'
    'preloader.bin lk.img'
)

# output dir info 
outputs=(
    '.'
    'prebuild_images'
)

##### ANPP CONFIG END #####

##### ANPP CUSTOM START #####
# 1. argv: refer to config.json "project_keys" array order except ${1}
#     ${1}: cmd
#     ${2}: project
#     ${3}: product
#     ${4}: kernel
#     ${5}: dts
#     ${6}: bootloaderStage1
#     ${7}: bootloaderStage2
#     ${8}: out
#     ${9}: efuse
#     ${10}: image
#     ${11}: output
# 2. return:
#     0: function run success
function project_product_custom() {

    # echo "argc: $#"
    # echo "argv: $@"

    if [ $1 == "test" ]; then
        return 0
    elif [ $# -eq 1 ] && [ $1 == "vim" ]; then
        touch ~/.vimrc

        vim_anpp_config_start=`grep "ANPP CONFIG START" ~/.vimrc`
        vim_anpp_config_end=`grep "ANPP CONFIG END" ~/.vimrc`
        if [ -z "${vim_anpp_config_start}" ] && [ -z "${vim_anpp_config_end}" ]; then
            cat <<EOF >> ~/.vimrc
" ANPP CONFIG START
filetype on
filetype plugin on
filetype indent on
syntax enable
set hlsearch
hi Search cterm=NONE ctermfg=white ctermbg=black
set tabstop=4
set shiftwidth=4
" ANPP CONFIG END
EOF
        else
            # 1. Using sed to delete all lines between two matching patterns
            #   https://stackoverflow.com/questions/6287755/using-sed-to-delete-all-lines-between-two-matching-patterns
            sed -i '/" ANPP CONFIG START/,/" ANPP CONFIG END/{{d;};}' ~/.vimrc
        fi
        return 0

    elif [ $# -eq 1 ] && [ $1 == "tmux" ]; then
        touch ~/.tmux.conf

        tmux_anpp_config_start=`grep "ANPP CONFIG START" ~/.tmux.conf`
        tmux_anpp_config_end=`grep "ANPP CONFIG END" ~/.tmux.conf`
        if [ -z "${tmux_anpp_config_start}" ] && [ -z "${tmux_anpp_config_end}" ]; then
            cat <<EOF >> ~/.tmux.conf
# ANPP CONFIG START
set -g default-terminal "screen-256color"
set -g history-limit 10000

# Use Alt-arrow keys to switch panes
unbind-key j
bind-key j select-pane -D
unbind-key k
bind-key k select-pane -U
unbind-key h
bind-key h select-pane -L
unbind-key l
bind-key l select-pane -R

unbind '"'
bind - splitw -v -c '#{pane_current_path}'
unbind %
bind | splitw -h -c '#{pane_current_path}'
# ANPP CONFIG END
EOF
        else
            # 1. Using sed to delete all lines between two matching patterns
            #   https://stackoverflow.com/questions/6287755/using-sed-to-delete-all-lines-between-two-matching-patterns
            sed -i '/# ANPP CONFIG START/,/# ANPP CONFIG END/{{d;};}' ~/.tmux.conf
        fi
        return 0
    else
        return 1
    fi
}
##### ANPP CUSTOM END #####

##### ANPP COMPONENT START #####
# components for shell alias cmd
components=(
    android
    kernel
    dts
    out
    bs1
    bs2
    efuse
    images
)

##### ANPP COMPONENT END #####

# pp function
function project_product() {
    project=
    product=
    kernel=
    currentpath=`pwd`

    # jump command
    if [ $# -lt 1 ]; then
        for i in "${!projects[@]}"
        do
            echo $i: ${projects[i]} -- ${products[i]} -- ${kernels[i]}
        done

        echo
        cd $defaultPath
    elif [ $1 == "workspace" ]; then
        cd $defaultPath
    else

        # jump to project
        for i in "${!projects[@]}"
        do
            project_lowercase=${projects[i]%%-*}
            project_lowercase=${project_lowercase,,}
            if [ ${1,,} == "${project_lowercase}" ]; then
                project=${projects[i]}
                product=${products[i]}

                cd ${defaultPath}/${projects[i]}

                if [ $# -eq 1 ]; then
                    pwd
                    return
                else
                    shift
                fi

                break
            fi
        done

        currentpath=`pwd`
        # jump to component
        for i in "${!projects[@]}"
        do
            if [[ ${currentpath} =~ "${projects[i]}" ]]; then
                ##### ANPP COMMAND START #####
                project=${projects[i]}
                product=${products[i]}
                kernel=${kernels[i]}
                dts=${dtss[i]}
                bootloaderStage1=${bootloaderStage1s[i]}
                bootloaderStage2=${bootloaderStage2s[i]}
                out=${outs[i]}
                efuse=${efuses[i]}
                image=${images[i]}
                output=${outputs[i]}

                if [ $1 == "None" ]; then
                    cd .
                elif [ $1 == "android" ]; then
                    cd ${defaultPath}/${project}
                elif [ $1 == "kernel" ]; then
                    cd ${defaultPath}/${project}/${kernel}
                elif [ $1 == "dts" ]; then
                    cd ${defaultPath}/${project}/${kernel}/${dts}
                elif [ $1 == "out" ]; then
                    cd ${defaultPath}/${project}/${out}/${product}
                elif [ $1 == "bs1" ]; then
                    cd ${defaultPath}/${project}/${bootloaderStage1}
                elif [ $1 == "bs2" ]; then
                    cd ${defaultPath}/${project}/${bootloaderStage2}
                elif [ $1 == "efuse" ]; then
                    cd ${defaultPath}/${project}/${efuse}
                elif [ $1 == "images" ]; then
                    echo copy file from ${defaultPath}/${project}/${out}/${product} to ${defaultPath}/${project}/${output}
                    mkdir -p ${defaultPath}/${project}/${output}
                    cd ${defaultPath}/${project}/${out}/${product}
                    cp -v ${image} ${defaultPath}/${project}/${output}
                    cd -
                    return
                else
                    project_product_custom $1 ${defaultPath} ${project} ${product} ${kernel} ${dts} ${bootloaderStage1} ${bootloaderStage2} ${out} ${efuse} ${image} ${output}
                    returnData=$?
                    if [ ${returnData} -ne 0 ]; then
                        echo "error: $1 returned with value: ${returnData}"
                        return
                    fi
                fi 
                ##### ANPP COMMAND END #####

                break
            fi
        done

        if [ "${project}" == "" ]; then
            echo "please jump to your android project at first"
            cd ${defaultPath}
        fi
    fi
    pwd
}

##### ANPP ALIAS START #####
alias anpp="project_product"           # just for project_product function alias
alias anppc="project_product_custom"   # just for project_product_custom function alias# custom shell alias cmds
alias pl="bs1"
alias lk="bs2"
##### ANPP ALIAS END #####

# component alias
for i in "${!components[@]}"
do
    component=${components[i]}

    alias ${component}="project_product ${component}"
done

# project_product completion
projectStrings=""
componentStrings=""

function _project_product_completions()
{

    # get project string
    for i in "${!projects[@]}"
    do
        project_lowercase=${projects[i]%%-*}
        project_lowercase=${project_lowercase,,}

        projectStrings="${projectStrings} ${project_lowercase}"
    done

    # get project component string
    for i in "${!components[@]}"
    do
        component=${components[i]}
        componentStrings="${componentStrings} ${component}"
    done

    # completion
    if [ "${#COMP_WORDS[@]}" == "2" ]; then
        COMPREPLY=($(compgen -W "${projectStrings}" "${COMP_WORDS[1]}"))
    elif [ "${#COMP_WORDS[@]}" == "3" ]; then
        COMPREPLY=($(compgen -W "${componentStrings}" "${COMP_WORDS[2]}"))
    fi
}

complete -F _project_product_completions anpp

# project completion
componentStrings=""

function _project_completions()
{

    # get project component string
    for i in "${!components[@]}"
    do
        component=${components[i]}
        componentStrings="${componentStrings} ${component}"
    done

    # completion
    if [ "${#COMP_WORDS[@]}" == "2" ]; then
        COMPREPLY=($(compgen -W "${componentStrings}" "${COMP_WORDS[1]}"))
    fi
}

# project alias and completion
for i in "${!projects[@]}"
do
    project_lowercase=${projects[i]%%-*}
    project_lowercase=${project_lowercase,,}

    alias ${project_lowercase}="project_product ${project_lowercase}"
    complete -F _project_completions ${project_lowercase}
done

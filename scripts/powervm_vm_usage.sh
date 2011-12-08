#!/bin/bash
# get lpar,cpu,mem,frame with same naming convention as Ludo's script for esx
ssh mgtu02 -- "echo '\"name\",\"numvpu\",\"memorymb\",\"esxhost\",\"parent\"'
lssyscfg -r sys -F name | while read framename
do
  lssyscfg -m \"\$framename\" -r lpar -F name,lpar_env,state| egrep -v \"Not Activated\"| sed 's/,.*//g' | while read vm rest
  do

    cpu=\$(lshwres -m \"\$framename\" -r proc --level lpar -Fcurr_proc_units --filter \"lpar_names=\$vm\")
    echo \$cpu | grep -q \"null\" && cpu=\$(lshwres -m \"\$framename\" -r proc --level lpar -Fcurr_procs --filter \"lpar_names=\$vm\")
    mem=\$(lshwres -m \"\$framename\" -r mem --level lpar -Fcurr_mem --filter \"lpar_names=\$vm\")
    echo '\"'\$vm'\",\"'\$cpu'\",\"'\$mem'\",\"'\$framename'\",\"\"'
  done
done
"

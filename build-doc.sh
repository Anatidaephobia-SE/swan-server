#!/bin/bash

dirlist=$(find $1 -mindepth 1 -maxdepth 1 -type d)


get_list_of_folders() {
    dirlist=$(find $1 -mindepth 1 -maxdepth 1 -type d)
}

is_doc_directory_exist() {
    ls $1 2> /dev/null | grep "docs" 1> /dev/null
    if [[ $? -eq 0 ]]; then 
        return 0
    else
        return 1
    fi
}

is_paths_yaml_exist() {
    ls $1/docs 2> /dev/null | grep "paths.yaml" 1> /dev/null
    if [[ $? -eq 0 ]]; then 
        return 0
    else
        return 1
    fi
}

is_definitions_yaml_exist() {
    ls $1/docs 2> /dev/null | grep "schemas.yaml" 1> /dev/null
    if [[ $? -eq 0 ]]; then 
        return 0
    else
        return 1
    fi
}

build_doc_entry() {
    touch generated-doc.yaml
    cat doc-entry.yaml >> generated-doc.yaml
}

add_paths_doc_to_global_doc() {
    cat $1/docs/paths.yaml >> generated-doc.yaml
    echo -e "\n" >> generated-doc.yaml
}

add_definitions_doc_to_global_doc() {
    cat $1/docs/schemas.yaml >> generated-doc.yaml
    echo -e "\n" >> generated-doc.yaml
}

add_new_line() {
    echo -e "\n" >> generated-doc.yaml
}

build_doc_exit() {
    cat doc-exit.yaml >> generated-doc.yaml
}
truncate -s 0 generated-doc.yaml
build_doc_entry
get_list_of_folders

declare -a recognized_dirs

for dir in $dirlist
do
  is_paths_yaml_exist $dir
  if [[ $? -ne 0 ]]; then
    continue
  fi

  is_definitions_yaml_exist $dir
  if [[ $? -ne 0 ]]; then
    continue
  fi
  recognized_dirs+=( $dir )
done

for dir in "${recognized_dirs[@]}"
do 
  echo "recognized docs folder and yaml's in $dir"
done



#add_new_line
#echo "definitions:" >> generated-doc.yaml
#add_new_line

for dir in "${recognized_dirs[@]}"
do 
  add_definitions_doc_to_global_doc $dir
done
echo "paths:" >> generated-doc.yaml

for dir in "${recognized_dirs[@]}"
do 
  add_paths_doc_to_global_doc $dir
done

add_new_line
build_doc_exit

#start generating json file from docker image
rm -rf docs
mkdir -p docs

cp generated-doc.yaml ./docs
docker run --rm -v "$PWD/docs":/docs openapitools/openapi-generator-cli generate -i /docs/generated-doc.yaml -g openapi -o /docs/swan-doc


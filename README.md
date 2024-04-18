export LC_ALL=C.UTF-8
 
ansible-playbook --extra-vars '{"host":"NOMBRE_INTANCIA-RAMA","git_repo":"[dev]","branch":"1RAMA","db_name":"base_de_datos"}'  -i ~/binhex-deploy/ansible-inventory ~/binhex-deploy/deploy-standar.yml -u root
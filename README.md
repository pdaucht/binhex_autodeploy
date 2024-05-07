# BINHEX AUTODEPLOY


## CONFIGURAR GITHUB
1. Settings/Webhook
2. Click on [Add webhook]
3. PayLoad URL: https://[YOUR-JENKINS-URL]/github-webhook/
4. Secret: token_de_git

## CONFIGURAR JENKINS
1. Accede a tu Jenkins
2. Hacer click en el boton [+ Nueva Tarea]
   En el campo "Enter an item name" escribir el nombre de la tarea
3. Seleccionar la opción "Crear un proyecto de estilo libre"
4. Hacer click en OK
5. Seleccionar la opción "GitHub project" y agregar la URL del proyecto.
6. En el apartado "Configurar el origen del código fuente" selecionar la opción Git y colocar la URL de clonado del proyecto y luego seleccionar las credenciales referentes a GitHub
7. En el apartado "Branches to build" especificar la rama la cual va a verificar una vez le sean notificado la actividad de cambios (*/RAMA)
8. En el apartado "Disparadores de ejecuciones" seleccionar "GitHub hook trigger for GITScm polling"
9. En "Build Steps" seleccionar "Ejecutar linea de comandos (shell)"
10. En Comando pegar las siguentes líneas

```bash
export LC_ALL=C.UTF-8
ansible-playbook --extra-vars '{"host":"NOMBRE_INTANCIA-RAMA","git_repo":"REPO_FILE","branch":"BRANCH","odoo_conf":"ODOO_FILE"}'  -i ~/binhex_autodeploy/ansible-inventory ~/binhex_autodeploy/deploy-standar.yml -u root
```
### PARÁMETROS DEL ANSIBLE
- host -- Valor del atriburo "name" en el nodes.json que identifica a (instancia|contenedor|servidor)
- git_repo -- nombre del archivo de configuración del repo git sin ".json"
- branch -- Rama del git a (clonar|actualizar)
- odoo_conf -- nombre del archivo de configuración del odoo sin ".json"

## DESCRIPCIÓN DE LOS ARCHIVOS JSON
### ARCHIVO: "nodes.json"
#### Este archivo se utiliza para autogenerar la configuración del ssh y el inventario del Ansible

* ip ---------- ip de la instancia en la red insterna
* nodeproxy --- FQDN del servidor con ip real que hará función de "ProxyJump"
* name -------- alias por el cual podrá ser reconocido tanto en la configuración del ssh como en el inventario
* nodename ---- atributo solo utlizado para agrupar en la configuarión del SSH los host que utilicen el mismo proxyJump

```
[
    [
      Este ejemplo es para las instancias que estan con ip real.
      En el atributo "ip" puede ser utilizado tanto la ip real como el FQDN.
      {
         "data":[
            {"ip":"10.0.0.4","name":"dev2.ejemplo.com"}
         ]
      }
    ],
    [
      Este ejemplo es para las instancias que no tengan ip real y se encuentren en una infraestructura de DMZ
      por lo que para acceder por ssh sea necesario configuar "ProxyJump" en el SSH.
      {
      "nodename":"DEV-ENV",
      "nodeproxy":"proxyssh.ejemplo.com",
      "data":[
               {"ip":"10.0.4.3","name":"dev1.ejemplo.com"},

         ]
      }
    ]
]
```
### ARCHIVO: "repos.json"
- pool_directory --- Directorio en el que queremos desplegar el repo.
- url -------------- Dirección ULR o SSH para clonar o actualizar repo
- repo_name -------- Nombre del repo (git@github.com:pdaucht/[binhex_autodeploy].git)
```
{
    "pool_directory":"temp/casa/",
    "origin":{
                "url" : "git@github.com:pdaucht/binhex_autodeploy.git",
                "repo_name" : "binhex_autodeploy"
            }
}
```

### ARCHIVO: "odoo.json"

Este archivo es de vital importancia, pues con estos datos son utilizados para 
desplegar el repositorio y se agrega la configuración de nuestro odoo el addon o el 
repo de addons

- addons_directory --- Ruta del directorio donde tenemos los addons
- config ------------- Ruta con el nombre del archivo de la configuración de nuestro Odd 
```
{
    "addons_directory" : "/home/samuel/",
    "config" : "/home/samuel/temp/odoo.conf"
}
```
#### NOTA:
Para que el repo pueda ser agregado a la configuracion de nuestro odoo una vez clonado, es necesario agregar este TAG (#ADDLINE) debajo de la 
última linea de declaración de addons. 

Es muy importante que la declaración de "adoons_path" sea como se muestra en el siguiente ejemplo.

#### EJEMPLO
```
addons_path = /opt/odoo-server/addons
	      ,/opt/odoo-server/extra_addons/oca/pos
         ,/opt/odoo-server/extra_addons/oca/helpdesk
         ,/opt/odoo-server/extra_addons/oca/l10n-portugal
#ADDLINE
```
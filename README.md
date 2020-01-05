# **API REST para Diseño de Sistemas Interactivos**
La API que se presenta ha sido diseñada con la idea de poder ser utilizada en un posible Trabajo de Fin de Grado. Esto implica que los recursos aquí implementados están orientados hacia este TFG, y como este no se encuentra desarrollado completamente, puede albergar fallos o no ser estrictamente completo, sobre todo en cuanto a aspectos como la gestión de la persistencia.

## **1. Temática**
El TFG para el que esta API está orientada consiste en construir un sistema de gestión de energía, que regule los consumos y su obtención, con el objetivo de optimizar los costes y su sostenibilidad en el tiempo. Este sistema debe ayudarse de una API que dará soporte a los usuarios del mismo, permitiéndoles interactúar con el sistema.

Así pues, a lo largo del documento se van a presentar los diferentes recursos que va a tener la aplicación, así como los *endpoints* y sus funcionalidades.

## **2. Recursos**
### **2.1 Usuarios**
En nuestra aplicación va a ser neceario autenticarse para entrar, por lo que cada usuario debe estar registrado en la aplicación. La información almacenada de cada uno de ellos será el correo electrónico y una contraseña.

La clase `User` está compuesta de tres atributos:

Atributo    | Tipo      | Descripción
:---:       | :---:     | ---
`id`        | `Integer` | Identificador del usuario dentro del sistema. Es único, y es asignado por el sistema
`email`     | `String`  | Correo electrónico del usuario
`password`  | `String`  | Contraseña del usuario en el sistema. La dejamos como `String` por simplicidad del sistema. Pero en el futuro habría que incorporar algún tipo de seguridad
`logged`    | `Boolean` | Para simular la sesión de un ususario, se crea este atributo. Cuando un usuario inicie sesión, se pondrá en `True`, siendo `False` en cualquier otro caso. Para poder interactuar con el sistema, un usuario deberá iniciar sesión con anterioridad.

#### 2.1.1 Endpoints
URI                 | Método HTTP   | Descripción
:---:               |     :---:     | ---
`/users/login/`     | `PUT`         | Inicia sesión en el sistema. Si el usuario es encontrado en el sistema, y la contraseña es correcta, se dará su sesión como iniciada, pudiendo interactuar con el sistema. Recibe como datos el correo y la contraseña del usuario que desea iniciar sesión
`/users/logout/`    | `PUT`         | Cierra sesión en el sistema. Recibe como datos el correo del usuario que desea cerrar sesión
`/users/`           | `GET`         | Obtiene todos los usuarios del sistema. Esta funcionalidad debería estar solamente disponible para el administrador del sistema
`/users/`           | `POST`        | Crea un nuevo usuario. Recibe como datos los atributos del nuevo usuario
`/users/<int:id>/`  | `GET`         | Obtiene la información de un usuario específico. Debería estar solo disponible para el propio usuario y el administrador del sistema
`/users/<int:id>/`  | `PUT`         | Actualiza la información del usuario específico. Recibe como datos los atributos que se desean cambiar del usuario específico
`/users/<int:id>/`  | `DELETE`      | Elimina el usuario indicado de la base de datos

### **2.2 Edificios**
En la aplicación, los edificios almacenan los diferentes datos de consumo energético que cada uno de ellos genera, para poder ser consultados por cualquier usuario.

Así, la clase `Building` está compuesta de los siguientes atributos:

Atributo        | Tipo              | Descripción
:---:           | :---:             | ---
`id`            | `Integer`         | Identificador del edificio dentro del sistema. Es único, y asignado por el sistema
`name`          | `String`          | Nombre del edificio
`consumptions`  | `[Consumption]`   | Consumos energéticos que ha tenido el edificio. Será una lista de objetos `Consumption`, que se tratan más adelante

#### 2.2.1 Endpoints
URI                     | Método HTTP   | Descripción
:---:                   | :---:         | ---
`/buildings/`           | `GET`         | Obtiene todos los edificios. Por evitar saturaciones, solamente obtiene la información de los mismos, NO sus consumos. Para obtener los consumos de un edificio será necesario realizar otra petición distinta
`/buildings/`           | `POST`        | Crea un nuevo edificio. Recibe como datos el nombre del nuevo edificio
`/buildings/<int:id>/`  | `GET`         | Obtiene la información relativa al edificio específico
`/buildings/<int:id>/`  | `PUT`         | Edita la información sobre un edificio específico. Recibe como datos el nuevo nombre del edificio
`/buildings/<int:id>/`  | `DELETE`      | Elimina un edificio específico del sistema. Hay que tener en cuenta que sus consumos se perderán también

### **2.3 Consumos**
Como hemos dicho antes, los consumos serán almacenados por los distintos edificios del sistema, para poder ser consultados en cualquier momento. El objetivo es que cada edificio almacene un histórico de sus consumos. Cada edificio almacenará sus consumos diarios.

Para ello, la clase `Consumption` contará con los siguientes atributos:

Atributo    | Tipo      | Descripción
:---:       | :---:     | ---
`date`      | `Date`    | La fecha en la que el consumo se ha almacenado. Seguirá el formato `AAAA-MM-DD`
`value`     | `Double`  | Consumo energético registrado en dicho día

#### 2.3.1 Endpoints
URI                         | Método HTTP   | Descripción
:---:                       | :---:         | ---
`/consumptions/<int:b_id>/<string:inicio>/<string:final>/` | `GET`         | Obtiene todos los consumos del edificio correspondiente registrados entre las fechas `inicio` y `final`
`/consumptions/<int:b_id>/` | `POST`        | Añade un nuevo consumo al edificio indicado. Recibe como datos la fecha del consumo, y el propio consumo energético. Si la fecha ya tiene un consumo asignado, lanza un error. Para editar un consumo se debe usar otra URI
`/consumptions/<int:b_id>/<string:date>/`   | `PUT` | Edita el consumo correspondiente a la fecha indicada y perteneciente al edificio indicado. Recibe como datos el nuevo consumo
`/consumptions/<int:b_id>/<string:date>/`   | `DELETE`  | Elimina los consumos registrados en la fecha correspondiente y pertenecientes al edificio indicado
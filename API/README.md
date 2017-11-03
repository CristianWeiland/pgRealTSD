## Implementado por Eduardo Machado

Como rodar:

> * Instalar python3 e pip3
> * pip3 install requirements.txt
> * python3 manage.py runserver

Rotas:

>**GET /servers/**
>
>Mostra lista de servidores.


>**GET /servers/order/:order**
>
>Mostra lista de servidores ordenado.
>
>Parâmetros: <br>
>:order = 'name', '-name', 'active', '-active', 'state', '-state'


>**POST /servers/new**
>
>Adiciona um novo servidor.
>
>data:<br>
>{<br>
>"name": "nome_do_servidor",<br>
>"user_name": "usuario_usado_para_acessar_o_servidor",<br>
>}

>**GET /servers/:server_name/**
>
>Mostra os detalhes de um servidor.
>
>Parâmetros:<br>
>:server_name = Nome do servidor que se deseja ver os detalhes.

>**GET /servers/:server_name/:attribute/:period/:spacing**
>
>Mostra um período de dados de um determinado atributo.
>
>Parâmetros: <br>
>:server_name = Nome do servidor que se deseja ver os detalhes.<br>
>:attribute = {<br>
>('r' = Waiting processes),<br>
>('b' = Sleeping processes),<br>
>('swpd' = Virtual memory),<br>
>('free' = Idle memory),<br>
>('buff' = Memory used as buffers),<br>
>('cache' = Memory used as cache),<br>
>('inact' = Inactive memory),<br>
>('active' = Active memory),<br>
>('si' = Memory swapped in),<br>
>('so' = Memory swapped out),<br>
>('bi' = IO (in)),<br>
>('bo' = IO (out)),<br>
>('in' = System interrupts per second),<br>
>('cs' = Context switches per second),<br>
>('us' = CPU User time),<br>
>('sy' = CPU System time),<br>
>('id' = CPU Idle time),<br>
>('wa' = CPU IO wait time),<br>
>('st' = CPU Stolen from a virtual machine time)<br>
>}<br>
>:period = Período em minutos que deve ser mostrado.<br>
> * exemplo: 5 = mostra últimos 5 minutos de dados.<br>
>
>:spacing = Período em minutos que deve ser mostrado.<br>
> * exemplo: 3 = a cada 3 valores na base, retorna 1.


>**PUT /servers/:server_name/activation**
>
>Ativa ou desativa o coletor de dados do servidor.
>
>Parâmetros:<br>
>:server_name = Nome do servidor que se deseja ativar/desativar.


>DELETE /servers/:server_name/
>
>Exclui um servidor do banco de dados.
>
>Parâmetros: <br>
>:server_name = Nome do servidor que se deseja ver os detalhes.

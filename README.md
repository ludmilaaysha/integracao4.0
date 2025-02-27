# Integração 4.0 - Projeto Final

Repositório destinado ao Projeto Final da disciplina **Tópicos Especiais em Eletrônica**, semestre 2024.2, ministrada pelo professor Henrique Moura na Universidade de Brasília.

##

O projeto consiste em um sistema Django que recebe dados de distância medidos pelo sensor **HC-SR04** integrado à **RaspberryPi 4**. A partir das medições, são calculados os Limites de Controle, realizada a Análise de Capacidade ($C_p$ e $C_{pk}$), identificados os Outliers e o atendimento às quatro regras principais do Western Eletric Handbook.

Todos esses dados podem ser visualizados por meio dos gráficos X-barra e R plotados.

#

## 📦 Como Rodar o Projeto Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/ludmilaaysha/integracao4.0.git
```

### 2. Crie e ative um ambiente virtual

No **Linux/MacOS**:

```bash
python3 -m venv venv
source venv/bin/activate
```

No **Windows**:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Realize as migrações do banco de dados

```bash
python manage.py migrate
```

### 5. Execute o servidor local

```bash
python manage.py runserver
```

Acesse o projeto em: [http://localhost:8000](http://localhost:8000)

##

## 💻 Rodar o projeto com dados simulados

Caso queira visualizar o funcionamento do sistema simulando dados através da **Raspberry Pi**, siga os passos:

### 1. Acesse o arquivo disponível em

```bash
cd rpi/rpi.txt
```
### 2. Envie para a RPI e rode-o nela

### 3. Hospede o servidor
Substitua no arquivo o url do seu servidor hospedado

```bash
DJANGO_SERVER_URL = "<coloqueseuurl>/receive-data/"
```

### 4. Rode o projeto normalmente

#

## 👥 Contribuidores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/isaqzin">
        <img src="https://github.com/isaqzin.png" width="100px;" alt="Foto de perfil de isaqzin"/>
        <br />
        <sub><b>Isaque Camargos</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/ludmilaaysha">
        <img src="https://github.com/ludmilaaysha.png" width="100px;" alt="Foto de perfil de ludmilaaysha"/>
        <br />
        <sub><b>Ludmila Nunes</b></sub>
      </a>
    </td>
  </tr>
</table>
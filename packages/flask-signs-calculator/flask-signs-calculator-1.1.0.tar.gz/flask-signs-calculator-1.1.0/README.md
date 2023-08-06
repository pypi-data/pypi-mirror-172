## Como usar

### Requisitos

Instale os requisitos com `pip install -r requirements.txt`

### Configurações

Defina estas configurações em um arquivo chamado`.env`:

    FLASK_APP="signs_calculator/app.py"
    FLASK_DEBUG="true"
    SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost:5432/test"

Defina `FLASK_DEBUG` para `false` quando em produção

Defina `SQLALCHEMY_DATABASE_URI` como a uri do seu banco de dados

### Rodando o servidor

Rode o servidor com o comando `flask run`

### Uso

No seu navegador acesse `http://localhost:5000/calculadora/`, esse formulário vai aparecer:

![form](https://user-images.githubusercontent.com/110130850/186147454-65996fd2-6474-4c21-bbe9-5f77e7c985ee.png)

Preencha os dados de nascimento e verá qual seu signo e seu ascendente:

![result](https://user-images.githubusercontent.com/110130850/186147689-5167422d-3a6c-4513-abab-66bf26423bd3.png)

## Como usar

Instale com com `pip install -U flask-signs-calculator`.

### Exemplo simples

```
from flask import Flask
from sqlalchemy import create_engine
from signs_calculator import SignsCalculator

app = Flask(__name__)
db = create_engine('sqlite:///database.db')
SignsCalculator(app, db)
```

A classe SignsCalculator também precisa de uma instância de `Engine` de `sqlalchemy`

### Rotas

Acesse:

- `http://localhost:5000/calculadora-astrologica/` para resultados simples (signo e ascendente)
- `http://localhost:5000/calculadora-astrologica/completa` para resultados completos

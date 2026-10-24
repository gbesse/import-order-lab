# import-order-lab

## Français

Reproduire les défauts Python qui dépendent de l’ordre des imports.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m import_order_lab examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Installe des wheels locales de confiance, épinglées par SHA-256, dans un venv neuf puis exécute chaque permutation d’imports dans un processus neuf. La petite wheel fournie reproduit un succès ou échec selon l’ordre réel.

### Limites

Exécute du code local de confiance : ce n’est pas un bac à sable de sécurité. Pas de réseau ni dépendances téléchargées ; environnement enfant minimal sans clés. Quatre modules maximum, résultats bornés et empreintes de sortie, pas preuve d’absence d’interactions globales.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Reproduce Python failures depending on import order.

Synthetic data; no network access or secret required.

```sh
python -m import_order_lab examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Installs trusted local SHA-256-pinned wheels into a fresh venv, then runs each import permutation in a fresh process. The supplied tiny wheel reproduces success or failure depending on actual import order.

### Limits

Executes trusted local code: this is not a security sandbox. No network or downloaded dependencies; minimal child environment without keys. At most four modules, bounded results and output hashes, not proof of no global interactions.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Reproducir fallos Python que dependen del orden de importación.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m import_order_lab examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Instala wheels locales de confianza fijadas por SHA-256 en venv nuevo y ejecuta cada permutación de imports en proceso nuevo. La pequeña wheel reproduce éxito o fallo según orden real.

### Límites

Ejecuta código local de confianza: no es sandbox de seguridad. Sin red ni dependencias descargadas; entorno hijo mínimo sin claves. Máximo cuatro módulos, resultados acotados y resúmenes, sin prueba de ausencia de interacciones globales.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://docs.python.org/3/library/importlib.html
- https://docs.python.org/3/library/venv.html

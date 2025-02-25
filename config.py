

swagger_config = { ##item não obrigatorio
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/teste/teste/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/test" ## rota para documentação do swagger
}

swagger_template = { ##item recomendável caso tenha mais de uma classe de modelo
    "swagger": "2.0",
    "info": {
        "title": "API",
        "description": "API com documentação Swagger",
        "version": "1.0.0"
    },
    "host": "localhost:8080",
    "basePath": "/",
    "schemes": [
        "http"
    ],
    "definitions": {
        "Pessoa": { ## # Definição do modelo Trabalho no swagger
            "type": "object",
            "properties": {
                "id": {
                    "type": "string"
                },
                "nome": {
                    "type": "string"
                },
                "trabalho": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "string"
                        },
                        "cargo": {
                            "type": "string"
                        }
                    }
                }
            }
        },
        "Trabalho": {  # Definição do modelo Trabalho no swagger
            "type": "object",
            "properties": {
                "id": {
                    "type": "string"
                },
                "cargo": {
                    "type": "string"
                }
            }
        }
    }
}
import sys

from .algoritmos.gemini_integration import GeminiClient
from .utils import parse_args

"""
  Exemplo de utilização:
  uv run ia-m-uv -p 'prompt aqui'
  
  O arquivo main.py será chamado, nele a utilização do 'utils' é vista, além de ser possível a partir dele chamar outros algoritmos, até mesmo passar algum argumento texto:
  
  -p OU --problema 'prompt vai aqui'
"""


def main() -> None:
    print("Meu projeto!")
    args = parse_args()

    try:
        problema = args.problema
        print(f"Problema: {problema}")

        print("--- Teste de Geração de Texto Padrão ---")
        gemini_client = GeminiClient(api_key="chave-de-api", model_name="gemma-3-27b-it")
        response_text = gemini_client.generate_response(problema)
        print(f"Resposta: {response_text}\n")

        return 0
    except Exception as e:
        print(f"Erro: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

import os
from pathlib import Path

import uvicorn

# Se o painel não informar a porta automaticamente, troque 0 pela porta de Rede.
PORTA_MANUAL = 0

if __name__ == "__main__":
    # SERVER_PORT costuma ser fornecida pelo painel. APP_PORT permite configurá-la.
    porta = int(os.getenv("APP_PORT") or os.getenv("SERVER_PORT") or PORTA_MANUAL)
    if not 1 <= porta <= 65535:
        raise SystemExit(
            "Informe a porta mostrada em Rede/Network: configure APP_PORT "
            "no painel ou altere PORTA_MANUAL neste arquivo."
        )

    # 0.0.0.0 permite receber conexões externas. No servidor não usamos reload.
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=porta,
        app_dir=str(Path(__file__).resolve().parent),
    )

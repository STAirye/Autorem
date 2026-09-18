# -*- coding: utf-8 -*-
# ==========================================================================
# This code was generated with the assistance of Claude Opus 5 (Anthropic).
# The human author reviewed, modified, and integrated the code.
# Author: Simon Tobar - CESFAM Dr. Luis Ferrada Urzua (APS, SSMC)
# SPDX-License-Identifier: GPL-3.0-or-later
# ==========================================================================
"""
Los tests NUNCA tocan el caché REAL del usuario (`~/.autorem/`).

Cada `tests/test_*.py` lo importa PRIMERO (lo exige
`test_dotacion::test_todos_los_tests_aislan_el_cache_del_usuario`): redirige
`dotacion.RUTA_CACHE` y `estamentos.RUTA_CACHE` a una carpeta temporal antes de
que corra nada.

POR QUE (sep-2026): cada test tenia que acordarse de redirigirlo a mano, y uno se
olvido -- `test_externos_delta_y_detalle_conserva_filas` corria antes (orden
alfabetico) que el unico que lo redirigia, asi que CADA corrida de la suite
sobreescribia el `dotacion.json` real con 'FUNC EXTERNA'/'FUNC INTERNA'. En un PC
de trabajo eso es la clasificacion de externos del CESFAM, borrada por correr los
tests. Un test puede seguir apuntando `RUTA_CACHE` a su propio archivo: parte
desde aca, no desde el HOME.
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from programas import dotacion, estamentos   # noqa: E402

CARPETA = Path(tempfile.mkdtemp(prefix="autorem_cache_tests_"))
dotacion.RUTA_CACHE = CARPETA / "dotacion.json"
estamentos.RUTA_CACHE = CARPETA / "estamentos.json"

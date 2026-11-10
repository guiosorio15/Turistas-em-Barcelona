# Modelo E2

`e1_dfl_v3.joblib` — `HistGradientBoostingClassifier` de 3 classes (`H/A/D`) + Viterbi de 3 estados.

- **Treino:** 7 jogos DFL/Sportec (CC-BY 4.0), 1 002 644 frames.
- **Degradação:** 41% da bola em falta (lacunas de 3–30 s), 5% dos jogadores em falta por frame, ruído de 0,2 m.
- **Features:** 123, coletivas, sem identidades de jogador.
- **Custos de transição:** 9 (`H`↔`A`) e 12 (entrar/sair de `D`).
- **LOMO 7 jogos:** 0,525 ± 0,037; `macroF1` 0,868.
- **Estado:** congelado como candidato. E5 (bola fora), E2b (três classificadores) e E5b (4 estados, p90, etapa física) foram testados e pioraram em DFL; ver N13–N17.
- **Seed:** 0; `scikit-learn` 1.9.1.
- **Proveniência:** treinado apenas em dados públicos de outros jogos. O artefacto não contém dados do jogo fornecido.

Treino reproduzível:

```bash
uv sync --locked --extra notebooks
uv run --locked python scripts/fetch_dfl.py
uv run --locked --extra notebooks python scripts/train_model.py \
  --output models/e1_dfl_v3.joblib
```

Inferência no jogo fornecido:

```bash
uv run --locked python scripts/predict_target.py \
  --model models/e1_dfl_v3.joblib \
  --output outputs/submissions/Turistas_de_la_Nave.csv
```

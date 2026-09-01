# Engineered geometric features notebook summary

Repository commit: `7c844bffb553985f439f49c8d69e0b46bdc6a61d`

Evaluation label: **validation-split evaluation**.

ArGEnT engineered-feature inference was validated against the training-script `INPUT_COLS` / `QUERY_COLS` metadata.
PointNet headfeat inference now selects engineered features by explicit checkpoint column IDs instead of positional slicing, preserving training-time feature identity and normalization order.
The saved `feature_inference_validation.csv` report records feature counts, names, tensor shape, dtype, finite-value checks, preprocessing artifact references, and sample-alignment status.

Dataset available: quantitative feature-aware inference executed on the validation split and the resulting metrics/figures were regenerated from aligned shared sample IDs.

Static audit finding: no evidence was found that ArGEnT itself was dropping engineered inputs; its checkpoint/training metadata requires the engineered columns to enter through the encoder token tensor.
A separate notebook-side fragility was fixed for PointNet headfeat inference so engineered features are now addressed by their true training column IDs and not by positional prefix slicing.
# Engineered geometric features notebook summary

Repository commit: `ddaee34d2731dcfd06546c32f62b0ec9d863f9bf`

Evaluation label: **validation-split evaluation**.

ArGEnT engineered-feature inference was validated against the training-script `INPUT_COLS` / `QUERY_COLS` metadata.
PointNet headfeat inference now selects engineered features by explicit checkpoint column IDs instead of positional slicing, preserving training-time feature identity and normalization order.
The saved `feature_inference_validation.csv` report records feature counts, names, tensor shape, dtype, finite-value checks, preprocessing artifact references, and sample-alignment status.

Dataset limitation: the quantitative zonal HDF5 asset is unavailable in this environment, so the notebook completed with metadata-only validation artifacts and without regenerated numerical figures.

Static audit finding: no evidence was found that ArGEnT itself was dropping engineered inputs; its checkpoint/training metadata requires the engineered columns to enter through the encoder token tensor.
A separate notebook-side fragility was fixed for PointNet headfeat inference so engineered features are now addressed by their true training column IDs and not by positional prefix slicing.
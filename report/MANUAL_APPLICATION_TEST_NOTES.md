# Qualitative Testing of the Deployed Application

Seven hand-written Kinyarwanda sentences were entered manually into the Streamlit application. These examples are a small, targeted functionality check and are not a representative evaluation set.

## Results

- Correct predictions: 3/7
- Manual example accuracy: 42.9%
- Errors: two negative sentences were predicted as positive, and two negative sentences containing negation were predicted as neutral.
- The positive controls and the simple neutral statement were classified correctly in these examples.

## Interpretation

In these manually selected examples, the model recognized the positive examples and the factual neutral example, but it struggled with negative sentiment. In particular, “Sinakunze iyi filime na gato” and “Iyi serivisi ntabwo ari nziza” were both predicted as neutral. “Ndababaye cyane” and “Iyi filime ni mbi cyane” were predicted as positive. These outcomes suggest that negative wording and negation should be examined in future error analysis, but seven examples are not enough to prove the cause or estimate generalization performance.

The displayed class probability is the model's predicted-class probability; it should not be treated as a calibrated guarantee of correctness.

## Important distinction

This small manual check is separate from the held-out AfriSenti test-set evaluation. The formal held-out test results remain 65.01% accuracy and 0.6498 macro-F1. Do not replace the benchmark metrics with the manual example accuracy.

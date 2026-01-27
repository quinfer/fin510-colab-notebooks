# Statistical Science Checklist for Financial Data Analysis

**Purpose**: Apply this checklist to any empirical financial analysis—research papers, trading strategies, risk models, FinTech evaluations.

---

## 1. Data Quality and Measurement (Week 2, Chapter 02)

**Questions to ask**:

- [ ] **Where does the data come from?** (Data generating process)
- [ ] **What is the selection mechanism?** (Random sample or selected?)
- [ ] **Survivorship bias?** (Do we only observe winners/survivors?)
- [ ] **Look-ahead bias?** (Does analysis use future information unavailable at prediction time?)
- [ ] **Measurement validity?** (Do we measure what we claim to measure?)
- [ ] **Measurement reliability?** (Are measurements consistent/reproducible?)
- [ ] **Missing data?** (Why is data missing? Is it missing at random?)

**Red flags**:
- Backtest uses returns from indices that exclude delisted firms (survivorship bias)
- Analysis uses end-of-period data for beginning-of-period predictions (look-ahead bias)
- Transaction "categories" assigned by algorithm, not verified (validity issue)
- Only successful platforms/funds included in sample (selection bias)

---

## 2. Model Selection and Validation (Week 0, Chapter 00)

**Questions to ask**:

- [ ] **Cross-validation used?** (Not just single train/test split)
- [ ] **Temporal structure respected?** (For time series, use rolling/expanding windows—not random CV)
- [ ] **Out-of-sample testing?** (True holdout data never touched during development?)
- [ ] **Multiple testing corrected?** (If testing many models/features, apply Bonferroni/FDR)
- [ ] **Performance realistic?** (For return prediction, OOS R² > 5% is suspicious)
- [ ] **Comparison to naive baseline?** (Does model beat equal-weight/buy-hold/always-predict-majority?)

**Red flags**:
- Single train/test split (performance estimate has high variance)
- Random k-fold CV on time series (violates temporal ordering—look-ahead bias)
- Tested 100 strategies, report best (multiple testing without correction)
- OOS R² = 15% for monthly return prediction (suspiciously high—likely overfitting)
- No comparison to simple benchmarks (might underperform equal-weight!)

---

## 3. Regularization and Overfitting (Week 0, Chapter 00)

**Questions to ask**:

- [ ] **Regularization applied?** (L1/L2 for linear models, depth/leaf constraints for trees, dropout for neural nets)
- [ ] **Model complexity justified?** (Deep neural net for 1,000 samples—probably overfitting)
- [ ] **Bias-variance tradeoff discussed?** (All model choices trade these off)
- [ ] **Cross-validation to select hyperparameters?** (Not tuned on test set)
- [ ] **Simpler model compared?** (Logistic regression vs random forest—simpler often wins with limited data)

**Red flags**:
- 100 features with 500 samples (overparameterized)
- No regularization mentioned (likely overfitting)
- "We tried many models and selected the best" (tuned on test set—overfitting)
- Deep learning with small sample (almost certainly overfits)

---

## 4. Uncertainty Quantification (Week 0, Chapter 00)

**Questions to ask**:

- [ ] **Confidence intervals reported?** (Not just point estimates)
- [ ] **Standard errors provided?** (For regression coefficients, performance metrics)
- [ ] **Bootstrap used?** (For complex statistics where theory is hard)
- [ ] **Prediction intervals?** (Not just point forecasts)
- [ ] **Parameter uncertainty acknowledged?** (Estimated parameters ≠ true parameters)

**Red flags**:
- Only point estimates (no SEs, no CIs)
- "Optimal portfolio" with no uncertainty bounds (weights have huge uncertainty!)
- Forecast without prediction interval (no sense of forecast reliability)
- Parameters treated as known truth (ignores estimation error)

---

## 5. Statistical Significance and P-Values (Week 0, Chapter 00)

**Questions to ask**:

- [ ] **Gelman's pitfalls avoided?** (Statistical significance ≠ practical significance)
- [ ] **Effect sizes reported?** (Not just p-values—is effect meaningful?)
- [ ] **Multiple comparisons corrected?** (Testing many hypotheses inflates Type I error)
- [ ] **Sample size adequate?** (Small samples have low power)
- [ ] **Pre-registration or replication?** (To avoid p-hacking)

**Red flags**:
- "Significant at p < 0.05" without effect size (might be tiny and meaningless)
- Tested 50 factors, report 3 significant, no correction (multiple testing)
- Researcher degrees of freedom exploited (tried many specifications, report best)
- Small sample (n=50) with many features (p=20) claiming significant results (overfit)

---

## 6. Causal Inference (Week 0, Chapter 00)

**Questions to ask**:

- [ ] **Prediction vs causation distinguished?** (Model predicts ≠ intervention causes)
- [ ] **Identification strategy specified?** (RCT, natural experiment, IV, regression discontinuity?)
- [ ] **Confounders addressed?** (Omitted variables that bias estimates)
- [ ] **Selection bias?** (Treatment assignment non-random)
- [ ] **Causal claims justified?** (Or are they just correlations?)

**Red flags**:
- "X causes Y" based on regression (correlation ≠ causation!)
- Observational study claiming causal effect without addressing confounding
- No discussion of identification strategy (how do we know it's causal?)
- Selection on observables assumed (unobserved confounders ignored)

---

## 7. Rare Events and Class Imbalance (Week 0, Chapter 00; Ch 05, 08, 11, 12)

**Questions to ask**:

- [ ] **Base rate known?** (What proportion of positive class?)
- [ ] **Accuracy reported for rare events?** (Red flag—accuracy is misleading)
- [ ] **Appropriate metrics used?** (AUC, precision, recall, F1—not accuracy)
- [ ] **Confusion matrix shown?** (TP, FP, TN, FN with actual counts)
- [ ] **Threshold selection justified?** (Based on costs, not default 0.5)
- [ ] **Class weighting or resampling?** (To handle imbalance during training)

**Red flags**:
- "99% accurate fraud detection" for 0.1% fraud rate (likely predicting all legitimate)
- Accuracy reported, precision/recall not (hiding poor rare-event performance)
- Default 0.5 threshold used without justification (ignores cost asymmetry)
- No discussion of false positive vs false negative costs

---

## 8. Time-Series Specific Issues (Week 3, Ch 03, 04, 07, 08)

**Questions to ask**:

- [ ] **Temporal ordering preserved?** (No future data in training)
- [ ] **Autocorrelation acknowledged?** (Returns, volatility cluster)
- [ ] **Non-stationarity tested?** (Relationships change over time?)
- [ ] **Regime changes considered?** (Crisis vs calm periods differ)
- [ ] **Rolling/expanding windows used?** (Not random CV)
- [ ] **Structural breaks tested?** (Chow, Bai-Perron, Markov switching?)

**Red flags**:
- Random k-fold CV on time series (violates temporal structure)
- Training on 2010-2020, testing on 2015-2018 (test data earlier than some training data!)
- Assumes constant parameters across 2008 crisis (likely structural break)
- High GARCH persistence without testing for regime switching (might be artifact)

---

## 9. Estimation Error and Sensitivity (Week 0, Ch 04)

**Questions to ask**:

- [ ] **Parameter uncertainty acknowledged?** (All estimates have SEs)
- [ ] **Sensitivity analysis performed?** (How do results change with different inputs?)
- [ ] **Robustness checks?** (Different estimation windows, different specifications)
- [ ] **Estimation error propagation?** (Uncertainty in inputs → uncertainty in outputs)

**Red flags**:
- Portfolio optimization treats estimated returns as truth (sensitivity to inputs)
- No robustness checks (results could be fragile to small changes)
- Parameters from small sample treated as precise (estimation error large)
- Optimal decision assumes parameters are known (ignores parameter uncertainty)

---

## 10. Ethical and Practical Considerations

**Questions to ask**:

- [ ] **Who benefits? Who is harmed?** (Distributional effects)
- [ ] **Fairness evaluated?** (Across demographic groups, protected characteristics)
- [ ] **Privacy implications?** (What data is collected? How is it used?)
- [ ] **Explainability?** (Can predictions be explained to stakeholders?)
- [ ] **Operational feasibility?** (Can this run in production? Latency? Scale?)

**Red flags**:
- Claims "democratization" without evidence on who actually benefits (likely selective)
- Algorithmic decision-making without fairness evaluation (might discriminate)
- Model uses sensitive features (race proxies) without justification
- Black-box model for high-stakes decisions (unacceptable for regulatory contexts)

---

## Quick Reference: Common Pitfalls

| Pitfall | Example | Chapter | Correct Approach |
|---------|---------|---------|------------------|
| **Accuracy for rare events** | 99% accurate fraud detection for 0.1% fraud | Ch 05, 08 | Use AUC, precision, recall |
| **Single train/test split** | One 70/30 split, report performance | Ch 05 | Use 5-fold CV, report mean ± SD |
| **Random CV on time series** | Shuffle dates, k-fold CV | Ch 04, 07 | Use temporal validation (rolling windows) |
| **No regularization** | Fit model with p=50 features, n=100 samples | Ch 05 | Apply L1/L2, report cross-validated performance |
| **Treat estimates as truth** | Portfolio optimization with estimated returns | Ch 04 | Bootstrap CIs, sensitivity analysis |
| **Multiple testing** | Test 100 strategies, report best | Ch 07, 10 | Apply Bonferroni/FDR or out-of-sample holdout |
| **Survivorship bias** | Use S&P 500 returns 1990-2020 | Ch 02, 04 | Use point-in-time data including failures |
| **Correlation → Causation** | "X predicts Y, so X causes Y" | Ch 05 | State identification strategy or limit to prediction claims |
| **GARCH without break tests** | High persistence (α+β ≈ 0.98) | Ch 07 | Test for structural breaks, regime switching |
| **Overfitting to backtest** | Sharpe 2.5 in-sample, 0.3 OOS | Ch 10 | Compute PBO, require OOS validation |

---

## How to Use This Checklist

**When reading academic papers**:
1. Go through Sections 1-10 systematically
2. Note which items are satisfied, which are missing
3. Missing items → questions to ask authors

**When developing models**:
1. Use as design guide—ensure you address each section
2. Document decisions (why this CV strategy? Why this regularization?)
3. Include in model documentation for stakeholders/regulators

**When evaluating vendor claims**:
1. Ask vendors to demonstrate checklist compliance
2. "99% accurate" → demand precision/recall breakdown
3. "Proven in backtest" → demand OOS validation, PBO

**For assessments and coursework**:
1. Apply checklist to your own work before submission
2. Demonstrate you've considered each statistical issue
3. Acknowledge limitations explicitly (shows sophistication)

---

## Connection to Course Learning Objectives

This checklist operationalizes the course's central theme: **Financial data science is statistical science applied to financial problems.**

You've learned to:
- Question claims skeptically (does "democratization" have evidence?)
- Validate honestly (OOS performance, cross-validation)
- Acknowledge uncertainty (all parameters estimated with error)
- Distinguish prediction from causation (observational ≠ experimental)
- Recognize patterns across domains (Type I/II everywhere)

**These skills transfer**: Whether analyzing credit risk, detecting fraud, optimizing portfolios, or evaluating FinTech claims, the same statistical principles apply. This checklist is your portable framework for rigorous analysis in any financial data science context.

---

## Further Reading

**Textbook chapters with extensive treatment**:
- Chapter 00 (§0.2-0.8): Regression, validation, significance, causal inference
- Chapter 02 (§2.2-2.3): Data quality, measurement, selection bias
- Chapter 03 (§3.6): Structural breaks, regime switching
- Chapter 05 (credit scoring): Complete exemplar of checklist application
- Chapter 10 (§10.3): Multiple testing, CPCV, overfitting

**Key papers**:
- Gelman & Hill (2006): *Data Analysis Using Regression and Multilevel/Hierarchical Models*
- Harvey et al. (2016): "...and the Cross-Section of Expected Returns"
- Lopez de Prado (2014): "The Probability of Backtest Overfitting"
- @efron2016casi: *Computer Age Statistical Inference*

---

**Version**: 2026-01-24  
**Course**: FIN306 Financial Data Science  
**Author**: Based on course materials by Professor Barry Quinn

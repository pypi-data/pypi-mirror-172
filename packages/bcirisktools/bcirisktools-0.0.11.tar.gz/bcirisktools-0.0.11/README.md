# How to use

You must enter a dataframe with the features X and the target variable Y.

```python
test1, test2 = run_crt_tree(df_banked, "flag_30d_3m_ever", max_depth=2)
dict_summaries = get_statistics(test2)
get_report(dict_summaries, report_name="reporte_banked")
```
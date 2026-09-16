# Tight Loop Performance Exception (Ponytail Override)

When auditing code for over-engineering or replacing "hand-rolled" logic with standard library/third-party dependencies (e.g., when applying `ponytail` principles):
1. **Context matters:** Always check if the code executes inside a tight loop (e.g., >1,000 iterations per cycle).
2. **Instantiation Overhead:** Do not replace lightweight pure-Python math/geometry functions with heavy library objects (like `matplotlib.path.Path` or `numpy` class instantiations) inside tight loops if it introduces massive object-creation overhead.
3. **Execution over Dogma:** The simplest code that runs fast is better than "clean" dependency code that hangs the pipeline.
